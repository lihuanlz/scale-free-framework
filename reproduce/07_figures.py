# -*- coding: utf-8 -*-
"""Section 10: the five manuscript figures.

Runs every manuscript/make_fig*.py and checks that it rewrote its PNG. The
scripts are self-contained: they read data_external/ and results/ only.
"""
import subprocess
import sys
import time
from pathlib import Path

from _common import REPO, Report

MAN = REPO / "manuscript"
FIGS = [
    ("make_fig1_schematic.py", "fig1_schematic.png"),
    ("make_fig2_pdpc.py", "fig2_pdpc.png"),
    ("make_fig3.py", "fig3_pdpc_full.png"),
    ("make_fig4.py", "fig4_instances.png"),
    ("make_fig5_ledger.py", "fig5_ledger.png"),
]


def run():
    rep = Report("07 figures")
    for script, png in FIGS:
        p = MAN / script
        if not p.exists():
            rep.check(False, f"{script} present", "missing")
            continue
        before = (MAN / png).stat().st_mtime if (MAN / png).exists() else 0
        t0 = time.time()
        env = dict(__import__("os").environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        cp = subprocess.run([sys.executable, str(p)], cwd=str(MAN), env=env,
                            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900)
        ok = cp.returncode == 0
        rep.check(ok, f"{script} exit code", str(cp.returncode) if not ok else f"{time.time()-t0:.1f}s")
        after = (MAN / png).stat().st_mtime if (MAN / png).exists() else 0
        rep.check(after > before, f"{png} regenerated", f"{after-before:.0f}s newer")
    return rep
