# Project — From quantum foundations to QSVT

Demo code for the 30-minute, 3-speaker talk: QSP, block-encoding, QSVT circuits measured on Qiskit Aer, and the three algorithms rebuilt as polynomials (fixed-point search, Hamiltonian simulation, linear systems) plus the polynomial-method lower bound for OR. Simulator only.

| Path | What it is |
|---|---|
| `src/qsvt_demo.py` | Shared helpers: `qsp`, `find_phases`, `block_encode`, `qsvt_matrix`, `qsvt_circuit`, `min_degree`, `g_inv`, plus helpers for E0, E3–E8 and the big-data experiments E10–E12 |
| `notebooks/demo0_foundations_grover.ipynb` | Demo 0 (speaker 1): Helstrom, Werner threshold, post-selection, Grover as a 2D rotation with an Aer check (E0, E3) |
| `notebooks/demo1_qsp_phases.ipynb` | Demo 1 (speaker 2): zero phases give T_d, the R_Z sign rule, BFGS phase finding, the bound check |
| `notebooks/demo2_qsvt_circuit_measure.ipynb` | Demo 2 (speaker 2): block-encoding, invariant subspaces, QSVT circuit vs numpy, Aer measurement (E7) |
| `notebooks/demo3_algorithms.ipynb` | Demo 3 (backup, not run live): fixed-point vs Grover (E4), QSVT vs Trotter (E5), linear systems (E6), OR lower bound (E8) |
| `notebooks/demo4_bigdata.ipynb` | Demo 4 (speaker 3): regression by pseudo-inverse (E10), PCA by singular value filtering (E11), the ‖A‖_F/‖A‖ cost of loading data (E12) |
| `scripts/make_data.py` | Precomputes the CSV files the notebooks and slides read |
| `scripts/build_notebooks.py` | Regenerates the five notebooks |
| `data/` | Saved phases and experiment results |
| `slides/qsvt-slides.html` / `.pdf` | The 47-slide deck, built with the `educational-dark-design` skill. Plan: `slides/slide-content-spec.md`; rebuild with `slides/make_slide_charts.py` then `slides/build_deck.py` |

## Run

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python scripts\make_data.py
.venv\Scripts\python -m jupyter nbconvert --to notebook --execute --inplace notebooks\demo0_foundations_grover.ipynb notebooks\demo1_qsp_phases.ipynb notebooks\demo2_qsvt_circuit_measure.ipynb notebooks\demo3_algorithms.ipynb notebooks\demo4_bigdata.ipynb
```

Run Demo 1 before Demo 2: Demo 2 loads the phases Demo 1 saves to `data/phases_cos3x_d10.npy`. Every check prints `PASS` or `FAIL`; the only intended `FAIL` is the unscaled 1/x in Demo 3, cell 3.

Conventions: the ancilla is the highest-index qubit, `e^{i phi Z} = RZ(-2 phi)`, seed 1234 everywhere.

Shared tools and reference material are at the repo root: the slide skill in `../.claude/skills/` and the reference book folder `../material/`.
