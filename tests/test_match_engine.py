
from src.engine.match_engine import analyze_match


def test_pass_completion_percentage():
    events = [
        {"team": "Arsenal", "type": "pass", "completed": True},
        {"team": "Arsenal", "type": "pass", "completed": True},
        {"team": "Arsenal", "type": "pass", "completed": False},
    ]

    result = analyze_match(events)

    arsenal = result["team_stats"]["Arsenal"]
    assert arsenal["passes"] == 3
    assert arsenal["completed_passes"] == 2
    assert arsenal["pass_completion_pct"] == 66.7


def test_shots_on_target():
    events = [
        {"team": "Chelsea", "type": "shot", "on_target": True},
        {"team": "Chelsea", "type": "shot", "on_target": False},
    ]

    result = analyze_match(events)

    chelsea = result["team_stats"]["Chelsea"]
    assert chelsea["shots"] == 2
    assert chelsea["shots_on_target"] == 1


def test_possession_percentages():
    events = [
        {
            "team": "Arsenal",
            "type": "possession",
            "duration_seconds": 60,
        },
        {
            "team": "Chelsea",
            "type": "possession",
            "duration_seconds": 40,
        },
    ]

    result = analyze_match(events)

    assert result["team_stats"]["Arsenal"]["possession_pct"] == 60.0
    assert result["team_stats"]["Chelsea"]["possession_pct"] == 40.0


def test_significant_events():
    events = [
        {
            "team": "Arsenal",
            "type": "shot",
            "on_target": True,
            "significant": True,
            "description": "Shot on target",
        },
        {
            "team": "Chelsea",
            "type": "pass",
            "completed": True,
        },
    ]

    result = analyze_match(events)

    assert len(result["significant_events"]) == 1
    assert result["significant_events"][0]["description"] == "Shot on target"


def test_empty_events():
    result = analyze_match(events=[])

    assert result["team_stats"] == {}
    assert result["significant_events"] == []
