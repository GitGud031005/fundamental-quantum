# Slide plan — "From quantum foundations to QSVT", with big data (45 minutes, 3 speakers)

The deck is built with the `educational-dark-design` skill (`.claude/skills/` at the repo root). Content comes from QSVT plan v4 and the 45-minute plan on Claude Docs (tab "Bản 45 phút + Big Data"); every number comes from `data/` and the outputs of the demo notebooks. The bilingual speaker script is in [`speaker-script.md`](speaker-script.md).

- **Length:** 42 minutes of content (four live demos, 8 minutes in total) plus 3 minutes of buffer; Q&A is separate.
- **Language:** English slides (`<html lang="en">`); the speaker script is English with a Vietnamese version of every block.
- **Demos:** run in the notebooks at the ▶ marks. Demo 3 is backup only; its numbers are on slides 30–34.
- **Placeholders to fill:** team name and advisor (slide 1), team email (slide 47).
- **Status column:** kept from the 30-minute deck, changed, or new.

| # | Layout | Speaker | Starts | Key message | Figure / numbers | Status |
|---|---|---|---|---|---|---|
| 1 | cover | 1 | 00:00 | From quantum foundations to QSVT, and what it means for big data | — | changed |
| 2 | bignum | 1 | 00:30 | A 10⁶ × 10⁶ rating matrix has 10¹² entries | — | new |
| 3 | zig4 | 1 | 01:30 | Regression, PCA, recommendation and search are linear algebra | — | new |
| 4 | statement | 1 | 02:30 | Three algorithms, one circuit, swap polynomials | — | kept |
| 5 | toc | 1 | 03:00 | Five chapters, RQ0–RQ4 | — | changed |
| 6 | section | 1 | 03:40 | 01 Foundations | — | kept |
| 7 | table | 1 | 03:50 | What QSVT trains, what it skips | plan section 2 | kept |
| 8 | five | 1 | 04:40 | A1–A4: Dirac, tensors, spectral theorem, SVD, SU(2) | — | new |
| 9 | zig3 | 1 | 05:40 | Three easy-to-miss conventions | — | kept |
| 10 | bullets | 1 | 06:20 | Measuring and post-selecting (A5) | 0.13 | kept |
| 11 | zig4 | 1 | 07:00 | A6–A7: density matrices, partial trace, Werner p > 1/3, Kraus channels | — | new |
| 12 | text2 | 1 | 08:00 | A8: Helstrom 0.854, contraction, error ≤ Tε | — | new |
| 13 | section-alt | 1 | 08:50 | 02 Classic algorithms | — | new |
| 14 | zig4 | 1 | 09:00 | B1–B4: Deutsch–Jozsa, Grover, QFT, phase and amplitude estimation | — | new |
| 15 | figure | 1 | 10:30 | Grover is a 2D rotation (E3) | `e3_grover.png`, 1.7·10⁻¹⁶, Aer 0.9967 | new |
| ▶ | Demo 0 | 1 | 11:00–12:30 | `demo0_foundations_grover.ipynb` | — | new |
| 16 | section | 2 | 13:00 | 03 QSP and QSVT | — | changed |
| 17 | zig2 | 2 | 13:10 | Two signal conventions, W(x) and R(x) | — | new |
| 18 | diagram | 2 | 13:50 | Phases are the dials (QSP theorem) | — | kept |
| 19 | figure | 2 | 15:00 | Zero phases give Chebyshev | `qsp_zero_phase_chebyshev.png` | kept |
| 20 | table | 2 | 15:40 | Degree follows smoothness; check max\|p\| ≤ 1 | 6→48, 27→427, 16→95 | new |
| 21 | five | 2 | 16:40 | Five ways to find phases | — | new |
| ▶ | Demo 1 | 2 | 17:20–19:20 | `demo1_qsp_phases.ipynb` | — | kept, shortened |
| 22 | figure alt | 2 | 19:20 | Demo 1 result | `qsp_phase_fit.png`, 1.97·10⁻⁶ | kept |
| 23 | diagram | 2 | 19:40 | Put A inside a unitary; LCU | — | kept |
| 24 | focus | 2 | 21:00 | RQ1 | — | kept |
| 25 | diagram | 2 | 21:20 | One QSP per eigenvalue; Jordan / cosine–sine for general matrices | — | changed |
| 26 | steps | 2 | 22:50 | From formula to circuit: 1 ancilla, k ancillas, gate order, real part | — | new |
| 27 | figure wide | 2 | 23:30 | The QSVT circuit in Qiskit | `qsvt_circuit.png`, 9.5·10⁻¹⁶ | kept |
| ▶ | Demo 2 | 2 | 24:10–26:40 | `demo2_qsvt_circuit_measure.ipynb` | — | kept |
| 28 | table | 2 | 26:40 | Demo 2 results, handoff | 0.5223 vs 0.5217 | kept |
| 29 | section-alt | 3 | 27:00 | 04 Algorithms | — | kept |
| 30 | figure | 3 | 27:10 | Fixed-point never overshoots (E4) | `e4_fixed_point.png` | kept |
| 31 | figure alt | 3 | 28:20 | Hamiltonian simulation (E5) | `e5_qsvt_vs_trotter.png` | kept |
| 32 | table | 3 | 29:30 | Linear systems: degree vs κ (E6) | — | kept |
| 33 | focus | 3 | 30:30 | A bug we really hit | — | kept |
| 34 | figure | 3 | 30:45 | Grover is optimal (E8) | inline SVG | kept |
| 35 | table | 3 | 31:30 | One table, five results (adds the eigenvalue filter) | — | changed |
| 36 | section | 3 | 32:00 | 05 Big Data | — | new |
| 37 | table | 3 | 32:10 | Big data through QSVT: task, polynomial, quantum and classical cost | — | new |
| 38 | figure | 3 | 33:10 | Regression with QSVT (E10) | inline SVG dilation, 2.2·10⁻³, degree 53 | new |
| 39 | figure alt | 3 | 34:10 | PCA by filtering σ (E11) | `e11_degree_vs_gap.png`, ≈ 5/δ | new |
| ▶ | Demo 4 | 3 | 35:10–37:10 | `demo4_bigdata.ipynb` | — | new |
| 40 | focus | 3 | 37:10 | QSVT counts queries, not the cost of building the block-encoding | — | new |
| 41 | zig3 | 3 | 37:30 | Three traps: loading (‖A‖_F/‖A‖ = 16, E12), reading out, dequantization | — | new |
| 42 | table | 3 | 38:40 | Who wins, and when: classical vs QSVT + QRAM vs dequantized | — | new |
| 43 | bullets | 3 | 39:30 | When QSVT might pay off | — | new |
| 44 | five | 3 | 40:20 | Five questions answered, RQ0–RQ4 | — | changed |
| 45 | bullets | 3 | 41:00 | Limits and next steps | — | changed |
| 46 | text2 | 3 | 41:30 | References | — | new |
| 47 | thanks | 3 | 41:50 | Q&A, repo link | — | kept |

## Build

```powershell
.venv\Scripts\python scripts\make_data.py
.venv\Scripts\python slides\make_slide_charts.py
.venv\Scripts\python slides\build_deck.py
```

`build_deck.py` copies the skill's `assets/starter.html`, inserts `slides/slides-body.html` between the `SLIDES START/END` markers, switches the page to `lang="en"`, embeds the PNGs from `slides/assets/` as data URIs and writes `slides/qsvt-slides.html`. For the PDF, open the HTML in Chrome and print with margins "None" and "Background graphics" ticked, or run headless Chrome with `--print-to-pdf`.
