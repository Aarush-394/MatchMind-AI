
from src.agents.key_moments_agent import rank_key_moments


def test_shot_on_target_gets_higher_priority():
    moments = [
        {
            "minute": 20,
            "event_type": "pass",
            "evidence": {},
        },
        {
            "minute": 12,
            "event_type": "shot",
            "evidence": {"on_target": True},
        },
        {
            "minute": 30,
            "event_type": "shot",
            "evidence": {"on_target": False},
        },
    ]

    ranked = rank_key_moments(moments)

    assert ranked[0]["priority"] == "High"
    assert ranked[0]["minute"] == 12
    assert ranked[1]["priority"] == "Medium"
    assert ranked[2]["priority"] == "Low"


def test_empty_moments_returns_empty_list():
    assert rank_key_moments([]) == []
