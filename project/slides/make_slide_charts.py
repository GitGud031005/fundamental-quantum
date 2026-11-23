"""Charts for the QSVT deck, drawn in the Educational Dark palette (navy canvas).

Run from the project folder:  python slides/make_slide_charts.py
Reads data/ (run scripts/make_data.py and Demo 1 first) and writes slides/assets/*.png.
"""
import csv
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import qsvt_demo as q  # noqa: E402

DATA = ROOT / "data"
OUT = ROOT / "slides" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

NAVY, CYAN, BLUE, GREY, WHITE = "#0D1030", "#79E0FF", "#0F5AFF", "#C2C2C2", "#FFFFFF"
plt.rcParams.update({
    "font.size": 15, "figure.facecolor": NAVY, "axes.facecolor": NAVY, "savefig.facecolor": NAVY,
    "axes.edgecolor": GREY, "axes.labelcolor": WHITE, "xtick.color": GREY, "ytick.color": GREY,
    "text.color": WHITE, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": False,
    "legend.frameon": False,
})


def read(name):
    with open(DATA / name, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    return {k: np.array([r[k] for r in rows]) for k in rows[0]}


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / f"{name}.png", dpi=200)
    plt.close(fig)
    print("wrote slides/assets/" + name + ".png")


# 1. zero phases give T_d
xs = np.linspace(-1, 1, 401)
fig, ax = plt.subplots(figsize=(7.2, 4.2))
for d, c in zip([3, 6, 9], [CYAN, BLUE, WHITE]):
    P = np.array([q.qsp(np.zeros(d + 1), x, "Wx")[0, 0].real for x in xs])
    ax.plot(xs, P, color=c, lw=2.6, label=f"d = {d}: T{chr(0x2080 + d)}(x)")
ax.set_xlim(-1, 1); ax.set_ylim(-1.1, 1.1); ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_xlabel("x"); ax.set_ylabel("P(x) with all phases = 0")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize=13)
save(fig, "qsp_zero_phase_chebyshev")

# 2. phase finding fit
phis = np.load(DATA / "phases_cos3x_d10.npy")
f1 = lambda x: 0.8 * np.cos(3 * x)
ReP = np.array([q.qsp(phis, x)[0, 0].real for x in xs])
fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(xs, f1(xs), color=BLUE, lw=9, solid_capstyle="round", label="target 0.8·cos(3x)")
ax.plot(xs, ReP, color=CYAN, lw=2, label="Re P(x) from 11 phases")
ax.set_ylim(-1, 1.1); ax.set_xlabel("x"); ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.legend(loc="lower center", ncol=2, fontsize=13, bbox_to_anchor=(0.5, -0.02))
save(fig, "qsp_phase_fit")

# 3. QSVT circuit
q.reset_rng()
A = q.random_hermitian(4, scale=1.1)
qc = q.qsvt_circuit(A, phis)
style = {"backgroundcolor": NAVY, "textcolor": WHITE, "linecolor": GREY, "gatefacecolor": BLUE,
         "gatetextcolor": WHITE, "subtextcolor": WHITE,
         "displaycolor": {"rz": [BLUE, WHITE], "unitary": [CYAN, NAVY]}}
fig = qc.draw("mpl", fold=-1, style=style, scale=0.9)
fig.savefig(OUT / "qsvt_circuit.png", dpi=200, bbox_inches="tight")
plt.close(fig)
print("wrote slides/assets/qsvt_circuit.png")

# 4. E4 fixed point vs Grover
e4 = read("e4_success.csv")
a = e4["a"].astype(float)
w, delta, L, k = float(e4["w"][0]), float(e4["delta"][0]), int(e4["L"][0]), int(e4["k_grover"][0])
fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.axvspan(w, 1, color=BLUE, alpha=0.22, lw=0)
ax.semilogx(a, e4["grover"].astype(float), color=GREY, lw=1.6, label=f"Grover, k = {k}")
ax.semilogx(a, e4["fixed_point"].astype(float), color=CYAN, lw=3, label=f"fixed-point, L = {L}")
ax.axhline(1 - delta ** 2, color=WHITE, ls="--", lw=1)
ax.text(1.2e-3, 1 - delta ** 2 + 0.04, "1 − δ² = 0.99", color=WHITE, fontsize=13)
ax.text(0.22, 1.1, "a ≥ w = 0.05", color=WHITE, fontsize=13, ha="center")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=13)
ax.set_ylim(0, 1.2); ax.set_xlabel("a (fraction of solutions, log scale)"); ax.set_ylabel("success probability")
save(fig, "e4_fixed_point")

# 5. E5 QSVT vs Trotter
e5 = read("e5_degrees.csv")
t = e5["t"].astype(float)
fig, ax = plt.subplots(figsize=(7.2, 4.2))
for key, c, label in [("trotter1_steps", GREY, "Trotter, 1st order"), ("trotter2_steps", BLUE, "Trotter, 2nd order"),
                      ("qsvt_degree_1e-3", CYAN, "QSVT")]:
    y = e5[key].astype(float)
    ax.loglog(t, y, "o-", color=c, lw=2.6, ms=7)
    ax.text(t[-1] * 1.12, y[-1], f"{label}\n{int(y[-1]):,}", color=c, fontsize=13, va="center")
ax.set_xlim(0.8, 110); ax.set_xlabel("simulation time t"); ax.set_ylabel("queries / steps")
ax.minorticks_off()
save(fig, "e5_qsvt_vs_trotter")

# 6. E3 Grover rotation, N = 64
e3 = read("e3_grover.csv")
fig, ax = plt.subplots(figsize=(7.2, 4.2))
for M, c in [("1", CYAN), ("3", BLUE)]:
    sel = e3["M"] == M
    k = e3["k"][sel].astype(int)
    ax.plot(k, e3["formula"][sel].astype(float), color=c, lw=1.2, alpha=0.6)
    ax.plot(k, e3["statevector"][sel].astype(float), "o", color=c, ms=7, label=f"M = {M}")
ax.set_xlabel("Grover iterations k"); ax.set_ylabel("success probability")
ax.set_ylim(0, 1.08); ax.set_xticks(range(0, 13, 2))
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize=13)
save(fig, "e3_grover")

# 7. E11 degree vs gap
e11 = read("e11_pca_degrees.csv")
inv = 1 / e11["delta"].astype(float)
deg = e11["degree"].astype(int)
fig, ax = plt.subplots(figsize=(7.2, 4.2))
ax.plot(inv, deg, "o-", color=CYAN, lw=2.6, ms=8)
for x, y, d in zip(inv, deg, e11["delta"]):
    ax.text(x + 0.4, y - 7, f"δ = {d}", color=WHITE, fontsize=13)
ax.set_xlabel("1/δ  (narrower gap between signal and noise →)"); ax.set_ylabel("polynomial degree")
ax.set_xlim(0, 23); ax.set_ylim(0, 110)
save(fig, "e11_degree_vs_gap")
