from __future__ import annotations

import json
from pathlib import Path

from asbp.output_validation_model import (
    OutputValidationRuleLibraryModel,
    OutputValidationRuleModel,
)
from asbp.renderer_output_model import RendererSupportedOutputFormat


DEFAULT_OUTPUT_VALIDATION_RULE_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "output_validation"
    / "starter_output_validation_rules.json"
)


def load_output_validation_rule_library_from_payload(
    payload: dict,
) -> OutputValidationRuleLibraryModel:
    if "validation_rules" not in payload:
        raise ValueError("output validation rule library payload must include validation_rules")

    return OutputValidationRuleLibraryModel(**payload)


def load_output_validation_rule_library_from_path(
    path: Path,
) -> OutputValidationRuleLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_output_validation_rule_library_from_payload(payload)


def load_default_output_validation_rule_library() -> OutputValidationRuleLibraryModel:
    return load_output_validation_rule_library_from_path(
        DEFAULT_OUTPUT_VALIDATION_RULE_SOURCE_PATH,
    )


def list_output_validation_rule_ids(
    library: OutputValidationRuleLibraryModel,
) -> list[str]:
    return [rule.rule_id for rule in library.validation_rules]


def get_output_validation_rule_by_id(
    library: OutputValidationRuleLibraryModel,
    rule_id: str,
) -> OutputValidationRuleModel:
    for rule in library.validation_rules:
        if rule.rule_id == rule_id:
            return rule

    raise ValueError(f"Output validation rule source record not found: {rule_id}")


def get_output_validation_rule_for_format(
    library: OutputValidationRuleLibraryModel,
    output_format: RendererSupportedOutputFormat,
) -> OutputValidationRuleModel:
    matched_rules = [
        rule
        for rule in library.validation_rules
        if output_format in rule.supported_formats
    ]

    if len(matched_rules) == 1:
        return matched_rules[0]

    if not matched_rules:
        raise ValueError(f"Output validation rule not found for format: {output_format}")

    raise ValueError(f"Multiple output validation rules found for format: {output_format}")


def assert_output_validation_rules_exist(
    library: OutputValidationRuleLibraryModel,
    required_rule_ids: set[str],
) -> None:
    registered_rule_ids = set(list_output_validation_rule_ids(library))
    missing_rule_ids = sorted(required_rule_ids - registered_rule_ids)
    if missing_rule_ids:
        joined_missing_ids = ", ".join(missing_rule_ids)
        raise ValueError(f"Output validation rule source records not found: {joined_missing_ids}")
