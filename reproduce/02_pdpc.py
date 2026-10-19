# -*- coding: utf-8 -*-
"""Section 4 of the paper: the PdPC static sensor (Theorems 2-4, Fig. 2-3).

Re-runs code04_pdpc_identifiability_audit.py (~15 s) and checks the numbers that
appear in Table 2 and in the text: condition number, confidence inflation,
mutual information and the closed-form Hill agreement.
"""
import re
from _common import REPO, Report


def run():
    rep = Report("02 pdpc")
    out = rep.run_script("code04_pdpc_identifiability_audit.py", timeout=900)

    # group actions on the curve family
    rep.contains(out, "0.000e+00", "pure group actions give zero")
    rep.contains(out, "2.220e-16", "mixed action at machine precision")

    # [T2] shape condition numbers across kappa
    block = out.split("[T2]")[1].split("[T3")[0] if "[T2]" in out else ""
    chis = [float(x) for x in re.findall(r"\n\s+[\d.]+\s+([\d.]+)\s+[\d.eE+-]+\s", block)]
    if chis:
        rep.check(abs(min(chis) - 18.87) < 0.05, "chi_shape min = 18.87", f"{min(chis)}")
        rep.check(abs(max(chis) - 33.46) < 0.05, "chi_shape max = 33.46", f"{max(chis)}")
    else:
        rep.check(False, "chi_shape parsed", "no rows in [T2]")

    # [T3b] measured confidence inflation at kappa = 0.001
    rep.contains(out, "2551.92", "CI inflation 2551.92 (Table 2)")
    tex = (REPO / "manuscript" / "main.tex").read_text(encoding="utf-8")
    rep.check("2552" in tex, "manuscript quotes the measured ratio 2552",
              "Table 2 must carry the ratio column, not the script's target")
    body = tex.split(r"\bibitem")[0]
    rep.check("2920" not in body, "body does not quote the target column 2920",
              "the only 2920 left in the file is inside a reference DOI")

    # [T4] mutual information
    rep.contains(out, "2.851", "I = 2.851 bit at kappa = 0.1")
    rep.contains(out, "3.040", "I = 3.040 bit at kappa = 3")
    rep.contains(out, "I_narrow=1.41, I_wide=1.11", "zero-order limit 1.41 / 1.11 bit")
    return rep
