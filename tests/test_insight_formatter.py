
from src.engine.insight_formatter import format_match_insights


def test_formats_pipeline_output():
    pipeline_result = {
        "match_analysis": {
            "team_stats": {
                "Arsenal": {
                    "passes": 10,
                    "completed_passes": 8,
                    "pass_completion_pct": 80.0,
                    "shots": 3,
                    "shots_on_target": 2,
                    "possession_pct": 60.0,
                }
            }
        },
        "key_moments": [
            {
                "minute": 15,
                "team": "Arsenal",
                "description": "Shot on target",
                "review_status": "verified",
                "interpretation": "Recorded significant event.",
            }
        ],
        "review_summary": {
            "total_reviewed": 1,
            "approved": 1,
            "rejected": 0,
        },
    }

    result = format_match_insights(pipeline_result)

    assert result["teams"][0]["team"] == "Arsenal"
    assert result["teams"][0]["pass_completion_pct"] == 80.0
    assert result["timeline"][0]["minute"] == 15
    assert result["review_summary"]["approved"] == 1
    assert result["insight_count"] == 1
