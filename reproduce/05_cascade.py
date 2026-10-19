# -*- coding: utf-8 -*-
"""Section 7 of the paper: the M3R-to-Ca2+ cascade (Fig. 4c).

The per-cell peak tables are third-party (Keshelava et al. 2018); the archived
per-experiment fits and their summary are what the paper quotes.
"""
import statistics as st
from _common import Report


def run():
    rep = Report("05 cascade")
    rep.run_script("cascade_audit_gpcr_ca.py", timeout=900)

    d = rep.json("cascade_audit_results.json")
    ep = d.get("exp_params", {})
    rep.check(len(ep) == 26, "26 per-experiment fits", str(len(ep)))
    rep.check(d.get("n_cells") == 353, "353 cells with complete 7x5 matrices", str(d.get("n_cells")))

    ec = [v["ec50"] for v in ep.values()]
    med = st.median(ec)
    cv = st.pstdev(ec) / st.mean(ec)
    fold = max(ec) / min(ec)
    rep.close(med, 0.6323, 0.001, "median EC50 = 0.632 uM")
    rep.close(cv, 1.1608, 0.005, "CV = 1.161")
    rep.close(fold, 32.40, 0.1, "32.4-fold range")
    rep.close(min(ec), 0.15940, 1e-4, "lowest EC50 = 0.159 uM")
    rep.close(max(ec), 5.1652, 1e-4, "highest EC50 = 5.165 uM")

    wc = d.get("within_cell_CV", [])
    ac = d.get("across_cell_CV", [])
    rep.check(len(wc) == 7 and len(ac) == 7, "seven dose levels", f"{len(wc)}/{len(ac)}")
    rep.check(min(wc) < 0.06 and max(ac) > 0.28, "within-cell CV below across-cell CV",
              f"{min(wc):.3f} vs {max(ac):.3f}")
    return rep
