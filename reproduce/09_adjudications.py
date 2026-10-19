# -*- coding: utf-8 -*-
"""Section 8 of the paper: the five blind adjudications, re-run from scratch.

These are the only scripts that need third-party archives larger than the
repository carries. Run `python reproduce/fetch_data.py` once; without the data
this block reports SKIP rather than FAIL.

The point of the block is that the frozen verdicts are recomputed, not read:
each script is executed against the downloaded archives and its ruling file is
then compared with what the paper reports.
"""
import json
from _common import REPO, RESULTS, Report

EXT = REPO / "data_external" / "external"

RUNS = [
    ("code44_P2_blind_adjudication_amplitude_stratification.py", "code44_ruling.json", "P2"),
    ("code44b_P2_CI_recompute.py", "code44b_CI_unit_table.csv", "P2 CI"),
    ("code45_P3_blind_adjudication_free_statistic_sufficiency.py", "code45_ruling.json", "P3"),
    ("code46_P4_blind_adjudication_ERK_GPCR_KTR.py", "code46_ruling.json", "P4"),
    ("p9_bcd_anchor_audit.py", "p9_bcd_anchor_results.json", "P9"),
]


def _data_present():
    need = ["HansenZechner2021", "Sung2022", "ChavezAbiega2022", "Nikolic2024"]
    return all((EXT / n).exists() for n in need)


def run():
    rep = Report("09 adjudications")
    if not _data_present():
        rep.skip("third-party archives", "run reproduce/fetch_data.py first")
        return rep

    for script, artifact, tag in RUNS:
        rep.run_script(script, timeout=1800, tag=script.replace(".py", ""))
        rep.check((RESULTS / artifact).exists(), f"{tag}: wrote {artifact}")

    p2 = json.loads((RESULTS / "code44_ruling.json").read_text(encoding="utf-8"))
    rep.check(p2.get("overall") is False, "P2: overall not confirmed",
              f"overall={p2.get('overall')}")

    p3 = json.loads((RESULTS / "code45_ruling.json").read_text(encoding="utf-8"))
    rep.check(str(p3.get("overall", "")).startswith("P3 falsified"),
              "P3: falsified", str(p3.get("overall"))[:60])

    p4 = json.loads((RESULTS / "code46_ruling.json").read_text(encoding="utf-8"))
    rep.check(str(p4.get("overall", "")).startswith("P4 falsified"),
              "P4: falsified", str(p4.get("overall"))[:60])

    p9 = json.loads((RESULTS / "p9_bcd_anchor_results.json").read_text(encoding="utf-8"))
    d = p9.get("P9_1", {})
    rep.close(d.get("alpha"), -0.18224, 1e-4, "P9: alpha = -0.18224")
    rep.check(d.get("n") == 581, "P9: n = 581", str(d.get("n")))
    return rep
