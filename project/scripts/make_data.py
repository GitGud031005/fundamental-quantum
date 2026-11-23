"""Precompute the data files that Demo 3 reads (E4, E5, E6, E8).

Run from the project folder:  python scripts/make_data.py
Writes CSV files into data/. Takes about a minute.
"""
import csv
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import qsvt_demo as q  # noqa: E402

DATA = ROOT / "data"
DATA.mkdir(exist_ok=True)


def write(name, header, rows):
    with open(DATA / name, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote data/{name} ({len(rows)} rows)")


# ---------------------------------------------------------------- E4
W_LOW, DELTA = 0.05, 0.1
L = q.ylc_length(W_LOW, DELTA)
K = (L - 1) // 2                       # Grover with the same number of oracle calls
a_grid = np.geomspace(1e-3, 1, 400)
ylc = q.ylc_success(a_grid, L, DELTA)
grv = q.grover_success(a_grid, K)
# cross-check the closed form against a 2D statevector simulation of the YLC phases
sv_err = max(abs(q.ylc_statevector_success(a, L, DELTA) - p) for a, p in zip(a_grid[::20], ylc[::20]))
write("e4_success.csv", ["a", "grover", "fixed_point", "w", "delta", "L", "k_grover", "sv_check_err"],
      [[f"{a:.6g}", f"{g:.10f}", f"{y:.10f}", W_LOW, DELTA, L, K, f"{sv_err:.2e}"]
       for a, g, y in zip(a_grid, grv, ylc)])

# ---------------------------------------------------------------- E5
q.reset_rng(q.SEED)
H = q.random_hermitian(8, scale=1.0)   # ||H|| = 1 so the QSVT block-encoding applies
A_part = np.diag(np.diag(H))           # split H = diagonal + off-diagonal
B_part = H - A_part
EPS5 = 1e-3
rows = []
for t in [1, 2, 4, 8, 16, 32]:
    d_cos6 = q.min_degree(lambda x, t=t: np.cos(t * x), 1e-6)
    d_qsvt = q.qsvt_degree_exp(t, EPS5)
    r1 = q.trotter_steps(A_part, B_part, t, EPS5, order=1)
    r2 = q.trotter_steps(A_part, B_part, t, EPS5, order=2)
    rows.append([t, d_cos6, d_qsvt, r1, r2])
    print(f"  E5 t={t}: deg cos(1e-6)={d_cos6}, QSVT deg(1e-3)={d_qsvt}, Trotter1={r1}, Trotter2={r2}")
write("e5_degrees.csv", ["t", "deg_cos_1e-6", "qsvt_degree_1e-3", "trotter1_steps", "trotter2_steps"], rows)

# ---------------------------------------------------------------- E6
q.reset_rng(q.SEED)
TOL6 = 1e-3
rows = []
for kappa in [2, 4, 8, 16, 32]:
    g = q.g_inv(kappa)
    d = q.min_degree(g, TOL6)
    c = np.polynomial.chebyshev.chebinterpolate(g, d)
    poly = lambda x, c=c: np.polynomial.chebyshev.chebval(x, c)
    for n in (4, 8):
        A = q.matrix_with_kappa(n, kappa)
        b = q.rng.normal(size=n)
        b /= np.linalg.norm(b)
        x_true = np.linalg.solve(A, b)
        gb = q.f_of_A(poly, A) @ b               # what the QSVT circuit applies (block 0)
        x_est = 2 * kappa * gb                   # undo the 0.5/kappa normalisation
        rel = np.linalg.norm(x_est - x_true) / np.linalg.norm(x_true)
        p_succ = np.linalg.norm(gb) ** 2         # post-selection probability
        rows.append([kappa, n, d, f"{q.check_bounded(g):.4f}", f"{rel:.2e}", f"{p_succ:.4f}"])
        print(f"  E6 kappa={kappa} n={n}: degree={d}, rel err={rel:.2e}, p_succ={p_succ:.4f}")
write("e6_degrees.csv", ["kappa", "n", "degree", "max_abs_g", "rel_error", "p_success"], rows)

# ---------------------------------------------------------------- E8
rows = []
for N in [16, 64, 256]:
    d = q.or_min_degree(N)
    rows.append([N, d, f"{d / np.sqrt(N):.3f}"])
    print(f"  E8 N={N}: min degree={d}, d/sqrt(N)={d / np.sqrt(N):.3f}")
write("e8_or_degree.csv", ["N", "min_degree", "d_over_sqrtN"], rows)

# ---------------------------------------------------------------- E3 (Grover, N = 64)
N3 = 64
rows = []
for M in (1, 3):
    theta = np.arcsin(np.sqrt(M / N3))
    for k in range(13):
        sv = q.grover_success_sv(N3, M, k)
        rows.append([M, k, f"{sv:.12f}", f"{np.sin((2 * k + 1) * theta) ** 2:.12f}"])
write("e3_grover.csv", ["M", "k", "statevector", "formula"], rows)

# ---------------------------------------------------------------- E10 (least squares)
q.reset_rng(q.SEED)
rows = []
for kappa in (2, 4, 8):
    n, d = 12, 4
    X = q.matrix_with_singular_values(n, d, np.geomspace(1, 1 / kappa, d))
    beta = q.rng.normal(size=d)
    y = X @ beta + 0.05 * q.rng.normal(size=n)
    y /= np.linalg.norm(y)
    g = q.g_inv(kappa)
    deg = q.min_degree(g, 1e-3)
    H = q.hermitian_dilation(X)
    out = q.f_of_A(q.cheb_poly(g, deg), H) @ np.concatenate([y, np.zeros(d)])
    b_q = 2 * kappa * out[n:]
    b_c = np.linalg.lstsq(X, y, rcond=None)[0]
    rel = np.linalg.norm(b_q - b_c) / np.linalg.norm(b_c)
    rows.append([kappa, n, d, H.shape[0], deg, f"{rel:.2e}", f"{np.linalg.norm(out) ** 2:.4f}"])
    print(f"  E10 kappa={kappa}: degree={deg}, rel err={rel:.2e}, p={np.linalg.norm(out) ** 2:.4f}")
write("e10_regression.csv", ["kappa", "n", "d", "dilation_dim", "degree", "rel_error", "p_success"], rows)

# ---------------------------------------------------------------- E11 (PCA filter)
q.reset_rng(q.SEED)
N11, TAU = 16, 0.5
svals = np.concatenate([[0.95, 0.8], q.rng.uniform(0, 0.25, N11 - 2)])
X = q.matrix_with_singular_values(N11, N11, svals)
_, _, Vt = np.linalg.svd(X)
P_true = Vt[:2].T @ Vt[:2]
rows = []
for delta in (0.3, 0.2, 0.1, 0.05):
    f = q.smooth_step(TAU, delta)
    deg = q.min_degree(f, 1e-2)
    P = q.f_of_A(q.cheb_poly(f, deg), q.hermitian_dilation(X))[N11:, N11:]   # right-singular block
    err = np.linalg.norm(P - P_true, 2)
    rows.append([delta, deg, f"{deg * delta:.1f}", f"{err:.2e}"])
    print(f"  E11 delta={delta}: degree={deg}, projector err={err:.2e}")
write("e11_pca_degrees.csv", ["delta", "degree", "degree_x_delta", "projector_error"], rows)

# ---------------------------------------------------------------- E12 (block-encoding normalisation)
q.reset_rng(q.SEED)
rows = []
for N12 in (256, 512, 1024):
    full = q.rng.normal(size=(N12, N12))
    low = q.rng.normal(size=(N12, 5)) @ q.rng.normal(size=(5, N12))
    for name, A in (("full rank", full), ("rank 5", low)):
        ratio = np.linalg.norm(A, "fro") / np.linalg.norm(A, 2)
        rows.append([N12, name, f"{ratio:.2f}", f"{np.sqrt(N12) / 2:.1f}" if name == "full rank" else f"{np.sqrt(5):.2f}"])
        print(f"  E12 N={N12} {name}: ||A||_F/||A|| = {ratio:.2f}")
write("e12_frobenius_ratio.csv", ["N", "matrix", "fro_over_spectral", "reference"], rows)
