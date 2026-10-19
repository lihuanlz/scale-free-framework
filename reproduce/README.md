# reproduce/ — run the paper's numbers

This directory is the bridge between the manuscript and `code/`. It does not
re-implement anything: each check either re-runs an archived script and reads
what it prints, or compares an archived result file with the number in the
paper.

```bash
python reproduce/run_all.py                     # everything
python reproduce/run_all.py 01 03               # selected sections
python reproduce/fetch_data.py --list           # what the 09 block needs
python reproduce/fetch_data.py                  # download it (~430 MB)
```

Exit code is 0 only if every check passes.

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

## What runs from a clean clone

Eight of the 30 scripts in `code/` are executed by this layer: `code04`,
`code10`, `audit_bergmann2010_axis12`, the four adjudication scripts
`code44`/`code44b`/`code45`/`code46`, and `p9_bcd_anchor_audit`. The other 22 are
not executed here; their published outputs are either compared against
`results/` (the ledger block) or not covered at all (see below).

## The adjudication block needs one download

`09_adjudications.py` re-runs five scripts against public archives that are too
large to redistribute. Fetch them once (about 430 MB):

```bash
python reproduce/fetch_data.py --list    # sources and sizes
python reproduce/fetch_data.py           # download into data_external/external
```

Then `python reproduce/run_all.py 09` re-derives the frozen verdicts — P2 not
confirmed, P3 falsified, P4 falsified, P9 α = −0.18224 with n = 581 — instead of
reading them. Without the data the block reports SKIP, not FAIL.

The archives are pinned by DOI: Zenodo 10.5281/zenodo.2755026 (Hansen &
Zechner), 10.5281/zenodo.5836623 (Chavez-Abiega et al.),
`tay-lab/Spatial_NF-kB_Signaling` (Sung et al.) and
`mnikolic7/Scale-invariance-in-early-embryonic-development` (Nikolić et al.).

## What this layer does not cover

Twelve scripts read analysis inputs that were never placed in the repository
(`code/data/…`: hand-digitised source images, the Gillies 2020 supplement, the
GEO extract GSE305057, the P11–P16 working tables) and cannot be re-run from any
clone:

`p10`, `p11`, `p12a_erk_violin_digitize`, `p12a_gerosa_a375_digitize`,
`p12b_egfr_dms_audit`, `p12b_egfr_dms_A5_audit`, `p12b_extended_audit`,
`p12b_final_audit`, `p12b_resistance_zero_direction_audit`,
`p13_mutual_info_audit`, `p13_robustness_recheck`, `p14_shape_decoding_audit`.

Their published results are still checked where they feed the ledger
(`p14`, `p15`, `P12b`), but the inputs would have to be added — or those
scripts rewritten to fetch them — before the runs themselves are reproducible.

`code09`, `code12` and `code13` are also not covered: the first two need more
than 150 s and were never wired in, and `code13_p53_fisher_stratification_S7.py`
is no longer in the tree.

## Output

Every script run writes its stdout to `records/logs/<script>.run.txt`, so a run
of this layer also refreshes the archive of what the code printed.
