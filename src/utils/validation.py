
from typing import Any


VALID_EVENT_TYPES = {"pass", "shot", "possession"}


def validate_match_events(events: list[dict[str, Any]]) -> list[str]:
    """
    Return validation errors for malformed match events.
    An empty list means the input passed these checks.
    """

    errors = []

    if not isinstance(events, list):
        return ["Events must be provided as a list."]

    for index, event in enumerate(events):
        prefix = f"Event {index}"

        if not isinstance(event, dict):
            errors.append(f"{prefix} must be an object.")
            continue

        if not isinstance(event.get("team"), str) or not event["team"].strip():
            errors.append(f"{prefix}: team must be a non-empty string.")

        event_type = event.get("type")
        if event_type not in VALID_EVENT_TYPES:
            errors.append(f"{prefix}: unsupported event type.")

        minute = event.get("minute")
        if minute is not None:
            if (
                isinstance(minute, bool)
                or not isinstance(minute, int)
                or not 0 <= minute <= 120
            ):
                errors.append(f"{prefix}: minute must be an integer from 0 to 120.")

        if event_type == "possession":
            duration = event.get("duration_seconds")
            if (
                isinstance(duration, bool)
                or not isinstance(duration, (int, float))
                or duration < 0
            ):
                errors.append(
                    f"{prefix}: possession duration must be non-negative."
                )

        for field in ("completed", "on_target", "significant"):
            if field in event and not isinstance(event[field], bool):
                errors.append(f"{prefix}: {field} must be a boolean.")

    return errors
