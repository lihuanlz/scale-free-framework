# -*- coding: utf-8 -*-
"""Section 11: figures must be legible at printed size.

Each figure is drawn on a canvas wider than the text block, so every label is
scaled down when the PDF places it. This check computes that scale from the
script (figsize) and the LaTeX placement (\\includegraphics width) and fails if
any text would print below 5 pt.
"""
import re
from _common import REPO, Report

TEXTWIDTH_IN = 15.92 / 2.54          # A4, 1 inch margins
MIN_PT = 5.0

FIGURES = {
    "make_fig1_schematic.py": ("fig1_schematic.png", 1.0),
    "make_fig2_pdpc.py": ("fig2_pdpc.png", 1.0),
    "make_fig3.py": ("fig3_pdpc_full.png", 1.0),
    "make_fig4.py": ("fig4_instances.png", 1.0),
    "make_fig5_ledger.py": ("fig5_ledger.png", 1.0),
}


def _canvas_width(text):
    m = re.search(r"figsize\s*=\s*\(([^)]*)\)", text, re.S)
    if not m:
        return None
    body = m.group(1)
    if "MM" in body:
        val = re.search(r"([\d.]+)\s*\*\s*MM", body)
        return float(val.group(1)) / 25.4 if val else None
    val = re.search(r"([\d.]+)", body)
    return float(val.group(1)) if val else None


def run():
    rep = Report("08 figure legibility")
    man = REPO / "manuscript"
    tex = (man / "main.tex").read_text(encoding="utf-8")
    widths = {m.group(2): m.group(1)
              for m in re.finditer(r"\\includegraphics\[width=([^\]]*)\]\{([^}]*)\}", tex)}

    for script, (png, _) in FIGURES.items():
        src = (man / script).read_text(encoding="utf-8")
        w = _canvas_width(src)
        if w is None:
            rep.check(False, f"{script}: figsize found")
            continue
        frac = 1.0
        spec = widths.get(png, "")
        m = re.match(r"([\d.]+)\\textwidth", spec)
        if m:
            frac = float(m.group(1))
        target = TEXTWIDTH_IN * frac
        scale = target / w
        fonts = [float(x) for x in re.findall(r"fontsize\s*=\s*([\d.]+)", src)]
        if not fonts:
            rep.check(False, f"{script}: fonts found")
            continue
        printed = min(fonts) * scale
        rep.check(printed >= MIN_PT, f"{png}: min printed size >= {MIN_PT} pt",
                  f"{min(fonts)} pt x {scale:.2f} = {printed:.2f} pt")
    return rep
