# -*- coding: utf-8 -*-
"""Section 6 of the paper: the Wnt fold-change plateau.

The source study publishes no machine-readable supplement, so the seven points
in results/fig4F_digitized.csv are the archive of record for Fig. 4b.
"""
import csv
from _common import RESULTS, Report

PLATEAU = {7.2: 0.964, 20.8: 1.040, 41.3: 1.021, 48.6: 0.983}
BREAKDOWN = {58.1: 0.605, 70.1: 0.268, 82.0: 0.246}


def run():
    rep = Report("04 wnt")
    p = RESULTS / "fig4F_digitized.csv"
    rep.check(p.exists(), "results/fig4F_digitized.csv present", str(p))
    if not p.exists():
        return rep
    rows = list(csv.DictReader(p.open(encoding="utf-8")))
    rep.check(len(rows) == 7, "seven digitised points", str(len(rows)))
    got = {float(r["LiCl_mM"]): float(r["fold_change"]) for r in rows}

    for k, v in PLATEAU.items():
        rep.check(k in got and abs(got[k] - v) < 0.002, f"plateau point {k} mM = {v}", f"{got.get(k)}")
    for k, v in BREAKDOWN.items():
        rep.check(k in got and abs(got[k] - v) < 0.002, f"breakdown point {k} mM = {v}", f"{got.get(k)}")

    plat = [got[k] for k in PLATEAU if k in got]
    rep.check(max(abs(x - 1) for x in plat) <= 0.05, "plateau inside +-5%",
              f"max deviation {max(abs(x-1) for x in plat):.3f}")
    rep.check(48.6 in got and 58.1 in got, "breakdown bracketed by 48.6 and 58.1 mM")
    rep.check(7.2 <= min(got) and max(got) <= 82.0, "range 7-82 mM", f"{min(got)}-{max(got)}")
    return rep
