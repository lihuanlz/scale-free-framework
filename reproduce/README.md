# reproduce/ — run the paper's numbers

This directory is the bridge between the manuscript and `code/`. It does not
re-implement anything: each check either re-runs an archived script and reads
what it prints, or compares an archived result file with the number in the
paper.

```bash
python reproduce/run_all.py          # everything, 25 s on a laptop
python reproduce/run_all.py 01 03    # selected sections
```

Exit code is 0 only if every check passes. Current state: **78 checks, 78 pass,
0 fail, 24 s**.

## Sections

| # | Module | Paper | What is checked |
|---|---|---|---|
| 01 | `01_group_algebra.py` | Sec. 2–4, Eqs. 1–2 | runs `code10`; group-action residuals 0 / 2.2e-16, counterexample 1.45e-1, closed form to 1e-14 |
| 02 | `02_pdpc.py` | Sec. 4, Theorems 2–4, Table 2 | runs `code04` (~25 s); χ 18.87–33.46, CI inflation 2551.92, I = 2.851 / 3.040 bit, zero-order 1.41 / 1.11; asserts the manuscript quotes the measured ratio and not the script's target column |
| 03 | `03_bicoid.py` | Sec. 5, Fig. 4a | runs `audit_bergmann2010_axis12.py`; S = 1.728, P1 5/10, 0/22, posterior 0.889, precision 2.11%, weighted means 1.069→0.955→0.841; reads `p9_bcd_anchor_results.json` for α, CI, λ, n |
| 04 | `04_wnt.py` | Sec. 6, Fig. 4b | reads `fig4F_digitized.csv`; seven points, plateau ±5%, breakdown bracketed 48.6–58.1 mM |
| 05 | `05_cascade.py` | Sec. 7, Fig. 4c | reads `cascade_audit_results.json`; 26 fits, 353 cells, median EC50 0.632, CV 1.161, 32.4-fold |
| 06 | `06_ledger.py` | Sec. 9, Table 4 | reads `p14_results.json`, `p15_tcga_results.json`, `P12b_abl_catalytic_efficacy.csv` |
| 07 | `07_figures.py` | Sec. 10 | runs all five `manuscript/make_fig*.py` and checks each figure is rewritten |

## What this layer does not cover

Five analyses need third-party archives that are not redistributed in this
repository. Their results are archived and checked here, but the scripts cannot
be re-run from a clean clone:

| script | dataset | how to supply it |
|---|---|---|
| `code44`, `code44b` | Hansen & Zechner 2021 | see `data_external/external/README.md` |
| `code45` | Sung et al. 2022 | idem |
| `code46` | Chavez-Abiega et al. 2022 | idem |
| `p9_bcd_anchor_audit.py` | Nikolić et al. per-embryo Bicoid profiles | idem |

Point the environment variable `CELL_EXTERNAL_DATA` at a directory containing
the four dataset folders and the four adjudication scripts run unchanged.

## Output

Every script run writes its stdout to `records/logs/<script>.run.txt`, so a run
of this layer also refreshes the archive of what the code printed.
