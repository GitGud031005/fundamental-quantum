"""Generate the five demo notebooks in notebooks/.

Run from the project folder:  python scripts/build_notebooks.py
Then execute them (outputs saved in place):
  jupyter nbconvert --to notebook --execute --inplace notebooks/demo*.ipynb
"""
from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks"
OUT.mkdir(exist_ok=True)

SETUP = """\
import sys
from pathlib import Path
ROOT = Path.cwd().parent if Path.cwd().name == "notebooks" else Path.cwd()
sys.path.insert(0, str(ROOT / "src"))
DATA = ROOT / "data"

import numpy as np
import matplotlib.pyplot as plt
import qiskit
from qsvt_demo import *
import qsvt_demo

plt.rcParams.update({"font.size": 13, "figure.figsize": (8, 3.6), "axes.grid": True})
reset_rng()
print(f"Qiskit {qiskit.__version__} | numpy {np.__version__} | seed {SEED}")"""


def md(s):
    return nbf.v4.new_markdown_cell(s)


def code(s):
    return nbf.v4.new_code_cell(s)


def save(name, cells):
    nb = nbf.v4.new_notebook()
    nb["cells"] = cells
    nb["metadata"]["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
    nbf.write(nb, OUT / name)
    print("wrote notebooks/" + name)


# ===================================================================== Demo 1
save("demo1_qsp_phases.ipynb", [
    md("# Demo 1 — QSP và tìm pha\n"
       "**Người nói 1 · 06:30–09:00 (2 phút 30)**\n\n"
       "Ý chính: một chuỗi phép quay một qubit tạo ra đa thức $P(x)$; chọn pha là chọn đa thức."),
    md("## Cell 1 — Thiết lập\nToàn bộ hàm nằm trong `src/qsvt_demo.py`, seed cố định."),
    code(SETUP),
    md("## Cell 2 — Pha bằng 0 cho đúng Chebyshev $T_d$\n"
       "$U_\\Phi(x)=e^{i\\phi_0 Z}\\prod_k W(x)e^{i\\phi_k Z}$ với mọi $\\phi_k=0$ cho $P(x)=\\cos(d\\arccos x)=T_d(x)$."),
    code("""\
xs = np.linspace(-1, 1, 101)
fig, ax = plt.subplots()
ok = True
for d in [3, 6, 9]:
    P = np.array([qsp(np.zeros(d + 1), x, "Wx")[0, 0] for x in xs])
    err = np.max(np.abs(P - np.cos(d * np.arccos(xs))))
    ok &= err < 1e-12
    print(f"T_{d}: err = {err:.1e}")
    ax.plot(xs, P.real, lw=2, label=f"QSP, d={d}")
    ax.plot(xs, np.cos(d * np.arccos(xs)), "k:", lw=1)
ax.set_xlabel("x"); ax.set_ylabel("P(x)"); ax.set_title("Pha 0: P(x) trùng T_d(x) (đường chấm)")
ax.legend(loc="lower left"); plt.show()
print(verdict(ok))"""),
    md("## Cell 3 — Quy ước $R_Z$: $e^{i\\phi Z}=R_Z(-2\\phi)$\nSai dấu ở đây là sai toàn bộ QSP khi chuyển sang mạch."),
    code("""\
from qiskit.circuit.library import RZGate
from qiskit.quantum_info import Operator
phi = 0.37
err = np.linalg.norm(Operator(RZGate(-2 * phi)).data - z_phase(phi))
print(f"e^(i phi Z) vs RZ(-2 phi): {err:.1e}", verdict(err < 1e-12))"""),
    md("## Cell 4 — Tìm pha cho $f(x)=0.8\\cos(3x)$, bậc $d=10$\n"
       "BFGS tự viết, 8 lần khởi tạo, khớp $\\mathrm{Re}\\,P$ trên nút Chebyshev. Tiêu chí E1: sai số đều $<10^{-4}$."),
    code("""\
import time
f1 = lambda x: 0.8 * np.cos(3 * x)
t0 = time.time()
reset_rng()
phis, err = find_phases(f1, 10)
np.save(DATA / "phases_cos3x_d10.npy", phis)
print(f"{len(phis)} pha, sai số đều = {err:.2e}, thời gian {time.time() - t0:.1f} s")
print(np.round(phis, 4))

grid = np.linspace(-1, 1, 401)
ReP = np.array([qsp(phis, x)[0, 0].real for x in grid])
fig, ax = plt.subplots()
ax.plot(grid, f1(grid), lw=4, alpha=0.35, label="mục tiêu 0.8 cos(3x)")
ax.plot(grid, ReP, "k--", lw=1.5, label="Re P(x) từ 11 pha")
ax.set_xlabel("x"); ax.legend(loc="lower center"); plt.show()
print(verdict(err < 1e-4))"""),
    md("## Cell 4b — Dự phòng\nNếu cell 4 chạy quá 20 giây: đọc pha đã lưu và vẽ lại."),
    code("""\
phis = np.load(DATA / "phases_cos3x_d10.npy")
grid = np.linspace(-1, 1, 401)
err = np.max(np.abs([qsp(phis, x)[0, 0].real - f1(x) for x in grid]))
print(f"pha đã lưu: sai số đều = {err:.2e}", verdict(err < 1e-4))"""),
    md("## Cell 5 — Luôn kiểm tra $\\max|f|\\le 1$ trước khi tìm pha\nQSP chỉ tạo được đa thức bị chặn bởi 1 trên $[-1,1]$."),
    code("""\
m = check_bounded(f1)
print(f"max|f| trên lưới 4001 điểm = {m:.3f}", verdict(m <= 1))"""),
])

# ===================================================================== Demo 2
save("demo2_qsvt_circuit_measure.ipynb", [
    md("# Demo 2 — QSVT trên ma trận 4×4, mạch Qiskit và đo trên Aer\n"
       "**Người nói 2 · 15:30–18:30 (3 phút)**\n\n"
       "Ý chính (RQ1): mỗi trị riêng có một không gian con 2 chiều bất biến, nên cùng một bộ pha áp được cho cả ma trận."),
    md("## Cell 1 — Ma trận và pha\n$A$ đối xứng 4×4 ngẫu nhiên, chia cho $1.1\\|A\\|$; pha lấy từ Demo 1."),
    code(SETUP + """

A = random_hermitian(4, scale=1.1)
f1 = lambda x: 0.8 * np.cos(3 * x)
phis = np.load(DATA / "phases_cos3x_d10.npy")
print("trị riêng của A:", np.round(np.linalg.eigvalsh(A), 4))"""),
    md("## Cell 2 — Block-encoding kiểu phản xạ\n"
       "$U_A=\\begin{pmatrix}A&\\sqrt{I-A^2}\\\\\\sqrt{I-A^2}&-A\\end{pmatrix}$ — ancilla là qubit chỉ số cao nhất."),
    code("""\
UA = block_encode(A)
e_unit = np.linalg.norm(UA @ UA.conj().T - np.eye(8))
e_block = np.linalg.norm(UA[:4, :4] - A)
print(f"||U U^† - I|| = {e_unit:.1e}   ||khối trên-trái - A|| = {e_block:.1e}")
print(verdict(e_unit < 1e-12 and e_block < 1e-12))"""),
    md("## Cell 3 — RQ1 bằng số: không gian con bất biến\n"
       "Với $A|v\\rangle=\\lambda|v\\rangle$, $U_A$ giữ nguyên $\\mathrm{span}\\{|0\\rangle|v\\rangle,|1\\rangle|v\\rangle\\}$ và tác động ở đó đúng như $R(\\lambda)$."),
    code("""\
lam, V = np.linalg.eigh(A)
ok = True
for l, v in zip(lam, V.T):
    B = np.stack([np.kron([1, 0], v), np.kron([0, 1], v)], axis=1)   # 8x2, ancilla = qubit cao nhất
    blk = B.conj().T @ UA @ B
    leak = np.linalg.norm(UA @ B - B @ blk)
    e = np.linalg.norm(blk - R(l))
    ok &= e < 1e-12 and leak < 1e-12
    print(f"lambda = {l:+.3f}   ||blk - R(lambda)|| = {e:.1e}   rò ra ngoài = {leak:.1e}")
print(verdict(ok))"""),
    md("## Cell 4 — QSVT bằng ma trận: cùng 11 pha, áp lên cả $A$\n"
       "So $\\mathrm{Re}$ khối trên-trái với $f(A)=0.8\\cos(3A)$; sai số phải cùng cỡ sai số xấp xỉ của Demo 1."),
    code("""\
U = qsvt_matrix(A, phis)
err_fA = np.linalg.norm(U[:4, :4].real - f_of_A(f1, A), 2)
print(f"||Re U[:4,:4] - f(A)|| = {err_fA:.2e}", verdict(err_fA < 1e-4))"""),
    md("## Cell 5 — Mạch Qiskit\n3 qubit, ancilla là q2; mỗi pha là một $R_Z(-2\\phi)$; append theo thứ tự đảo vì tích ma trận đọc từ phải."),
    code("""\
from qiskit.quantum_info import Operator
qc = qsvt_circuit(A, phis)
display(qc.draw("mpl", fold=-1, scale=0.55))
ops = qc.count_ops()
err_circ = np.linalg.norm(Operator(qc).data - U, 2)
print(f"số lần gọi U_A = {ops.get('unitary', 0)}, số cổng RZ = {ops['rz']}")
print(f"||Operator(qc) - numpy|| = {err_circ:.2e}", verdict(err_circ < 1e-10))"""),
    md("## Cell 6 — E7: đo ancilla trên Aer\n"
       "Chuẩn bị $|0\\rangle_{anc}|{+}{+}\\rangle$, chạy mạch, đo ancilla 20 000 shot. "
       "Tần suất ancilla $=0$ phải nằm trong $p\\pm3\\sigma$ với $p=\\|P(A)\\psi\\|^2$; trạng thái hậu chọn phải có fidelity $>1-10^{-10}$."),
    code("""\
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector

psi = np.ones(4) / 2                                   # |++> trên q0, q1
meas = QuantumCircuit(3, 1)
meas.initialize(psi, [0, 1])
meas.compose(qc, inplace=True)
meas.measure(2, 0)                                     # ancilla = q2
sim, N = AerSimulator(seed_simulator=SEED), 20000
counts = sim.run(transpile(meas, sim), shots=N).result().get_counts()
freq = counts.get("0", 0) / N

PA_psi = U[:4, :4] @ psi                               # khối trên-trái (phức) tác động lên psi
p = np.linalg.norm(PA_psi) ** 2
sig = np.sqrt(p * (1 - p) / N)
ok_freq = abs(freq - p) <= 3 * sig
print(f"p lý thuyết = {p:.4f}   tần suất đo = {freq:.4f}   3σ = {3 * sig:.4f}", verdict(ok_freq))

sv = Statevector(np.kron([1, 0], psi)).evolve(qc).data[:4]
fid = abs(np.vdot(sv / np.linalg.norm(sv), PA_psi / np.linalg.norm(PA_psi))) ** 2
print(f"fidelity trạng thái hậu chọn = {fid:.12f}", verdict(fid > 1 - 1e-10))"""),
])

# ===================================================================== Demo 3
save("demo3_algorithms.ipynb", [
    md("# Demo 3 — Ba thuật toán và cận dưới\n"
       "**Người nói 3 · 23:00–25:30 (2 phút 30)**\n\n"
       "Cell 1, 2, 4 đọc dữ liệu tính sẵn bằng `scripts/make_data.py`; chỉ cell 3 chạy trực tiếp."),
    code(SETUP + """
import csv

def read_csv(name):
    with open(DATA / name, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}"""),
    md("## Cell 1 — E4: Grover gốc so với fixed-point search (Yoder–Low–Chuang)\n"
       "Cùng số lần gọi oracle. Grover dao động và rơi khi $a$ khác giá trị thiết kế; fixed-point giữ trên $1-\\delta^2$ với mọi $a\\ge w$."),
    code("""\
e4 = read_csv("e4_success.csv")
a = e4["a"].astype(float); grv = e4["grover"].astype(float); fp = e4["fixed_point"].astype(float)
w, delta, L, k = float(e4["w"][0]), float(e4["delta"][0]), int(e4["L"][0]), int(e4["k_grover"][0])
fig, ax = plt.subplots()
ax.semilogx(a, grv, lw=1.5, label=f"Grover, k={k} vòng")
ax.semilogx(a, fp, lw=2.5, label=f"fixed-point, L={L}")
ax.axhline(1 - delta**2, color="k", ls="--", lw=1); ax.axvline(w, color="gray", ls=":", lw=1)
ax.text(w * 1.1, 0.45, f"a = w = {w}", color="gray")
ax.set_xlabel("a (tỉ lệ nghiệm)"); ax.set_ylabel("xác suất thành công")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2, frameon=False); plt.show()
ok = np.all(fp[a >= w] >= 1 - delta**2 - 1e-12)
print(f"min fixed-point trên a ≥ w: {fp[a >= w].min():.4f} (ngưỡng {1 - delta**2})", verdict(ok))
print(f"kiểm tra công thức bằng mô phỏng 2D: sai số {e4['sv_check_err'][0]}")"""),
    md("## Cell 2 — E5: mô phỏng Hamiltonian, bậc QSVT so với số bước Trotter\n"
       "$H$ ngẫu nhiên 8×8, $\\|H\\|=1$, mục tiêu $\\|U-e^{-iHt}\\|<10^{-3}$. Bậc QSVT = số lần gọi block-encoding."),
    code("""\
e5 = read_csv("e5_degrees.csv")
t = e5["t"].astype(float)
cols = [("qsvt_degree_1e-3", "QSVT: bậc đa thức"), ("trotter2_steps", "Trotter bậc 2: số bước"),
        ("trotter1_steps", "Trotter bậc 1: số bước")]
fig, ax = plt.subplots()
for key, label in cols:
    y = e5[key].astype(float)
    slope = np.polyfit(np.log(t[-3:]), np.log(y[-3:]), 1)[0]
    ax.loglog(t, y, "o-", lw=2, label=f"{label} (độ dốc ≈ {slope:.2f})")
ax.set_xlabel("t"); ax.set_ylabel("số truy vấn / số bước"); ax.legend(loc="upper left", fontsize=11); plt.show()
print("t     bậc cos(1e-6)  QSVT(1e-3)  Trotter1  Trotter2")
for row in zip(*(e5[c] for c in ["t", "deg_cos_1e-6", "qsvt_degree_1e-3", "trotter1_steps", "trotter2_steps"])):
    print("{:<6}{:<15}{:<12}{:<10}{}".format(*row))"""),
    md("## Cell 3 — E6: hệ tuyến tính (chạy trực tiếp)\n"
       "Hàm $1/x$ làm trơn $g(x)=\\frac{1-e^{-(3\\kappa x)^2}}{\\kappa x}$ vượt 1 — không có bộ pha nào cho nó. Nhân 0.5 thì hợp lệ."),
    code("""\
grid = np.linspace(-1, 1, 4001)
g = g_inv(8)
print(f"không nhân 0.5: max|g| = {np.max(np.abs(2 * g(grid))):.3f}", verdict(np.max(np.abs(2 * g(grid))) <= 1))
print(f"nhân 0.5:       max|g| = {np.max(np.abs(g(grid))):.3f}", verdict(np.max(np.abs(g(grid))) <= 1))
degs = [(k, min_degree(g_inv(k), 1e-3)) for k in [2, 4, 8, 16]]
for k, d in degs:
    print(f"kappa = {k:>2}: bậc = {d:>3}   bậc/kappa = {d / k:.1f}")"""),
    code("""\
e6 = read_csv("e6_degrees.csv")
print("kappa  n  bậc  sai số tương đối  xác suất hậu chọn")
for row in zip(*(e6[c] for c in ["kappa", "n", "degree", "rel_error", "p_success"])):
    print("{:<7}{:<3}{:<5}{:<18}{}".format(*row))"""),
    md("## Cell 4 — E8: polynomial method cho OR\n"
       "Bậc nhỏ nhất để có $q$ với $|q(0)|\\le 1/3$, $|q(k)-1|\\le 1/3$ ($k=1..N$), giải bằng `linprog` trong cơ sở Chebyshev. "
       "$d/\\sqrt N$ gần như hằng số nên Grover tối ưu."),
    code("""\
e8 = read_csv("e8_or_degree.csv")
print("N     bậc nhỏ nhất  d/sqrt(N)")
for row in zip(e8["N"], e8["min_degree"], e8["d_over_sqrtN"]):
    print("{:<6}{:<14}{}".format(*row))
r = e8["d_over_sqrtN"].astype(float)
print(verdict(r.max() / r.min() < 1.5))"""),
])

# ===================================================================== Demo 0
save("demo0_foundations_grover.ipynb", [
    md("# Demo 0 — Toán nền và Grover\n"
       "**Người nói 1 · 11:00–12:30 (1 phút 30)**\n\n"
       "Cell 2 hiện output đã lưu; cell 3–4 chạy trực tiếp."),
    code(SETUP),
    md("## Cell 2 — E0 rút gọn: Helstrom, Werner, hậu chọn\n"
       "Helstrom: phân biệt |0⟩ và |+⟩ tối ưu với xác suất ½ + ½D = cos²(π/8). "
       "Werner p|Φ⁺⟩⟨Φ⁺| + (1−p)I/4 rối khi p > 1/3 (chuyển vị riêng phần có trị riêng âm)."),
    code("""\
ket0, plus = np.array([1, 0]), np.array([1, 1]) / np.sqrt(2)
p_meas, p_formula = helstrom(np.outer(ket0, ket0), np.outer(plus, plus))
ok1 = abs(p_meas - np.cos(np.pi / 8) ** 2) < 1e-12 and abs(p_meas - p_formula) < 1e-12
print(f"Helstrom: đo bằng projector = {p_meas:.4f}, cos²(π/8) = {np.cos(np.pi/8)**2:.4f}", verdict(ok1))

below, above = werner_min_pt_eig(1/3 - 1e-6), werner_min_pt_eig(1/3 + 1e-6)
ok2 = below > 0 > above
print(f"Werner: λ_min(ρ^T_B) = {below:+.1e} tại p = 1/3 − 10⁻⁶, {above:+.1e} tại p = 1/3 + 10⁻⁶", verdict(ok2))

A = np.diag([0.5, 0.1])
p_post = np.linalg.norm(A @ plus) ** 2
print(f"Hậu chọn: ‖A|+⟩‖² = {p_post:.2f}", verdict(abs(p_post - 0.13) < 1e-12))"""),
    md("## Cell 3 — E3: Grover là phép quay 2D\n"
       "N = 64, M = 1 và 3 nghiệm, k = 0..12. Xác suất thành công phải bằng sin²((2k+1)θ) với sin θ = √(M/N)."),
    code("""\
N = 64
fig, ax = plt.subplots()
ok = True
for M, c in [(1, "tab:blue"), (3, "tab:orange")]:
    theta = np.arcsin(np.sqrt(M / N))
    ks = np.arange(13)
    sv = np.array([grover_success_sv(N, M, k) for k in ks])
    err = np.max(np.abs(sv - np.sin((2 * ks + 1) * theta) ** 2))
    ok &= err < 1e-10
    kstar = int(np.round(np.pi / (4 * theta) - 0.5))
    ax.plot(ks, sv, "o-", color=c, label=f"M = {M}, k* = {kstar}")
    print(f"M = {M}: sai số so với công thức = {err:.1e}, k* = {kstar}, P(k*) = {sv[kstar]:.4f}")
ax.set_xlabel("số vòng Grover k"); ax.set_ylabel("xác suất thành công"); ax.legend(); plt.show()
print(verdict(ok))"""),
    md("## Cell 4 — Đo trên Aer tại k* (M = 1)\n20 000 shot; tần suất phải nằm trong p ± 3σ."),
    code("""\
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
N, M, n = 64, 1, 6
theta = np.arcsin(np.sqrt(M / N)); kstar = int(np.round(np.pi / (4 * theta) - 0.5))
s = np.ones(N) / np.sqrt(N)
oracle = np.diag([-1.0 if i < M else 1.0 for i in range(N)])
G = (2 * np.outer(s, s) - np.eye(N)) @ oracle
qc = QuantumCircuit(n, n)
qc.h(range(n))
qc.unitary(np.linalg.matrix_power(G, kstar), range(n), label=f"G^{kstar}")
qc.measure(range(n), range(n))
sim, shots = AerSimulator(seed_simulator=SEED), 20000
counts = sim.run(transpile(qc, sim), shots=shots).result().get_counts()
freq = sum(v for b, v in counts.items() if int(b, 2) < M) / shots
p = np.sin((2 * kstar + 1) * theta) ** 2
sig = np.sqrt(p * (1 - p) / shots)
print(f"k* = {kstar}: p = {p:.4f}, tần suất = {freq:.4f}, 3σ = {3 * sig:.4f}", verdict(abs(freq - p) <= 3 * sig))"""),
])

# ===================================================================== Demo 4
save("demo4_bigdata.ipynb", [
    md("# Demo 4 — QSVT cho bài toán dữ liệu lớn\n"
       "**Người nói 3 · 35:10–37:10 (2 phút)**\n\n"
       "Ba cell chạy trực tiếp, mỗi cell dưới vài giây. Mức phân tích: áp đa thức lên ma trận bằng numpy, "
       "đúng như khối trên-trái của mạch QSVT."),
    code(SETUP + """
import csv

def read_csv(name):
    with open(DATA / name, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}"""),
    md("## Cell 2 — E10: hồi quy tuyến tính bằng nghịch đảo giả\n"
       "Ma trận dữ liệu X (12 mẫu × 4 đặc trưng, κ = 4) không vuông, nên nhúng vào H = [[0, X], [Xᵀ, 0]] "
       "(16×16, tức 4 qubit + 1 ancilla). Áp 1/x làm trơn (hàm lẻ, g(0) = 0) lên H: "
       "khối dưới của g(H)[y; 0] tỉ lệ với β = X⁺y."),
    code("""\
reset_rng()
kappa, n, d = 4, 12, 4
X = matrix_with_singular_values(n, d, np.geomspace(1, 1 / kappa, d))
beta_true = rng.normal(size=d)
y = X @ beta_true + 0.05 * rng.normal(size=n); y /= np.linalg.norm(y)
g = g_inv(kappa)
deg = min_degree(g, 1e-3)
out = f_of_A(cheb_poly(g, deg), hermitian_dilation(X)) @ np.concatenate([y, np.zeros(d)])
beta_q = 2 * kappa * out[n:]
beta_c = np.linalg.lstsq(X, y, rcond=None)[0]
rel = np.linalg.norm(beta_q - beta_c) / np.linalg.norm(beta_c)
print(f"bậc đa thức = {deg}, max|g| = {check_bounded(g):.3f}")
print("β QSVT :", np.round(beta_q, 4))
print("β lstsq:", np.round(beta_c, 4))
print(f"sai số tương đối = {rel:.2e}, xác suất hậu chọn = {np.linalg.norm(out)**2:.4f}", verdict(rel < 1e-2))"""),
    md("## Cell 3 — E11: PCA bằng lọc giá trị kỳ dị\n"
       "X 16×16 có 2 thành phần chính (σ = 0,95; 0,8) và nhiễu σ ≤ 0,25. Đa thức chẵn xấp xỉ hàm bước tại τ = 0,5 "
       "cho projector lên 2 thành phần đó. Khe hở δ càng hẹp, bậc càng cao."),
    code("""\
reset_rng()
svals = np.concatenate([[0.95, 0.8], rng.uniform(0, 0.25, 14)])
X = matrix_with_singular_values(16, 16, svals)
_, _, Vt = np.linalg.svd(X); P_true = Vt[:2].T @ Vt[:2]
deltas, degs = [0.3, 0.2, 0.1, 0.05], []
for delta in deltas:
    f = smooth_step(0.5, delta)
    dg = min_degree(f, 1e-2); degs.append(dg)
    P = f_of_A(cheb_poly(f, dg), hermitian_dilation(X))[16:, 16:]
    print(f"δ = {delta:<5} bậc = {dg:>3}   bậc × δ = {dg * delta:4.1f}   sai số projector = {np.linalg.norm(P - P_true, 2):.1e}")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(1 / np.array(deltas), degs, "o-"); ax.set_xlabel("1/δ"); ax.set_ylabel("bậc"); plt.show()
prod = [dg * dl for dg, dl in zip(degs, deltas)]
print(verdict(max(prod) / min(prod) < 1.5))"""),
    md("## Cell 4 — E12: cái giá của việc nạp dữ liệu\n"
       "Block-encoding dựng từ QRAM có hệ số chuẩn hóa ‖A‖_F thay vì ‖A‖, nên số truy vấn bị nhân với ‖A‖_F/‖A‖. "
       "Ma trận đầy đủ hạng: tỉ lệ tăng theo √N; hạng thấp k: không quá √k."),
    code("""\
reset_rng()
for N in (256, 512, 1024):
    full = rng.normal(size=(N, N))
    low = rng.normal(size=(N, 5)) @ rng.normal(size=(5, N))
    r_full = np.linalg.norm(full, "fro") / np.linalg.norm(full, 2)
    r_low = np.linalg.norm(low, "fro") / np.linalg.norm(low, 2)
    print(f"N = {N:>4}: đầy đủ hạng {r_full:5.2f} (√N/2 = {np.sqrt(N)/2:4.1f})   hạng 5 {r_low:4.2f} (≤ √5 = {np.sqrt(5):.2f})")
print(verdict(r_low <= np.sqrt(5) + 1e-9))"""),
    md("## Cell 5 — Dự phòng\nNếu máy chậm: đọc kết quả đã tính sẵn bằng `scripts/make_data.py`."),
    code("""\
for name in ["e10_regression.csv", "e11_pca_degrees.csv", "e12_frobenius_ratio.csv"]:
    t = read_csv(name)
    print(name)
    print("  " + " | ".join(t))
    for r in zip(*t.values()):
        print("  " + " | ".join(r))"""),
])
