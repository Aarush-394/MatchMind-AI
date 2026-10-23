
def identify_key_moments(
    events: list[dict],
    match_analysis: dict,
) -> list[dict]:
    """
    Identify recorded significant events and attach relevant team statistics.

    This agent uses local Python logic only. No API calls are made.
    """

    team_stats = match_analysis.get("team_stats", {})
    key_moments = []

    for event in events:
        if not event.get("significant", False):
            continue

        team = event.get("team", "Unknown")
        event_type = event.get("type", "unknown")

        moment = {
            "minute": event.get("minute"),
            "team": team,
            "event_type": event_type,
            "description": event.get(
                "description",
                "Significant event recorded in the dataset.",
            ),
            "evidence": {
                "team_stats": team_stats.get(team, {}),
                "on_target": event.get("on_target"),
                "completed": event.get("completed"),
            },
            "interpretation": (
                "This event was marked significant in the synthetic data. "
                "Its wider tactical impact requires additional context."
            ),
        }

        key_moments.append(moment)

    key_moments.sort(
        key=lambda moment: (
            moment["minute"]
            if moment["minute"] is not None
            else -1
        )
    )

    return key_moments



def summarize_key_moments(key_moments: list[dict]) -> str:
    """Summarize significant events using the supplied match evidence."""
    if not key_moments:
        return "No significant moments were identified in the match data."

    lines = [
        f"Identified {len(key_moments)} significant moment(s) "
        "from the supplied match events:"
    ]

    for moment in key_moments:
        minute = moment.get("minute")
        team = moment.get("team", "Unknown")
        description = moment.get(
            "description",
            "No event description available.",
        )

        timestamp = f"{minute}'" if minute is not None else "Minute unknown"

        lines.append(f"- {timestamp} — {team}: {description}")

    return "\n".join(lines)


def rank_key_moments(key_moments: list[dict]) -> list[dict]:
    """Rank significant moments using transparent event-based rules."""
    ranked = []

    for moment in key_moments:
        event_type = moment.get("event_type", "unknown")
        evidence = moment.get("evidence", {})

        score = 1

        if event_type == "shot":
            score += 2

            if evidence.get("on_target") is True:
                score += 2

        ranked.append({
            **moment,
            "priority_score": score,
            "priority": (
                "High" if score >= 4
                else "Medium" if score >= 2
                else "Low"
            ),
        })

    ranked.sort(
        key=lambda item: (
            -item["priority_score"],
            item.get("minute") if item.get("minute") is not None else 999,
        )
    )

    return ranked
