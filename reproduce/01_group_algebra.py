# -*- coding: utf-8 -*-
"""Section 1 of the paper: the degeneracy group of the covalent cycle (Eqs. 1-2).

Re-runs code10_asymmetric_Km_degeneracy_group.py and checks the invariance
residuals the paper reports for the four group actions.
"""
from _common import Report


def run():
    rep = Report("01 group algebra")
    out = rep.run_script("code10_asymmetric_Km_degeneracy_group.py", timeout=300)

    rep.contains(out, "group action (a) k1,k2", "action (a) present")
    rep.contains(out, "max|Δu| = 0.000e+00", "pure actions give exactly zero")
    rep.contains(out, "2.220e-16", "mixed action at machine precision")
    rep.contains(out, "1.454e-01", "counterexample moves the curve")
    rep.contains(out, "max relative deviation = 1.04e-14", "closed form holds to 1e-14")
    return rep
