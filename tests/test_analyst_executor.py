
from src.agents.analyst_executor import generate_local_analysis


def test_local_analysis_uses_match_statistics():
    match_analysis = {
        "team_stats": {
            "Arsenal": {
                "possession_pct": 60.0,
                "shots_on_target": 4,
                "pass_completion_pct": 85.0,
            },
            "Chelsea": {
                "possession_pct": 40.0,
                "shots_on_target": 2,
                "pass_completion_pct": 75.0,
            },
        }
    }

    result = generate_local_analysis(match_analysis)

    assert "Arsenal" in result
    assert "Chelsea" in result
    assert "60.0% possession" in result
    assert "4 shots on target" in result


def test_local_analysis_handles_missing_statistics():
    assert "Insufficient" in generate_local_analysis(
        {"team_stats": {}}
    )
