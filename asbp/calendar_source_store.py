from __future__ import annotations

import json
from pathlib import Path

from asbp.calendar_source_model import (
    CalendarLibraryModel,
    CalendarSourceModel,
    CalendarType,
    CalendarWorkDayModel,
    WeekdayName,
)


DEFAULT_CALENDAR_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "calendars"
    / "starter_calendars.json"
)


def load_calendar_library_from_payload(payload: dict) -> CalendarLibraryModel:
    if "calendars" not in payload:
        raise ValueError("calendar library payload must include calendars")

    return CalendarLibraryModel(**payload)


def load_calendar_library_from_path(path: Path) -> CalendarLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_calendar_library_from_payload(payload)


def load_default_calendar_library() -> CalendarLibraryModel:
    return load_calendar_library_from_path(DEFAULT_CALENDAR_SOURCE_PATH)


def list_calendar_ids(library: CalendarLibraryModel) -> list[str]:
    return [calendar.calendar_id for calendar in library.calendars]


def get_calendar_by_id(
    library: CalendarLibraryModel,
    calendar_id: str,
) -> CalendarSourceModel:
    for calendar in library.calendars:
        if calendar.calendar_id == calendar_id:
            return calendar

    raise ValueError(f"Calendar source definition not found: {calendar_id}")


def list_calendars_by_type(
    library: CalendarLibraryModel,
    calendar_type: CalendarType,
) -> list[CalendarSourceModel]:
    return [
        calendar
        for calendar in library.calendars
        if calendar.calendar_type == calendar_type
    ]


def get_work_day_by_name(
    calendar: CalendarSourceModel,
    day: WeekdayName,
) -> CalendarWorkDayModel:
    for work_day in calendar.working_days:
        if work_day.day == day:
            return work_day

    raise ValueError(
        "Calendar work day definition not found: "
        f"{calendar.calendar_id}::{day}"
    )


def build_calendar_day_definition_id(
    calendar_id: str,
    day: WeekdayName,
) -> str:
    return f"{calendar_id}::{day}"
