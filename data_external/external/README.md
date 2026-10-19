# data_external/external — third-party archives, not redistributed

Four analyses in `code/` read public single-cell or per-embryo archives that are
too large to ship here (about 1.3 GB in total) and are already published with
their own DOIs. Download them, keep the folder names below, and point
`CELL_EXTERNAL_DATA` at the parent directory:

```bash
export CELL_EXTERNAL_DATA=/path/to/external      # POSIX
set CELL_EXTERNAL_DATA=D:\path\to\external       # Windows
```

Default when the variable is unset: this directory.

| Folder | Dataset | Source | Used by |
|---|---|---|---|
| `HansenZechner2021/` | Msn2 promoter dynamics, 2018 data release | Hansen & Zechner, *Mol. Syst. Biol.* 17, e9821 (2021), doi:10.15252/msb.20209821 | `code44`, `code44b` |
| `Sung2022/` | NF-κB sequential-stimulation grids (four `.mat` files) | Sung et al. (2022) | `code45` |
| `ChavezAbiega2022/` | ERK/Akt KTR trajectories under GPCR stimulation | Chavez-Abiega et al., *J. Cell Sci.* 135, jcs259685 (2022), doi:10.1242/jcs.259685 | `code46` |
| `Nikolic2023/` | per-embryo Bicoid profiles, 581 embryos | Nikolić et al., *PNAS* 121, e2403265121 (2024), doi:10.1073/pnas.2403265121 | `p9_bcd_anchor_audit.py` |

The expected layout is exactly the folder names above; individual scripts state
the subdirectory they expect (for example `HansenZechner2021/2018_DataForPaper`).

The result files these scripts produce are archived in `results/`, and the
values they contain are checked by `reproduce/03_bicoid.py` and by the ledger
section, so every number quoted in the paper is verifiable without the raw data.

Two archives that *are* shipped, because they are small enough to redistribute
under their licences:

- `data_external/bergmann2010/` — Datasets S1 and S2 of Morton de Lachapelle &
  Bergmann, *Mol. Syst. Biol.* 6, 351 (2010).
- `data_external/muzzey2009/` — author supplementary workbook `mmc2.xls`, plus
  `mmc2.xlsx` (same workbook re-saved so pandas can read it) and the digitised
  glycerol arms.
