
import pytest

from src.personalization.match_briefing import build_team_briefing


def test_build_team_briefing():
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

    moments = [
        {
            "minute": 12,
            "team": "Arsenal",
            "description": "Shot on target",
            "review_status": "verified",
        },
        {
            "minute": 53,
            "team": "Chelsea",
            "description": "Shot on target",
            "review_status": "verified",
        },
    ]

    briefing = build_team_briefing(
        "Arsenal", match_analysis, moments
    )

    assert briefing["team"] == "Arsenal"
    assert briefing["statistics"]["possession_pct"] == 60.0
    assert len(briefing["key_moments"]) == 1
    assert "60.0% possession" in briefing["summary"]


def test_unknown_team_raises_error():
    with pytest.raises(ValueError, match="No statistics available"):
        build_team_briefing(
            "Liverpool",
            {"team_stats": {"Arsenal": {}}},
            [],
        )
