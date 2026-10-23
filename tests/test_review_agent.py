
from src.agents.review_agent import review_key_moments


def test_valid_event_is_approved():
    original_events = [
        {
            "minute": 15,
            "team": "Arsenal",
            "type": "shot",
            "significant": True,
            "description": "Arsenal creates an early shot on target",
        }
    ]

    key_moments = [
        {
            "minute": 15,
            "team": "Arsenal",
            "event_type": "shot",
            "description": "Arsenal creates an early shot on target",
        }
    ]

    result = review_key_moments(key_moments, original_events)

    assert len(result["approved"]) == 1
    assert len(result["rejected"]) == 0
    assert result["approved"][0]["review_status"] == "verified"


def test_altered_description_is_rejected():
    original_events = [
        {
            "minute": 15,
            "team": "Arsenal",
            "type": "shot",
            "description": "Arsenal creates an early shot on target",
        }
    ]

    key_moments = [
        {
            "minute": 15,
            "team": "Arsenal",
            "event_type": "shot",
            "description": "Arsenal scores a goal",
        }
    ]

    result = review_key_moments(key_moments, original_events)

    assert len(result["approved"]) == 0
    assert len(result["rejected"]) == 1
    assert result["rejected"][0]["review_status"] == "rejected"


def test_empty_input():
    result = review_key_moments([], [])

    assert result["approved"] == []
    assert result["rejected"] == []
    assert result["total_reviewed"] == 0
