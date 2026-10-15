# Third-party data provenance

## Shipped here (small, license-clear)

| Folder | Source | Terms |
|---|---|---|
| `bergmann2010/` | Morton de Lachapelle & Bergmann, *Mol. Syst. Biol.* 6, 351 (2010), supplementary Datasets S1/S2 (per-boundary precision and scaling tables, PMC2858443) | Open-access supplementary (CC BY). Parsed verbatim; row-level correspondence asserted before analysis. |
| `muzzey2009/mmc2.xls` | Muzzey, Gómez-Uribe, Mettetal & van Oudenaarden, *Cell* 138, 160–171 (2009), supplementary numerical tables (PMC3109981) | Author supplementary data. Only the glycerol arms of our analysis rely on figure digitisation (documented in the manuscript Methods). |

## Our own digitisation (ours, included in `results/`)

| File | Basis |
|---|---|
| `results/fig4F_digitized.csv` | Digitised by us from Goentoro & Kirschner, *Mol. Cell* 36, 872–881 (2009), Fig. 4F (PMC2921914); registered precision ±0.05 fold-change, ±2 mM. The source study provides no machine-readable data. |

## Referenced but not re-hosted (large archives)

| Source | Used for | Access |
|---|---|---|
| Nikolić et al. scale-invariance repository (arXiv:2312.17684); per-embryo Bicoid profiles of Liu et al., *PNAS* 110, 6724–6729 (2013) | P9 anchor audit (581 embryos) | Public repository; download per the repository README |
| Gregor et al., *PNAS* 102, 18403–18407 (2005) | cross-species λ/L consistency | Publisher site |
| Gregor et al., *Cell* 130, 153–164 (2007); Petkova et al., *Cell* 176, 844–855 (2019) | per-embryo wild-type resources (registered tensions) | Publisher sites |
| Cheung et al., *Development* 141, 124–135 (2014) | large-embryo retuning arm | Publisher site |
| Chavez-Abiega et al., *J. Cell Sci.* 135, jcs259685 (2022) KTR archive (~786 MB) | P4 adjudication, P10 confinement test | Authors' public archive |
| Wang et al., *Cell Rep.* 40, 111159 (2022) NF-κB sequential-stimulation archive (~54 MB) | P6 adjudication, P10 confinement test | Authors' public archive |
| Keshelava et al., *Nat. Commun.* 9, 876 (2018) Suppl. Data 3 | cascade instance (`cascade_audit_gpcr_ca.py`) | Mirrored in the companion repo [gpcr-field-audit](https://github.com/lihuanlz/gpcr-field-audit) (`data_external/keshelava2018/`) |
| TCGA PanCanAtlas 2018 (via cBioPortal) | P15 tissue-level decoupling | cBioPortal public export |
| GSE305057 (EGFR saturation mutagenesis) | P12b A5 arm | GEO |
| Gillies et al., *Mol. Syst. Biol.* 16, e9518 (2020), Source Data Figs 2 and 6 (PMC7569415) | P13 channel-capacity audit | Publisher supplementary |
| Liu et al. (EVER), *Commun. Biol.* 3, 30 (2020), Supplementary Data 1 (PMC6952392) | P12b ABL catalytic axis | Publisher supplementary |
| Jimenez-Asins et al., *Mol. Syst. Biol.* 18, e10588 (2022), RNA-seq TPM + TMT proteomics | P14 shape decoding | Authors' public repository (`albajimenezasins/Proteomics_MSB_2022`) |
| Finzel Pérez, A., PhD thesis, Freie Universität Berlin (2016), Fig. 30 | P11 digitised counting-law arms | Institutional repository (refubium fub188/7115) |
| Stewart-Ornstein & Lahav, *Sci. Signal.* 10, eaah6671 (2017) (PMC5504473) | P11 per-line periodicity / ATM IC50 / γH2AX arms | Publisher site |
| Moore et al., *Cell Syst.* 15, 628–638 (2024) FRET archive, Dryad doi:10.5061/dryad.nvx0k6dzz | P7 adjudication | Mirrored CC0 in [chemotaxis-receptor-layer](https://github.com/lihuanlz/chemotaxis-receptor-layer) |

All verdicts in `results/` are our own derived work product.
