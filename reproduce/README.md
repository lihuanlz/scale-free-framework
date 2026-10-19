# reproduce/ — run the paper's numbers

This directory is the bridge between the manuscript and `code/`. Nothing here
re-implements an analysis: each check either re-runs an archived script and
reads what it prints, or compares an archived result file with the number in the
paper.

```bash
python reproduce/run_all.py --quick      # 8 sections, ~30 s, no downloads
python reproduce/fetch_data.py           # ~430 MB, once
python reproduce/run_all.py              # all default sections, ~11 min
python reproduce/run_all.py --slow       # adds the two long audits (~13 min more)
python reproduce/run_all.py 01 03        # selected sections
```

Exit code is 0 only if every check passes. Default run: **131 checks, 131 pass, 0 fail**; with `--slow`, 134.

## Sections

| # | Module | Paper | What is checked |
|---|---|---|---|
| 01 | `01_group_algebra.py` | Sec. 2–4, Eqs. 1–2 | runs `code10`; group-action residuals 0 / 2.2e-16, counterexample 1.45e-1, closed form to 1e-14 |
| 02 | `02_pdpc.py` | Sec. 4, Theorems 2–4, Table 2 | runs `code04`; χ 18.87–33.46, CI inflation 2551.92, I = 2.851 / 3.040 bit; asserts the manuscript quotes the measured ratio, not the script's target column |
| 03 | `03_bicoid.py` | Sec. 5, Fig. 4a | runs `audit_bergmann2010_axis12.py`; S = 1.728, P1 5/10, 0/22, posterior 0.889, precision 2.11% |
| 04 | `04_wnt.py` | Sec. 6, Fig. 4b | reads `fig4F_digitized.csv`; seven points, plateau ±5%, breakdown bracketed 48.6–58.1 mM |
| 05 | `05_cascade.py` | Sec. 7, Fig. 4c | runs `cascade_audit_gpcr_ca.py`, then reads its JSON; 26 fits, 353 cells, EC50 0.632, CV 1.161, 32.4-fold |
| 06 | `06_ledger.py` | Sec. 9, Table 4 | reads `p14_results.json`, `p15_tcga_results.json`, `P12b_abl_catalytic_efficacy.csv` |
| 07 | `07_figures.py` | Sec. 10 | runs all five `manuscript/make_fig*.py` |
| 08 | `08_figure_legibility.py` | Sec. 10 | derives each figure's scale from its figsize and `\includegraphics` width; fails below 5 pt printed |
| 09 | `09_adjudications.py` | Sec. 8 | re-runs P2, P2-CI, P3, P4 and P9 against the fetched archives and checks the frozen verdicts |
| 10 | `10_scripts.py` | Sec. 12 | executes the remaining 19 analysis scripts and checks their artefacts |
| 11 | `11_slow.py` | Sec. 12 | `code09` and `code12`, about 13 minutes together; only with `--slow` |

## Coverage

**All 30 scripts in `code/` are executed**, 28 of them in the default run:

- 01–02: `code10`, `code04`
- 03: `audit_bergmann2010_axis12`
- 05: `cascade_audit_gpcr_ca`
- 09: `code44`, `code44b`, `code45`, `code46`, `p9_bcd_anchor_audit`
- 10: `code06`, `code08`, `code11`, `code13`, `code15`, `code48`, `p10`, `p11`,
  `p12a_erk_violin_digitize`, `p12b_egfr_dms_audit`, `p12b_egfr_dms_A5_audit`,
  `p12b_extended_audit`, `p12b_final_audit`,
  `p12b_resistance_zero_direction_audit`, `p13_mutual_info_audit`,
  `p13_robustness_recheck`, `p14_shape_decoding_audit`,
  `p15_tcga_decoupling_audit`, `score_markers_v2_authordata`
- 11 (`--slow`): `code09`, `code12`

## Data

Two directories of inputs are not in git, because together they are about
800 MB:

- `data_external/external/` — the four public archives fetched by
  `fetch_data.py` (Zenodo 10.5281/zenodo.2755026 and 10.5281/zenodo.5836623,
  `tay-lab/Spatial_NF-kB_Signaling`, `mnikolic7/Scale-invariance-…`).
- `data_external/analysis_inputs/` — the working tables and digitised source
  images the tumour-line and p53 scripts read. `code/data` is a junction to it,
  so every script keeps its original `HERE/data/...` path.

Both are described in `data_external/external/README.md` and
`data_external/analysis_inputs/README.md`.

## Output

Every script run writes its stdout to `records/logs/<script>.run.txt`, so a run
of this layer also refreshes the archive of what the code printed.
