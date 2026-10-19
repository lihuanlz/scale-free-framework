# -*- coding: utf-8 -*-
"""Section 5 of the paper: the morphogen anchor.

Two independent checks.
  * audit_bergmann2010_axis12.py re-reads data_external/bergmann2010 and prints
    the scaling table the paper quotes (Sec. 5, Fig. 4a).
  * results/p9_bcd_anchor_results.json holds the per-embryo anchor fit; the
    per-embryo Bicoid profiles themselves are third-party and not re-hosted.
"""
from _common import Report


def run():
    rep = Report("03 bicoid")

    out = rep.run_script("audit_bergmann2010_axis12.py", timeout=300)
    rep.contains(out, "1.728", "anterior median S = 1.728")
    rep.contains(out, "5/10", "P1: 5 of 10 with the 68% interval excluding unity")
    rep.contains(out, "0/22", "4x mid-embryo: 0 of 22 hyper-scaling by CI")
    rep.contains(out, "0.889", "posterior tail median S = 0.889 (>56% EL, n=36)")
    rep.contains(out, "2.11% EL", "precision median 2.11% embryo length")
    for v in ("1.069", "0.955", "0.841"):
        rep.contains(out, v, f"confidence-weighted mean S = {v}")

    j = rep.json("p9_bcd_anchor_results.json")
    p = j.get("P9_1", {})
    rep.close(p.get("alpha"), -0.18224, 1e-4, "alpha = -0.18224")
    rep.close(p.get("se"), 0.14333, 1e-4, "se = 0.14333")
    rep.close(p.get("ci95", [None, None])[0], -0.47584, 1e-4, "CI lower = -0.4758")
    rep.close(p.get("ci95", [None, None])[1], 0.10945, 1e-4, "CI upper = +0.1095")
    rep.close(p.get("median_lambda_um"), 87.6413, 1e-3, "median lambda = 87.64 um")
    rep.close(p.get("theil_sen"), -0.19873, 1e-4, "Theil-Sen = -0.1987")
    rep.check(p.get("n") == 581, "n = 581 embryos", str(p.get("n")))
    return rep
