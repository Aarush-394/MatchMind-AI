
from src.engine.insight_formatter import generate_tactical_takeaways


def test_takeaways_compare_two_teams():
    result = {
        "match_analysis": {
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
    }

    takeaways = generate_tactical_takeaways(result)

    assert len(takeaways) == 3
    assert any("Arsenal" in item for item in takeaways)


def test_takeaways_handle_empty_statistics():
    result = {"match_analysis": {"team_stats": {}}}

    assert generate_tactical_takeaways(result) == [
        "No team statistics are available for analysis."
    ]
