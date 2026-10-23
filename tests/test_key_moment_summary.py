
from src.agents.key_moments_agent import summarize_key_moments


def test_summary_lists_significant_events():
    moments = [
        {
            "minute": 12,
            "team": "Arsenal",
            "description": "Arsenal records a shot on target",
        },
        {
            "minute": 53,
            "team": "Chelsea",
            "description": "Chelsea responds with a shot on target",
        },
    ]

    summary = summarize_key_moments(moments)

    assert "Identified 2 significant moment(s)" in summary
    assert "12' — Arsenal" in summary
    assert "53' — Chelsea" in summary


def test_summary_handles_no_moments():
    summary = summarize_key_moments([])

    assert "No significant moments" in summary
