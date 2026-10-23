
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "synthetic" / "rich_sample_match.json"
)


def generate_events() -> list[dict]:
    events = []

    # Generate fictional passing events across both halves.
    for minute in range(1, 86, 3):
        team = "Arsenal" if (minute // 3) % 2 == 0 else "Chelsea"

        # Passing completion varies deterministically by team and minute.
        completed = (minute + len(team)) % 5 != 0

        events.append({
            "minute": minute,
            "team": team,
            "type": "pass",
            "completed": completed,
        })

    # Fictional shots with explicitly recorded outcomes.
    shots = [
        {
            "minute": 12,
            "team": "Arsenal",
            "on_target": True,
            "significant": True,
            "description": "Arsenal records an early shot on target",
        },
        {
            "minute": 24,
            "team": "Chelsea",
            "on_target": False,
            "significant": False,
            "description": "Chelsea attempts a shot off target",
        },
        {
            "minute": 38,
            "team": "Arsenal",
            "on_target": True,
            "significant": True,
            "description": "Arsenal creates another shot on target",
        },
        {
            "minute": 53,
            "team": "Chelsea",
            "on_target": True,
            "significant": True,
            "description": "Chelsea responds with a shot on target",
        },
        {
            "minute": 67,
            "team": "Chelsea",
            "on_target": False,
            "significant": False,
            "description": "Chelsea attempts a late attacking shot",
        },
        {
            "minute": 81,
            "team": "Arsenal",
            "on_target": True,
            "significant": True,
            "description": "Arsenal records a late shot on target",
        },
    ]

    for shot in shots:
        events.append({
            "type": "shot",
            **shot,
        })

    # Fictional possession intervals.
    possession_intervals = [
        (8, "Arsenal", 150),
        (20, "Chelsea", 110),
        (32, "Arsenal", 180),
        (45, "Chelsea", 140),
        (58, "Chelsea", 160),
        (72, "Arsenal", 170),
        (88, "Arsenal", 100),
    ]

    for minute, team, duration in possession_intervals:
        events.append({
            "minute": minute,
            "team": team,
            "type": "possession",
            "duration_seconds": duration,
        })

    events.sort(key=lambda event: event["minute"])
    return events


def main():
    match = {
        "match_id": "SYN-002",
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "dataset_type": "synthetic",
        "description": (
            "Fictional match events generated for MatchMind AI testing."
        ),
        "events": generate_events(),
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(match, file, indent=2)

    print(f"Generated {len(match['events'])} synthetic events.")
    print(f"Saved dataset to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
