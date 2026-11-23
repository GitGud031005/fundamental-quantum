"""qsvt_demo.py — shared QSP/QSVT helpers for the seminar demos.

Based on section 19 of QSVT_plan_v4 (v2: 0.5 normalisation for the smoothed 1/x),
plus helpers for the Stage 3 experiments (E4 fixed-point search, E5 Trotter,
E6 linear systems, E8 polynomial method).

Conventions
- W(x) = exp(i arccos(x) X)              ("Wx" convention, QSP theorem)
- R(x) = [[x, s], [s, -x]], s = sqrt(1-x^2) ("R" convention, block-encoding)
- exp(i phi Z) = RZ(-2 phi) in Qiskit
- The ancilla is always the highest-index qubit.
"""
import numpy as np
from numpy.polynomial import chebyshev as C
from scipy.optimize import minimize, linprog
from scipy.linalg import sqrtm, expm
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

SEED = 1234
rng = np.random.default_rng(SEED)


def reset_rng(seed=SEED):
    """Reset the module RNG so every notebook run gives the same numbers."""
    global rng
    rng = np.random.default_rng(seed)
    return rng


# ---------------------------------------------------------------- QSP core
def z_phase(phi):                      # e^{i phi Z}
    return np.diag([np.exp(1j * phi), np.exp(-1j * phi)])


def W(x):                              # e^{i arccos(x) X}
    s = np.sqrt(1 - x ** 2)
    return np.array([[x, 1j * s], [1j * s, x]])


def R(x):                              # reflection convention
    s = np.sqrt(1 - x ** 2)
    return np.array([[x, s], [s, -x]], dtype=complex)


def qsp(phis, x, conv="R"):
    sig = R(x) if conv == "R" else W(x)
    U = z_phase(phis[0])
    for p in phis[1:]:
        U = U @ sig @ z_phase(p)
    return U


def find_phases(f, d, restarts=8, conv="R"):
    """Fit Re P(x) = f(x) on the d+1 Chebyshev nodes with BFGS. Returns (phases, max error on a grid)."""
    m = d + 1
    xs = np.cos((2 * np.arange(m) + 1) * np.pi / (2 * m))      # Chebyshev nodes
    fx = f(xs)

    def loss(phis):
        return sum((qsp(phis, x, conv)[0, 0].real - y) ** 2 for x, y in zip(xs, fx))

    best = None
    for _ in range(restarts):
        res = minimize(loss, rng.uniform(-np.pi, np.pi, d + 1), method="BFGS")
        if best is None or res.fun < best.fun:
            best = res
    grid = np.linspace(-1, 1, 2001)
    err = max(abs(qsp(best.x, x, conv)[0, 0].real - f(x)) for x in grid)
    return best.x, err


def check_bounded(f, n=4001):
    """max |f| on a fine grid of [-1, 1]; QSP needs this to be <= 1."""
    grid = np.linspace(-1, 1, n)
    return float(np.max(np.abs(f(grid))))


# ------------------------------------------------------- block-encoding / QSVT
def random_hermitian(n, scale=1.1):
    """Real symmetric n x n matrix with ||A|| = 1/scale (so ||A|| < 1)."""
    H = rng.normal(size=(n, n))
    A = (H + H.T) / 2
    return A / (scale * np.linalg.norm(A, 2))


def block_encode(A):                   # A real Hermitian, ||A|| <= 1
    n = A.shape[0]
    B = np.real(sqrtm(np.eye(n) - A @ A))
    return np.block([[A, B], [B, -A]])  # ancilla = highest-index qubit


def qsvt_matrix(A, phis):
    n = A.shape[0]
    UA = block_encode(A)
    Zp = lambda p: np.kron(z_phase(p), np.eye(n))
    U = Zp(phis[0])
    for p in phis[1:]:
        U = U @ UA @ Zp(p)
    return U


def qsvt_circuit(A, phis):
    n = A.shape[0]
    m = int(np.log2(n))
    anc = m                                               # qubit m = ancilla
    UA = Operator(block_encode(A))
    qc = QuantumCircuit(m + 1)
    qc.rz(-2 * phis[-1], anc)                             # last phase acts first
    for p in phis[-2::-1]:                                # reverse order
        qc.unitary(UA, list(range(m + 1)), label="U_A")
        qc.rz(-2 * p, anc)
    return qc


def f_of_A(f, A):
    lam, V = np.linalg.eigh(A)
    return V @ np.diag(f(lam)) @ V.T


def min_degree(f, tol, dmax=800):
    """Smallest Chebyshev interpolation degree with max error < tol on [-1, 1]."""
    xs = np.linspace(-1, 1, 4001)
    fx = f(xs)
    for d in range(1, dmax):
        c = C.chebinterpolate(f, d)
        if np.max(np.abs(C.chebval(xs, c) - fx)) < tol:
            return d
    return None


def g_inv(kappa):                      # smoothed 1/x, times 0.5 so |g| <= 1
    def g(x):
        x = np.asarray(x, dtype=float)
        out = np.zeros_like(x)
        nz = x != 0
        out[nz] = 0.5 * (1 - np.exp(-(3 * kappa * x[nz]) ** 2)) / (kappa * x[nz])
        return out
    return g


# ------------------------------------------- E4: Grover vs fixed-point search
def grover_success(a, k):
    """Success probability after k Grover iterations, initial overlap a = sin^2(theta)."""
    theta = np.arcsin(np.sqrt(a))
    return np.sin((2 * k + 1) * theta) ** 2


def _cheb_T(L, x):
    """T_L(x) for real x, valid also for |x| > 1 (L may be non-integer when x >= 1)."""
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    inside = np.abs(x) <= 1
    out[inside] = np.cos(L * np.arccos(x[inside]))
    out[~inside] = np.cosh(L * np.arccosh(np.abs(x[~inside]))) * np.sign(x[~inside]) ** L
    return out


def ylc_gamma_inv(L, delta):
    """1/gamma = T_{1/L}(1/delta) (Yoder-Low-Chuang 2014)."""
    return np.cosh(np.arccosh(1 / delta) / L)


def ylc_success(a, L, delta):
    """Closed form: P_L(a) = 1 - delta^2 T_L(T_{1/L}(1/delta) sqrt(1-a))^2."""
    x = ylc_gamma_inv(L, delta) * np.sqrt(1 - np.asarray(a, dtype=float))
    return 1 - delta ** 2 * _cheb_T(L, x) ** 2


def ylc_length(w, delta):
    """Smallest odd L with P_L(a) >= 1 - delta^2 for every a >= w."""
    L = 1
    while ylc_gamma_inv(L, delta) * np.sqrt(1 - w) > 1:
        L += 2
    return L


def ylc_phases(L, delta):
    """Phases alpha_j, beta_j (j = 1..l, L = 2l+1) from Yoder-Low-Chuang."""
    l = (L - 1) // 2
    gamma = 1 / ylc_gamma_inv(L, delta)
    j = np.arange(1, l + 1)
    alpha = 2 * np.arctan2(1, np.tan(2 * np.pi * j / L) * np.sqrt(1 - gamma ** 2))
    beta = -alpha[::-1]
    return alpha, beta


def ylc_statevector_success(a, L, delta):
    """Simulate the YLC sequence in the 2D plane span{|good>, |bad>}."""
    alpha, beta = ylc_phases(L, delta)
    s = np.array([np.sqrt(a), np.sqrt(1 - a)], dtype=complex)    # |s> in (good, bad) basis
    T = np.array([1, 0], dtype=complex)
    S_s = lambda al: np.eye(2) - (1 - np.exp(-1j * al)) * np.outer(s, s.conj())
    S_t = lambda be: np.eye(2) - (1 - np.exp(1j * be)) * np.outer(T, T.conj())
    psi = s.copy()
    for al, be in zip(alpha, beta):
        psi = -S_s(al) @ (S_t(be) @ psi)
    return float(abs(psi[0]) ** 2)


# ------------------------------------------------------ E5: Trotter vs QSVT
def trotter_error(A, B, t, r, order=1):
    H = A + B
    exact = expm(-1j * H * t)
    dt = t / r
    if order == 1:
        step = expm(-1j * A * dt) @ expm(-1j * B * dt)
    else:                                  # symmetric (2nd order) Strang splitting
        half = expm(-1j * A * dt / 2)
        step = half @ expm(-1j * B * dt) @ half
    return np.linalg.norm(np.linalg.matrix_power(step, r) - exact, 2)


def trotter_steps(A, B, t, eps, order=1, rmax=10 ** 8):
    """Smallest r with ||U_trotter - e^{-iHt}|| < eps (doubling + binary search)."""
    hi = 1
    while trotter_error(A, B, t, hi, order) >= eps:
        hi *= 2
        if hi > rmax:
            return None
    lo = hi // 2
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if trotter_error(A, B, t, mid, order) < eps:
            hi = mid
        else:
            lo = mid
    return hi


def qsvt_degree_exp(t, eps):
    """Degree so that cos(tx) and sin(tx) are each within eps/2 (so e^{-itx} within eps)."""
    dc = min_degree(lambda x: np.cos(t * x), eps / 2)
    ds = min_degree(lambda x: np.sin(t * x), eps / 2)
    return max(dc, ds)


# ------------------------------------------------- E6: linear systems
def matrix_with_kappa(n, kappa):
    """Symmetric n x n matrix, eigenvalues of both signs in [1/kappa, 1] in absolute value."""
    Q, _ = np.linalg.qr(rng.normal(size=(n, n)))
    mags = np.geomspace(1 / kappa, 1, n)
    signs = np.where(np.arange(n) % 2 == 0, 1.0, -1.0)
    lam = signs * mags
    return Q @ np.diag(lam) @ Q.T


# ------------------------------------------------- E8: polynomial method
def or_feasible(N, d):
    """Is there q of degree d with |q(0)| <= 1/3 and |q(k) - 1| <= 1/3 for k = 1..N?"""
    k = np.arange(N + 1)
    y = 2 * k / N - 1                       # rescale Hamming weight to [-1, 1]
    V = C.chebvander(y, d)                  # rows: [T_0(y_k), ..., T_d(y_k)]
    lo = np.where(k == 0, -1 / 3, 2 / 3)
    hi = np.where(k == 0, 1 / 3, 4 / 3)
    A_ub = np.vstack([V, -V])
    b_ub = np.concatenate([hi, -lo])
    res = linprog(np.zeros(d + 1), A_ub=A_ub, b_ub=b_ub,
                  bounds=[(None, None)] * (d + 1), method="highs")
    return res.status == 0


def or_min_degree(N, dmax=200):
    for d in range(1, dmax):
        if or_feasible(N, d):
            return d
    return None


# ------------------------------------------------- E0 / E3: foundations, Grover
def helstrom(rho, sigma):
    """Optimal success probability of telling rho from sigma (equal priors).

    Returns (projector measurement result, formula 1/2 + D/2)."""
    lam, V = np.linalg.eigh(rho - sigma)
    E = V[:, lam > 0] @ V[:, lam > 0].conj().T            # projector on the positive part
    p_meas = 0.5 + 0.5 * np.real(np.trace(E @ (rho - sigma)))
    D = 0.5 * np.sum(np.abs(lam))
    return float(p_meas), float(0.5 + 0.5 * D)


def werner_min_pt_eig(p):
    """Smallest eigenvalue of the partial transpose of p|Phi+><Phi+| + (1-p) I/4."""
    phi = np.array([1, 0, 0, 1]) / np.sqrt(2)
    rho = p * np.outer(phi, phi) + (1 - p) * np.eye(4) / 4
    pt = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)   # transpose qubit B
    return float(np.linalg.eigvalsh(pt).min())


def grover_success_sv(N, M, k):
    """Success probability after k Grover iterations, by statevector simulation."""
    psi = np.ones(N) / np.sqrt(N)
    s = psi.copy()
    marked = np.zeros(N, dtype=bool)
    marked[:M] = True
    for _ in range(k):
        psi = np.where(marked, -psi, psi)                 # oracle O_±
        psi = 2 * s * (s @ psi) - psi                     # diffusion 2|s><s| - I
    return float(np.sum(psi[marked] ** 2))


# ------------------------------------------------- E10-E12: big-data tasks
def hermitian_dilation(X):
    """H = [[0, X], [X^T, 0]]: Hermitian, eigenvalues ±sigma_i (and zeros)."""
    n, d = X.shape
    return np.block([[np.zeros((n, n)), X], [X.T, np.zeros((d, d))]])


def matrix_with_singular_values(n, d, svals):
    U, _ = np.linalg.qr(rng.normal(size=(n, d)))
    V, _ = np.linalg.qr(rng.normal(size=(d, d)))
    return U[:, :len(svals)] @ np.diag(svals) @ V[:, :len(svals)].T


def smooth_step(tau, delta, scale=0.999):
    """Even function ~0 for |x| < tau - delta/2, ~1 for |x| > tau + delta/2 (bounded by `scale`)."""
    from scipy.special import erf
    return lambda x: scale * 0.5 * (1 + erf(2 * (np.abs(np.asarray(x, dtype=float)) - tau) / delta))


def cheb_poly(f, d):
    c = C.chebinterpolate(f, d)
    return lambda x: C.chebval(x, c)


def verdict(ok):
    return "PASS" if ok else "FAIL"
