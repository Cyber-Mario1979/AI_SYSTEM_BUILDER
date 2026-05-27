from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.calendar_source_model import CalendarLibraryModel
from asbp.calendar_source_store import (
    build_calendar_day_definition_id,
    get_calendar_by_id,
    get_work_day_by_name,
    list_calendar_ids,
    list_calendars_by_type,
    load_default_calendar_library,
    load_calendar_library_from_payload,
)


def _seven_day_workweek() -> list[dict]:
    return [
        {"day": "monday", "is_working_day": True, "start_time": "09:00", "end_time": "17:00", "break_minutes": 60},
        {"day": "tuesday", "is_working_day": True, "start_time": "09:00", "end_time": "17:00", "break_minutes": 60},
        {"day": "wednesday", "is_working_day": True, "start_time": "09:00", "end_time": "17:00", "break_minutes": 60},
        {"day": "thursday", "is_working_day": True, "start_time": "09:00", "end_time": "17:00", "break_minutes": 60},
        {"day": "friday", "is_working_day": False, "break_minutes": 0},
        {"day": "saturday", "is_working_day": False, "break_minutes": 0},
        {"day": "sunday", "is_working_day": True, "start_time": "09:00", "end_time": "17:00", "break_minutes": 60},
    ]


def _minimal_calendar_payload() -> dict:
    return {
        "calendar_id": "CAL-TEST-WORKWEEK@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "display_name": "Test workweek",
        "calendar_type": "workweek",
        "timezone": "Africa/Cairo",
        "locale_context": "Cairo / Egypt explicit test context",
        "regional_assumption_status": "explicit_starter_assumption",
        "user_amendable_parameters": ["working_days"],
        "working_days": _seven_day_workweek(),
        "assumption_controls": ["Calendar context must be confirmed before planning."],
    }


def _minimal_library_payload(calendar: dict | None = None) -> dict:
    return {
        "library_id": "TEST_CALENDAR_LIBRARY@v1",
        "version": "v1",
        "status": "starter_runtime_source",
        "calendars": [calendar or _minimal_calendar_payload()],
    }


def test_default_starter_calendar_library_loads_runtime_source_records():
    library = load_default_calendar_library()

    assert library.library_id == "M27_CALENDAR_STARTER_LIBRARY@v1"
    assert list_calendar_ids(library) == [
        "CAL-CAIRO-FIVE-DAY-WORKWEEK@v1",
        "CAL-CAIRO-SIX-DAY-WORKWEEK-CANDIDATE@v1",
        "CAL-WORKMONTH-BASELINE@v1",
        "CAL-USER-SUPPLIED-HOLIDAYS@v1",
        "CAL-MANUAL-FALLBACK-CONTEXT@v1",
    ]

    five_day = get_calendar_by_id(library, "CAL-CAIRO-FIVE-DAY-WORKWEEK@v1")
    assert five_day.calendar_type == "workweek"
    assert five_day.regional_assumption_status == "explicit_starter_assumption"

    friday = get_work_day_by_name(five_day, "friday")
    assert friday.is_working_day is False

    workweek_calendars = list_calendars_by_type(library, "workweek")
    assert [calendar.calendar_id for calendar in workweek_calendars] == [
        "CAL-CAIRO-FIVE-DAY-WORKWEEK@v1",
        "CAL-CAIRO-SIX-DAY-WORKWEEK-CANDIDATE@v1",
    ]


def test_calendar_day_definition_id_uses_calendar_and_day_identity():
    assert build_calendar_day_definition_id(
        "CAL-CAIRO-FIVE-DAY-WORKWEEK@v1",
        "monday",
    ) == "CAL-CAIRO-FIVE-DAY-WORKWEEK@v1::monday"


def test_calendar_library_rejects_duplicate_calendar_ids():
    calendar = _minimal_calendar_payload()
    payload = _minimal_library_payload(calendar)
    payload["calendars"].append(deepcopy(calendar))

    with pytest.raises(ValidationError) as exc_info:
        CalendarLibraryModel(**payload)

    assert "Duplicate calendar_id is not allowed: CAL-TEST-WORKWEEK@v1" in str(exc_info.value)


def test_workweek_rejects_duplicate_weekday():
    calendar = _minimal_calendar_payload()
    calendar["working_days"][1]["day"] = "monday"

    with pytest.raises(ValidationError) as exc_info:
        load_calendar_library_from_payload(_minimal_library_payload(calendar))

    assert "Duplicate working day is not allowed" in str(exc_info.value)


def test_workweek_rejects_missing_weekday_definition():
    calendar = _minimal_calendar_payload()
    calendar["working_days"] = calendar["working_days"][:-1]

    with pytest.raises(ValidationError) as exc_info:
        load_calendar_library_from_payload(_minimal_library_payload(calendar))

    assert "workweek calendar must define all seven weekdays" in str(exc_info.value)


def test_working_day_rejects_missing_times():
    calendar = _minimal_calendar_payload()
    calendar["working_days"][0].pop("start_time")

    with pytest.raises(ValidationError) as exc_info:
        load_calendar_library_from_payload(_minimal_library_payload(calendar))

    assert "Working day requires start_time and end_time: monday" in str(exc_info.value)


def test_working_day_rejects_end_time_before_start_time():
    calendar = _minimal_calendar_payload()
    calendar["working_days"][0]["start_time"] = "17:00"
    calendar["working_days"][0]["end_time"] = "09:00"

    with pytest.raises(ValidationError) as exc_info:
        load_calendar_library_from_payload(_minimal_library_payload(calendar))

    assert "Working day start_time must be before end_time: monday" in str(exc_info.value)


def test_non_working_day_rejects_hidden_work_times():
    calendar = _minimal_calendar_payload()
    calendar["working_days"][4]["start_time"] = "09:00"
    calendar["working_days"][4]["end_time"] = "12:00"

    with pytest.raises(ValidationError) as exc_info:
        load_calendar_library_from_payload(_minimal_library_payload(calendar))

    assert "Non-working day cannot include work times: friday" in str(exc_info.value)


def test_cairo_context_rejects_not_applicable_regional_assumption_status():
    calendar = _minimal_calendar_payload()
    calendar["regional_assumption_status"] = "not_applicable"

    with pytest.raises(ValidationError) as exc_info:
        load_calendar_library_from_payload(_minimal_library_payload(calendar))

    assert "Cairo/Egypt calendar context must use an explicit regional" in str(exc_info.value)


def test_workmonth_calendar_requires_workmonth_rules():
    calendar = _minimal_calendar_payload()
    calendar["calendar_id"] = "CAL-TEST-WORKMONTH@v1"
    calendar["calendar_type"] = "workmonth"
    calendar["timezone"] = "user_defined"
    calendar["locale_context"] = "User-defined workmonth"
    calendar["regional_assumption_status"] = "human_confirmation_required"
    calendar["working_days"] = []

    with pytest.raises(ValidationError) as exc_info:
        load_calendar_library_from_payload(_minimal_library_payload(calendar))

    assert "workmonth calendar requires workmonth_rules" in str(exc_info.value)


def test_holiday_policy_calendar_requires_holiday_rules():
    calendar = _minimal_calendar_payload()
    calendar["calendar_id"] = "CAL-TEST-HOLIDAYS@v1"
    calendar["calendar_type"] = "holiday_policy"
    calendar["timezone"] = "user_defined"
    calendar["locale_context"] = "User-defined holidays"
    calendar["regional_assumption_status"] = "human_confirmation_required"
    calendar["working_days"] = []

    with pytest.raises(ValidationError) as exc_info:
        load_calendar_library_from_payload(_minimal_library_payload(calendar))

    assert "holiday_policy calendar requires holiday_rules" in str(exc_info.value)


def test_blank_user_amendable_parameter_is_rejected():
    calendar = _minimal_calendar_payload()
    calendar["user_amendable_parameters"] = [" "]

    with pytest.raises(ValidationError) as exc_info:
        load_calendar_library_from_payload(_minimal_library_payload(calendar))

    assert "Blank calendar source value is not allowed" in str(exc_info.value)


def test_persisted_state_payload_is_not_calendar_source_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_calendar_library_from_payload(persisted_state_payload)

    assert "calendar library payload must include calendars" in str(exc_info.value)
