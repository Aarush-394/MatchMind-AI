
from src.utils.validation import validate_match_events


def test_valid_events():
    events = [
        {"minute": 10, "team": "Arsenal", "type": "pass", "completed": True},
        {
            "minute": 20,
            "team": "Chelsea",
            "type": "possession",
            "duration_seconds": 60,
        },
    ]

    assert validate_match_events(events) == []


def test_unsupported_event_type():
    events = [{"team": "Arsenal", "type": "goalkeeper_magic"}]

    errors = validate_match_events(events)

    assert any("unsupported event type" in error for error in errors)


def test_negative_possession_duration():
    events = [
        {
            "team": "Arsenal",
            "type": "possession",
            "duration_seconds": -10,
        }
    ]

    errors = validate_match_events(events)

    assert any("non-negative" in error for error in errors)


def test_invalid_minute():
    events = [{"minute": 150, "team": "Arsenal", "type": "pass"}]

    errors = validate_match_events(events)

    assert any("minute must be an integer" in error for error in errors)
