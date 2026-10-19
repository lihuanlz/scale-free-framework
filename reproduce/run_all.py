# -*- coding: utf-8 -*-
"""Run every section check of the framework paper.

    python reproduce/run_all.py            # everything (~9 min with data)\n    python reproduce/run_all.py --quick    # skip the two slow blocks
    python reproduce/run_all.py 01 02      # selected sections

Exit code 0 only if no check failed.
"""
import importlib
import sys
import time

from _common import print_report, rule

SECTIONS = [
    ("01", "01_group_algebra", "Sec. 2-4  degeneracy group of the covalent cycle"),
    ("02", "02_pdpc", "Sec. 4    PdPC static sensor (Theorems 2-4)"),
    ("03", "03_bicoid", "Sec. 5    morphogen anchor (Bergmann + Bicoid)"),
    ("04", "04_wnt", "Sec. 6    Wnt fold-change plateau"),
    ("05", "05_cascade", "Sec. 7    M3R-to-Ca2+ cascade"),
    ("06", "06_ledger", "Sec. 9    prediction ledger"),
    ("07", "07_figures", "Sec. 10   manuscript figures"),
    ("08", "08_figure_legibility", "Sec. 10   figures legible at print size"),
    ("09", "09_adjudications", "Sec. 8    five blind adjudications, re-run"),
    ("10", "10_scripts", "Sec. 12   remaining analysis scripts"),
]


def main(argv):
    quick = "--quick" in argv
    argv = [a for a in argv if a != "--quick"]
    want = set(argv) if argv else None
    if quick and not want:
        want = {"01", "02", "03", "04", "05", "06", "07", "08"}
    totals = [0, 0, 0]
    summary = []
    t_all = time.time()
    for key, modname, title in SECTIONS:
        if want and key not in want:
            continue
        rule(f"{title}   [{key}]")
        mod = importlib.import_module(modname)
        rep = mod.run()
        p, f, s = print_report(rep)
        totals[0] += p
        totals[1] += f
        totals[2] += s
        summary.append((key, title, p, f, s))

    rule("summary")
    print(f"{'section':6s} {'pass':>5s} {'fail':>5s} {'skip':>5s}   title")
    for key, title, p, f, s in summary:
        print(f"{key:6s} {p:5d} {f:5d} {s:5d}   {title}")
    print(f"\n{'total':6s} {totals[0]:5d} {totals[1]:5d} {totals[2]:5d}"
          f"   in {time.time()-t_all:.1f}s")
    return 0 if totals[1] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
