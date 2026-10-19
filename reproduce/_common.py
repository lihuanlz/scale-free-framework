# -*- coding: utf-8 -*-
"""Shared helpers for the reproduce/ layer.

Every check either
  * runs an archived script in code/ and inspects its printed output, or
  * reads an archived result file and compares it with the number in the paper.

Nothing here recomputes with new code: the layer exists to re-run the archived
scripts and to assert that what they print still matches the manuscript.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CODE = REPO / "code"
RESULTS = REPO / "results"
DATA = REPO / "data_external"
LOGS = REPO / "records" / "logs"
LOGS.mkdir(parents=True, exist_ok=True)


class Report:
    def __init__(self, name):
        self.name = name
        self.rows = []          # (status, label, detail)

    # -- assertions ---------------------------------------------------------
    def check(self, ok, label, detail=""):
        self.rows.append(("PASS" if ok else "FAIL", label, detail))
        return ok

    def skip(self, label, detail=""):
        self.rows.append(("SKIP", label, detail))
        return None

    def contains(self, text, needle, label=None):
        return self.check(needle in text, label or f"output contains {needle!r}")

    # -- running archived scripts -------------------------------------------
    def run_script(self, script, timeout=1800, tag=None, args=None):
        """Run code/<script>, archive its stdout under records/logs, return it."""
        path = CODE / script
        if not path.exists():
            self.check(False, f"{script} present", "file missing")
            return ""
        t0 = time.time()
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        cmd = [sys.executable, str(path)] + [str(a) for a in (args or [])]
        cp = subprocess.run(cmd, cwd=str(CODE), env=env,
                            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
        dt = time.time() - t0
        out = cp.stdout or ""
        log = LOGS / f"{(tag or path.stem)}.run.txt"
        log.write_text(
            f"$ python {script}\n# exit {cp.returncode}  wall {dt:.1f}s\n\n{out}\n"
            f"--- stderr (tail) ---\n{(cp.stderr or '')[-4000:]}\n",
            encoding="utf-8")
        self.check(cp.returncode == 0, f"{script} exit code", f"{cp.returncode} in {dt:.1f}s")
        return out

    # -- reading archived results -------------------------------------------
    def json(self, rel):
        p = RESULTS / rel
        self.check(p.exists(), f"results/{rel} present", str(p))
        return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}

    def text(self, rel):
        p = RESULTS / rel
        self.check(p.exists(), f"results/{rel} present", str(p))
        return p.read_text(encoding="utf-8") if p.exists() else ""

    def close(self, a, b, tol, label):
        ok = a is not None and abs(float(a) - float(b)) <= tol
        return self.check(ok, label, f"{a} vs {b} (tol {tol})")


def rule(title):
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def print_report(rep):
    for status, label, detail in rep.rows:
        mark = {"PASS": "  ok  ", "FAIL": " FAIL ", "SKIP": " skip "}[status]
        line = f"[{mark}] {label}"
        if detail:
            line += f"  -- {detail}"
        print(line)
    n_fail = sum(1 for s, _, _ in rep.rows if s == "FAIL")
    n_skip = sum(1 for s, _, _ in rep.rows if s == "SKIP")
    n_pass = sum(1 for s, _, _ in rep.rows if s == "PASS")
    return n_pass, n_fail, n_skip
