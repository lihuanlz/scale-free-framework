# -*- coding: utf-8 -*-
"""Section 11: the two long-running audits (about 13 minutes together).

Kept out of the default run so that `run_all.py` stays usable; enable with
`python reproduce/run_all.py --slow` or by naming the section: `... 11`.
"""
from _common import RESULTS, Report


def run():
    rep = Report("11 slow audits")
    rep.run_script("code09_nfkB_spike_mode_audit.py", timeout=3600,
                   tag="code09_nfkB_spike_mode_audit")
    rep.check((RESULTS / "NFkB_spike_mode_audit_fig.png").exists(),
              "code09: wrote NFkB_spike_mode_audit_fig.png")
    rep.run_script("code12_nfkB_GLM_prediction_test_switchlike_IkB.py", timeout=3600,
                   tag="code12_nfkB_GLM_prediction_test_switchlike_IkB")
    return rep
