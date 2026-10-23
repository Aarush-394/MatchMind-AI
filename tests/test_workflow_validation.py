
import pytest

from src.agents.match_workflow import build_match_workflow


@pytest.mark.asyncio
async def test_invalid_event_is_rejected():
    workflow = build_match_workflow()

    invalid_events = [
        {
            "minute": 150,
            "team": "Arsenal",
            "type": "pass",
            "completed": True,
        }
    ]

    with pytest.raises(Exception):
        await workflow.run(invalid_events)
