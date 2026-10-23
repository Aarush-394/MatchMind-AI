
def review_key_moments(
    key_moments: list[dict],
    original_events: list[dict],
) -> dict:
    """
    Check that each reported key moment corresponds to a recorded event.

    This is a deterministic evidence check, not an AI fact-checker.
    """

    original_event_keys = {
        (
            event.get("minute"),
            event.get("team"),
            event.get("type"),
            event.get("description"),
        )
        for event in original_events
    }

    approved = []
    rejected = []

    for moment in key_moments:
        event_key = (
            moment.get("minute"),
            moment.get("team"),
            moment.get("event_type"),
            moment.get("description"),
        )

        if event_key in original_event_keys:
            approved.append({
                **moment,
                "review_status": "verified",
                "review_note": (
                    "The event matches a record in the original dataset."
                ),
            })
        else:
            rejected.append({
                **moment,
                "review_status": "rejected",
                "review_note": (
                    "The event could not be matched to the original dataset."
                ),
            })

    return {
        "approved": approved,
        "rejected": rejected,
        "total_reviewed": len(key_moments),
    }
