
from collections import defaultdict


def analyze_match(events: list[dict]) -> dict:
    """Calculate basic match statistics from synthetic football events."""

    stats = defaultdict(
        lambda: {
            "passes": 0,
            "completed_passes": 0,
            "shots": 0,
            "shots_on_target": 0,
            "possession_seconds": 0,
        }
    )

    significant_events = []

    for event in events:
        team = event["team"]
        event_type = event["type"]

        if event_type == "pass":
            stats[team]["passes"] += 1

            if event.get("completed", False):
                stats[team]["completed_passes"] += 1

        elif event_type == "shot":
            stats[team]["shots"] += 1

            if event.get("on_target", False):
                stats[team]["shots_on_target"] += 1

        elif event_type == "possession":
            stats[team]["possession_seconds"] += event.get(
                "duration_seconds", 0
            )

        if event.get("significant", False):
            significant_events.append(event)

    result = {}

    for team, values in stats.items():
        total_passes = values["passes"]
        completed_passes = values["completed_passes"]

        result[team] = {
            **values,
            "pass_completion_pct": round(
                completed_passes / total_passes * 100, 1
            ) if total_passes else 0.0,
        }

    total_possession = sum(
        values["possession_seconds"] for values in stats.values()
    )

    for team, values in result.items():
        seconds = values["possession_seconds"]
        values["possession_pct"] = round(
            seconds / total_possession * 100, 1
        ) if total_possession else 0.0

    return {
        "team_stats": result,
        "significant_events": significant_events,
    }
