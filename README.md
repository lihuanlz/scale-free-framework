# The price of absolute scale: degeneracy groups, surviving statistics, and the reference economics of cellular signalling

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23402838.svg)](https://doi.org/10.5281/zenodo.23402838)

Framework-paper code, results and manuscript source for:

> H. Li. *The price of absolute scale: degeneracy groups, surviving statistics, and the reference economics of cellular signalling.* (2026), split from the umbrella project [cell-communication-audit](https://github.com/lihuanlz/cell-communication-audit) (archived at Zenodo, doi:10.5281/zenodo.23008824).

## Layout

- `manuscript/` — LaTeX source, compiled PDF, five figure PNGs, and one figure-generation script per figure: `make_fig1_schematic.py` (derived from the umbrella edition `draw_ed_figures.py`, EDFig1 section), `make_fig2_pdpc.py` (renamed copy of `code/make_fig2.py`), `make_fig3.py`, `make_fig4.py`, `make_fig5_ledger.py` (renamed copy of `code/make_fig1.py`).
- `code/` — analysis scripts (ours):
  - *PdPC instance*: code04 (identifiability audit), code10 (asymmetric-Km group), code11 (discrimination map);
  - *additional systems / census*: code06, 08, 09, 12, 15 (NF-κB, Msn2);
  - *blind adjudications P2/P3/P4/P6*: code44/44b/45/46/48;
  - *morphogen instance*: `p9_bcd_anchor_audit.py`, `audit_bergmann2010_axis12.py`;
  - *yeast positive control*: `score_markers_v2_authordata.py`;
  - *cascade instance*: `cascade_audit_gpcr_ca.py`, `p10_gain_confinement_audit.py`;
  - *tumour ledger P11–P16*: `p11_*.py` … `p15_*.py`.
- `results/` — derived outputs (ours): verdict-summary CSVs of the adjudication campaign, anchor-analysis JSONs, cascade results, tumour-chain result JSONs/CSVs, and our own digitisation of Goentoro & Kirschner (2009) Fig. 4F. The two PdPC analysis figures written by `code04` and `code10` also land here.
- `data_external/` — small third-party tables with provenance (`bergmann2010/`, `muzzey2009/`). Large source archives are **not** re-hosted; `data_external/external/README.md` lists the four that are needed by the adjudication scripts and how to point `CELL_EXTERNAL_DATA` at them.
- `reproduce/` — ordered entry points that re-run the archived scripts in the order of the paper and assert that what they print still matches the manuscript. `python reproduce/run_all.py` runs 78 checks in about 25 s.
- `records/logs/` — archived run logs of the analysis scripts, including the captured stdout of the console-only ones.

## Running

Python 3 (numpy/scipy/matplotlib/pandas). Most scripts are self-contained against `results/` and `data_external/`; the per-embryo Bicoid anchor audit and the four adjudication scripts P2/P3/P4 need the third-party archives listed in `data_external/external/README.md`.

To check the paper's numbers end to end:

```bash
python reproduce/run_all.py
```

## Ownership

Code, derived results and manuscript: the author's work product (MIT for code, CC BY 4.0 for text). Third-party data are redistributed only where small and license-clear, always with provenance; large archives are referenced, never copied.

## Companion papers

- *The p53 pulse encoder counts by topological necessity* → [p53-pulse-encoder](https://github.com/lihuanlz/p53-pulse-encoder)
- *Amplitude and midpoint statistics of the same chemotaxis cells demand incompatible receptor models* → [chemotaxis-receptor-layer](https://github.com/lihuanlz/chemotaxis-receptor-layer)
- *The quantitative currency of GPCR bias signalling fails its own algebraic identities* → [gpcr-field-audit](https://github.com/lihuanlz/gpcr-field-audit)
