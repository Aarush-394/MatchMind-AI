
from src.engine.match_report import build_match_report


def test_build_match_report():
    result = {
        "match_analysis": {
            "team_stats": {
                "Arsenal": {"possession_pct": 60.0},
                "Chelsea": {"possession_pct": 40.0},
            }
        },
        "analyst_analysis": "Arsenal recorded more possession.",
        "key_moments_summary": "Identified 1 significant moment.",
        "key_moments": [{"minute": 12, "team": "Arsenal"}],
        "review_summary": {
            "total_reviewed": 1,
            "approved": 1,
            "rejected": 0,
        },
        "workflow_trace": [
            "Input Validation",
            "Match Statistics",
            "Analyst Interpretation",
            "Key Moment Identification",
            "Evidence Review",
        ],
    }

    report = build_match_report(result)

    assert report["teams"]["Arsenal"]["possession_pct"] == 60.0
    assert report["analyst_analysis"] == (
        "Arsenal recorded more possession."
    )
    assert len(report["key_moments"]) == 1
    assert report["verification"]["approved"] == 1
    assert len(report["workflow_trace"]) == 5
    assert report["key_moments"][0]["priority"] == "Low"