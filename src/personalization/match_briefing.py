
def build_team_briefing(
    team: str,
    match_analysis: dict,
    key_moments: list[dict],
) -> dict:
    """Build a personalized briefing from recorded match evidence."""

    team_stats = match_analysis.get("team_stats", {})

    if team not in team_stats:
        raise ValueError(f"No statistics available for team: {team}")

    stats = team_stats[team]

    team_moments = [
        moment
        for moment in key_moments
        if moment.get("team") == team
    ]

    team_moments.sort(
        key=lambda moment: (
            moment.get("minute")
            if moment.get("minute") is not None
            else 999
        )
    )

    summary = (
        f"{team} recorded {stats['possession_pct']}% possession, "
        f"{stats['shots_on_target']} shots on target, and "
        f"{stats['pass_completion_pct']}% pass completion."
    )

    if team_moments:
        moment_summary = (
            f"{len(team_moments)} verified key moment(s) "
            f"are associated with {team}."
        )
    else:
        moment_summary = (
            f"No verified key moments are associated with {team}."
        )

    return {
        "team": team,
        "statistics": stats,
        "key_moments": team_moments,
        "summary": summary,
        "moment_summary": moment_summary,
    }
