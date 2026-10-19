# -*- coding: utf-8 -*-
"""Section 9 of the paper: the prediction ledger's quantitative rows.

Only the rows whose values live in this repository are checked here; the
companion-paper rows belong to their own repositories.
"""
import csv
from _common import RESULTS, Report


def run():
    rep = Report("06 ledger")

    # P14: downstream decoders misread the p53 regime switch
    p14 = rep.json("p14_results.json")
    rep.close(p14.get("frac_sustained_higher_2x"), 0.29034, 1e-4, "29.0% sustained >2x")
    rep.close(p14.get("frac_pulsed_higher_2x"), 0.11095, 1e-4, "11.1% pulsed >2x")
    rep.close(p14.get("frac_within_2x"), 0.49313, 1e-4, "49.3% within 2x")
    rep.check(p14.get("n_induced") == 9103, "n_induced = 9103", str(p14.get("n_induced")))

    # P15: tissue-level coupling
    p15 = rep.json("p15_tcga_results.json")
    luad = next((x for x in p15 if x.get("study", "").startswith("luad")), {})
    wt = luad.get("slopes", {}).get("WT", {})
    rep.close(wt.get("slope"), -0.2548, 1e-3, "LUAD WT slope = -0.255")
    rep.close(wt.get("p"), 0.00583, 1e-4, "LUAD WT p = 0.0058")
    coad = next((x for x in p15 if x.get("study", "").startswith("coadread")), {})
    cwt = coad.get("slopes", {}).get("WT", {})
    rep.check(cwt.get("p", 0) > 0.05, "COADREAD WT not significant", f"p={cwt.get('p'):.3f}")

    # P12b: ABL catalytic efficiency of the resistance mutations
    p = RESULTS / "tumour_chain_P11_P16" / "P12b_abl_catalytic_efficacy.csv"
    rep.check(p.exists(), "P12b ABL table present", str(p))
    if p.exists():
        tab = {r["mutation"]: float(r["fold_vs_WT"]) for r in csv.DictReader(p.open(encoding="utf-8"))}
        rep.close(tab.get("Y253H"), 2.458, 1e-3, "ABL Y253H = 2.46-fold")
        rep.close(tab.get("E255V"), 1.726, 1e-3, "ABL E255V = 1.73-fold")
    return rep
