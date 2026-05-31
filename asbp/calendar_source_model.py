from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


CalendarSourceStatus = Literal["starter_runtime_source", "mvp_remediation_source"]
CalendarType = Literal["workweek", "workmonth", "holiday_policy", "manual_fallback"]
WeekdayName = Literal["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
RegionalAssumptionStatus = Literal[
    "explicit_starter_assumption",
    "site_defined",
    "user_defined",
    "human_confirmation_required",
    "not_applicable",
]
HolidayRuleScope = Literal[
    "user_supplied_holidays",
    "site_shutdowns",
    "public_holidays_unverified",
    "no_holidays_assumed",
]
HolidayRuleSourceStatus = Literal["human_input_required", "starter_unverified", "not_applicable"]
WorkmonthBasis = Literal["calendar_month", "user_defined_period", "site_defined_period"]


def _time_to_minutes(value: str) -> int:
    hour_text, minute_text = value.split(":", 1)
    return int(hour_text) * 60 + int(minute_text)


class CalendarWorkDayModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    day: WeekdayName
    is_working_day: bool
    start_time: str | None = Field(default=None, pattern=r"^(?:[01][0-9]|2[0-3]):[0-5][0-9]$")
    end_time: str | None = Field(default=None, pattern=r"^(?:[01][0-9]|2[0-3]):[0-5][0-9]$")
    break_minutes: int = Field(default=0, ge=0)
    notes: str | None = Field(default=None, min_length=1)

    @model_validator(mode="after")
    def validate_working_day_times(self):
        if self.is_working_day:
            if self.start_time is None or self.end_time is None:
                raise ValueError(f"Working day requires start_time and end_time: {self.day}")
            if _time_to_minutes(self.start_time) >= _time_to_minutes(self.end_time):
                raise ValueError(f"Working day start_time must be before end_time: {self.day}")
        else:
            if self.start_time is not None or self.end_time is not None:
                raise ValueError(f"Non-working day cannot include work times: {self.day}")
            if self.break_minutes != 0:
                raise ValueError(f"Non-working day cannot include break_minutes: {self.day}")
        return self


class WorkmonthRuleModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1, pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    basis: WorkmonthBasis
    description: str = Field(min_length=1)
    user_amendable: bool = True
    notes: str | None = Field(default=None, min_length=1)


class HolidayRuleModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rule_id: str = Field(min_length=1, pattern=r"^[a-z0-9]+(?:_[a-z0-9]+)*$")
    scope: HolidayRuleScope
    source_status: HolidayRuleSourceStatus
    user_amendable: bool = True
    notes: str = Field(min_length=1)


class CalendarSourceModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    calendar_id: str = Field(min_length=1, pattern=r"^CAL-[A-Z0-9-]+@v[0-9]+$")
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: CalendarSourceStatus = "starter_runtime_source"
    display_name: str = Field(min_length=1)
    calendar_type: CalendarType
    timezone: str = Field(min_length=1)
    locale_context: str = Field(min_length=1)
    regional_assumption_status: RegionalAssumptionStatus
    user_amendable_parameters: list[str] = Field(min_length=1)
    working_days: list[CalendarWorkDayModel] = Field(default_factory=list)
    workmonth_rules: list[WorkmonthRuleModel] = Field(default_factory=list)
    holiday_rules: list[HolidayRuleModel] = Field(default_factory=list)
    assumption_controls: list[str] = Field(min_length=1)
    notes: list[str] = Field(default_factory=list)

    @field_validator("user_amendable_parameters", "assumption_controls", "notes")
    @classmethod
    def validate_no_blank_strings(cls, values: list[str]) -> list[str]:
        for value in values:
            if not value.strip():
                raise ValueError("Blank calendar source value is not allowed")
        return values

    @model_validator(mode="after")
    def validate_calendar_scope(self):
        self._validate_visible_regional_assumption()
        self._validate_unique_nested_ids()
        if self.calendar_type == "workweek":
            self._validate_workweek()
        elif self.calendar_type == "workmonth" and not self.workmonth_rules:
            raise ValueError(f"workmonth calendar requires workmonth_rules: {self.calendar_id}")
        elif self.calendar_type == "holiday_policy" and not self.holiday_rules:
            raise ValueError(f"holiday_policy calendar requires holiday_rules: {self.calendar_id}")
        elif self.calendar_type == "manual_fallback" and self.regional_assumption_status != "human_confirmation_required":
            raise ValueError("manual_fallback calendar requires human_confirmation_required regional_assumption_status: " f"{self.calendar_id}")
        return self

    def _validate_visible_regional_assumption(self) -> None:
        regional_text = f"{self.timezone} {self.locale_context}".lower()
        if ("cairo" in regional_text or "egypt" in regional_text) and self.regional_assumption_status == "not_applicable":
            raise ValueError("Cairo/Egypt calendar context must use an explicit regional assumption status: " f"{self.calendar_id}")

    def _validate_unique_nested_ids(self) -> None:
        seen_days: set[str] = set()
        for work_day in self.working_days:
            if work_day.day in seen_days:
                raise ValueError(f"Duplicate working day is not allowed in {self.calendar_id}: {work_day.day}")
            seen_days.add(work_day.day)
        seen_workmonth_rules: set[str] = set()
        for rule in self.workmonth_rules:
            if rule.rule_id in seen_workmonth_rules:
                raise ValueError(f"Duplicate workmonth rule_id is not allowed in {self.calendar_id}: {rule.rule_id}")
            seen_workmonth_rules.add(rule.rule_id)
        seen_holiday_rules: set[str] = set()
        for rule in self.holiday_rules:
            if rule.rule_id in seen_holiday_rules:
                raise ValueError(f"Duplicate holiday rule_id is not allowed in {self.calendar_id}: {rule.rule_id}")
            seen_holiday_rules.add(rule.rule_id)

    def _validate_workweek(self) -> None:
        expected_days = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}
        actual_days = {work_day.day for work_day in self.working_days}
        if actual_days != expected_days:
            raise ValueError(f"workweek calendar must define all seven weekdays: {self.calendar_id}")


class CalendarLibraryModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    library_id: str = Field(min_length=1)
    version: str = Field(min_length=1, pattern=r"^v[0-9]+$")
    status: CalendarSourceStatus = "starter_runtime_source"
    calendars: list[CalendarSourceModel] = Field(min_length=1)
    library_controls: list[str] = Field(default_factory=list)
    explicit_non_implementation_claims: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_unique_calendar_ids(self):
        calendar_ids: set[str] = set()
        for calendar in self.calendars:
            if calendar.calendar_id in calendar_ids:
                raise ValueError(f"Duplicate calendar_id is not allowed: {calendar.calendar_id}")
            calendar_ids.add(calendar.calendar_id)
        return self
