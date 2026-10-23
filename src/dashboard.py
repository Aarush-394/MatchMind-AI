
import json
from pathlib import Path

import streamlit as st
from src.engine.match_report import build_match_report
from src.agents.match_workflow import build_match_workflow
import asyncio
from src.personalization.match_briefing import build_team_briefing
from src.engine.insight_formatter import (
    format_match_insights,
    generate_tactical_takeaways,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "synthetic" / "rich_sample_match.json"

def run_workflow(events: list[dict]) -> dict:
    workflow = build_match_workflow()
    result = asyncio.run(workflow.run(events))
    outputs = result.get_outputs()

    if not outputs:
        raise RuntimeError("The workflow produced no output.")

    final_result = outputs[-1]
    final_result["formatted_insights"] = format_match_insights(final_result)

    return final_result

st.set_page_config(
    page_title="MatchMind AI",
    page_icon="⚽",
    layout="wide",
)

st.title("⚽ MatchMind AI")

SAMPLE_DIR = PROJECT_ROOT / "data" / "synthetic"

MATCH_OPTIONS = {
    "Arsenal vs Chelsea — Rich Match": (
        SAMPLE_DIR / "rich_sample_match.json"
    ),
    "Default Sample Match": (
        SAMPLE_DIR / "sample_match.json"
    ),
}

selected_match = st.selectbox(
    "Choose a match dataset",
    options=list(MATCH_OPTIONS.keys()),
)

DATA_PATH = MATCH_OPTIONS[selected_match]

with DATA_PATH.open("r", encoding="utf-8") as file:
    match = json.load(file)

st.subheader(
    f"{match['home_team']} vs {match['away_team']}"
)

st.caption(
    f"Match ID: {match['match_id']} | "
    f"Dataset: {match.get('dataset_type', 'Synthetic').title()}"
)

st.info(
    match.get(
        "description",
        "Synthetic match dataset for testing MatchMind AI.",
    )
)

result = run_workflow(match["events"])
report = build_match_report(result)

st.download_button(
    label="Download Match Intelligence Report",
    data=json.dumps(report, indent=2),
    file_name=f"{match['match_id']}_intelligence_report.json",
    mime="application/json",
)

st.divider()

st.subheader(report["report_title"])

with st.expander("View complete Match Intelligence Report"):
    st.markdown("### Analyst Findings")
    st.markdown(report["analyst_analysis"])

    st.markdown("### Key Moments")
    st.markdown(report["key_moments_summary"])

    st.markdown("### Verification Summary")
    st.json(report["verification"])

    st.markdown("### Workflow Execution Trace")
    for index, stage in enumerate(report["workflow_trace"], start=1):
        st.markdown(f"**{index}.** {stage}")

st.subheader("Analyst Agent")

analyst_analysis = result.get(
    "analyst_analysis",
    "Analyst output is not available.",
)

st.markdown(analyst_analysis)

st.caption(
    "Generated locally from match statistics. "
    "No external LLM API was called."
)


st.subheader("Team Focus")

team_names = list(result["match_analysis"]["team_stats"].keys())

selected_team = st.selectbox(
    "Select a team to focus on",
    options=team_names,
    key="team_focus",
)

team_stats = result["match_analysis"]["team_stats"][selected_team]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Possession", f"{team_stats['possession_pct']}%")

with col2:
    st.metric("Shots on Target", team_stats["shots_on_target"])

with col3:
    st.metric(
        "Pass Completion",
        f"{team_stats['pass_completion_pct']}%",
    )

st.caption(
    "Statistics are calculated from the selected synthetic match dataset."
)


st.divider()
st.subheader("Personalized Match Briefing")

briefing_team = st.selectbox(
    "Choose your team",
    options=list(result["match_analysis"]["team_stats"].keys()),
    key="briefing_team",
)

briefing = build_team_briefing(
    team=briefing_team,
    match_analysis=result["match_analysis"],
    key_moments=result["key_moments"],
)

st.markdown(f"**{briefing['team']} briefing**")
st.write(briefing["summary"])
st.info(briefing["moment_summary"])

if briefing["key_moments"]:
    st.markdown("**Key moments for your team**")

    for moment in briefing["key_moments"]:
        minute = moment.get("minute")
        timestamp = f"{minute}'" if minute is not None else "Minute unknown"

        st.markdown(
            f"- **{timestamp}:** {moment['description']}"
        )
else:
    st.write("No verified key moments are available for this team.")


st.subheader("Key Moments Agent")

key_moments_summary = result.get(
    "key_moments_summary",
    "Key moments summary is not available.",
)

st.markdown(key_moments_summary)

st.caption(
    "This summary lists events marked significant in the dataset; "
    "it does not independently establish their tactical importance."
)


st.subheader("Explore Match Timeline")

approved_moments = result["key_moments"]

if approved_moments:
    timeline_teams = ["All Teams"] + sorted(
        {moment["team"] for moment in approved_moments}
    )

    selected_timeline_team = st.selectbox(
        "Filter timeline by team",
        options=timeline_teams,
        key="timeline_team_filter",
    )

    filtered_moments = [
        moment
        for moment in approved_moments
        if selected_timeline_team == "All Teams"
        or moment["team"] == selected_timeline_team
    ]

    
    for moment in filtered_moments:
        minute = moment.get("minute")
        timestamp = (
            f"{minute}'" if minute is not None else "Minute unknown"
        )

        priority = moment.get("priority", "Unranked")
        score = moment.get("priority_score", "N/A")

        with st.expander(
            f"{timestamp} — {moment['team']}: "
            f"{moment['description']} | Priority: {priority}"
        ):
            st.write("**Priority:**", priority)
            st.write("**Priority score:**", score)
            st.write("**Verification:**", moment["review_status"])
            st.write("**Explanation:**", moment["interpretation"])
            st.json(moment["evidence"])

else:
    st.info("No verified key moments are available for this match.")

st.subheader("Multi-Agent Workflow")

st.caption(
    "Follow how match data moves through each processing stage."
)

for index, stage in enumerate(result["workflow_trace"], start=1):
    st.markdown(f"**{index}.** {stage}")

st.caption(
    "The current workflow uses deterministic Python processing "
    "with explicit executor handoffs."
)
insights = result["formatted_insights"]
takeaways = generate_tactical_takeaways(result)

st.subheader("Tactical Takeaways")

for takeaway in takeaways:
    st.markdown(f"- {takeaway}")

st.caption(
    "These observations are derived from match statistics. "
    "They are not definitive tactical conclusions."
)

st.subheader("Match at a Glance")

col1, col2, col3 = st.columns(3)

total_events = len(match["events"])
total_moments = result["review_summary"]["approved"]

with col1:
    st.metric("Total Events", total_events)

with col2:
    st.metric("Key Moments", total_moments)

with col3:
    st.metric(
        "Verified Insights",
        result["review_summary"]["approved"]
    )

st.markdown(
    f"### {match['home_team']} vs {match['away_team']}"
)

st.info(
    "This is a fictional match dataset created for demonstration. "
    "It does not represent an actual Premier League match."
)


st.subheader("Insight Verification")

review_summary = result["review_summary"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Moments Reviewed",
        review_summary["total_reviewed"],
    )

with col2:
    st.metric(
        "Verified",
        review_summary["approved"],
    )

with col3:
    st.metric(
        "Rejected",
        review_summary["rejected"],
    )

if review_summary["rejected"] == 0:
    st.success(
        "All generated key moments matched the original event records."
    )
else:
    st.warning(
        "Some key moments could not be matched to the original event records."
    )


st.divider()
st.header("Team Comparison")

team_columns = st.columns(len(insights["teams"]))

for column, team in zip(team_columns, insights["teams"]):
    with column:
        st.subheader(team["team"])

        st.metric("Passes", team["passes"])
        st.metric("Completed passes", team["completed_passes"])
        st.metric("Pass completion", f"{team['pass_completion_pct']}%")
        st.metric("Shots", team["shots"])
        st.metric("Shots on target", team["shots_on_target"])
        st.metric("Recorded possession", f"{team['possession_pct']}%")

st.divider()

st.header("Significant Moments")

timeline = insights["timeline"]
team_names = ["All teams"] + [
    team["team"] for team in insights["teams"]
]

selected_team = st.selectbox(
    "Filter moments by team",
    team_names,
)

show_evidence = st.toggle(
    "Show event evidence",
    value=True,
)

filtered_timeline = [
    moment
    for moment in timeline
    if selected_team == "All teams"
    or moment["team"] == selected_team
]

filtered_timeline.sort(
    key=lambda moment: (
        moment["minute"]
        if moment["minute"] is not None
        else -1
    )
)

if filtered_timeline:
    for moment in filtered_timeline:
        minute_label = (
            f"{moment['minute']}'"
            if moment["minute"] is not None
            else "Minute unknown"
        )

        with st.expander(
            f"{minute_label} — {moment['team']}: {moment['event']}"
        ):
            st.write(moment["explanation"])

            if show_evidence:
                st.caption(f"Evidence status: {moment['status']}")
else:
    st.write("No significant moments match this filter.")


if insights["timeline"]:
    for moment in insights["timeline"]:
        with st.expander(
            f"{moment['minute']}' — {moment['team']}: {moment['event']}"
        ):
            st.write(moment["explanation"])
            st.caption(f"Evidence status: {moment['status']}")
else:
    st.write("No significant moments were identified.")

st.divider()
st.header("Evidence Review")

review = insights["review_summary"]

col1, col2, col3 = st.columns(3)

col1.metric("Events reviewed", review["total_reviewed"])
col2.metric("Verified events", review["approved"])
col3.metric("Rejected events", review["rejected"])

st.caption(
    "Verification confirms that an event matches the synthetic source "
    "data. It does not prove a tactical interpretation is correct."
)
