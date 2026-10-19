# -*- coding: utf-8 -*-
"""Section 12: every remaining analysis script, executed.

This block does not re-check values (the ledger block does that); it checks that
each script still runs from the repository and writes the artefact it is
supposed to write. code09 and code12 are excluded: both need more than seven
minutes and are listed in the README as not covered.
"""
from _common import REPO, RESULTS, Report

EXT = REPO / "data_external" / "external"

RUNS = [
    ("code06_nfkB_negative_feedback_oscillator_audit.py", None, "code06_nfkB_audit_fig.png"),
    ("code08_msn2_excitable_frequency_encoding.py", None, "code08_msn2_frequency_fig.png"),
    ("code11_discrimination_map_v09.py", None, "discrimination_map_v09_experimental_points.png"),
    ("code15_nfkB_saturation_transient_test.py", None, "code15_saturation_transient_test.png"),
    ("code48_P6_blind_adjudication_FCD_attribution.py", EXT / "Wang2022", "code48_ruling.json"),
    ("p10_gain_confinement_audit.py", None, "p10_gain_confinement_results.json"),
    ("p11_counting_law_cross_cellline_audit.py", None, None),
    ("p12a_erk_violin_digitize.py", None, None),
    ("p12b_egfr_dms_audit.py", None, "p12b_egfr_dms_results.json"),
    ("p12b_egfr_dms_A5_audit.py", None, "p12b_egfr_dms_A5_results.json"),
    ("p12b_extended_audit.py", None, None),
    ("p12b_final_audit.py", None, None),
    ("p12b_resistance_zero_direction_audit.py", None, None),
    ("p13_mutual_info_audit.py", None, "p13_mi_results.json"),
    ("p13_robustness_recheck.py", None, "p13_robustness.json"),
    ("p14_shape_decoding_audit.py", None, "p14_results.json"),
    ("p15_tcga_decoupling_audit.py", None, "p15_tcga_results.json"),
    ("score_markers_v2_authordata.py", None, None),
]


def run():
    rep = Report("10 remaining scripts")
    if not (EXT / "Wang2022").exists():
        rep.skip("code48", "run reproduce/fetch_data.py first (Wang2022)")
    for script, arg, artifact in RUNS:
        if script.startswith("code48") and not (EXT / "Wang2022").exists():
            continue
        rep.run_script(script, timeout=1200, tag=script.replace(".py", ""),
                       args=[arg] if arg else None)
        if artifact:
            rep.check((RESULTS / artifact).exists(), f"{script.split('_')[0]}: wrote {artifact}")
    return rep
