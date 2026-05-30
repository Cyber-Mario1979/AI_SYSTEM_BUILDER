from __future__ import annotations

import json
from pathlib import Path

from asbp.document_lifecycle_model import (
    DocumentLifecycleRuleLibraryModel,
    DocumentLifecycleRuleModel,
)


DEFAULT_DOCUMENT_LIFECYCLE_RULE_SOURCE_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "source"
    / "document_lifecycle"
    / "starter_document_lifecycle_rules.json"
)


def load_document_lifecycle_rule_library_from_payload(
    payload: dict,
) -> DocumentLifecycleRuleLibraryModel:
    if "lifecycle_rules" not in payload:
        raise ValueError("document lifecycle rule library payload must include lifecycle_rules")

    return DocumentLifecycleRuleLibraryModel(**payload)


def load_document_lifecycle_rule_library_from_path(
    path: Path,
) -> DocumentLifecycleRuleLibraryModel:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    return load_document_lifecycle_rule_library_from_payload(payload)


def load_default_document_lifecycle_rule_library() -> DocumentLifecycleRuleLibraryModel:
    return load_document_lifecycle_rule_library_from_path(
        DEFAULT_DOCUMENT_LIFECYCLE_RULE_SOURCE_PATH,
    )


def list_document_lifecycle_rule_ids(
    library: DocumentLifecycleRuleLibraryModel,
) -> list[str]:
    return [rule.rule_id for rule in library.lifecycle_rules]


def get_document_lifecycle_rule_by_id(
    library: DocumentLifecycleRuleLibraryModel,
    rule_id: str,
) -> DocumentLifecycleRuleModel:
    for rule in library.lifecycle_rules:
        if rule.rule_id == rule_id:
            return rule

    raise ValueError(f"Document lifecycle rule source record not found: {rule_id}")


def get_default_document_lifecycle_rule(
    library: DocumentLifecycleRuleLibraryModel | None = None,
) -> DocumentLifecycleRuleModel:
    library = library or load_default_document_lifecycle_rule_library()
    if len(library.lifecycle_rules) != 1:
        raise ValueError("Default document lifecycle rule library must contain exactly one rule")
    return library.lifecycle_rules[0]


def assert_document_lifecycle_rules_exist(
    library: DocumentLifecycleRuleLibraryModel,
    required_rule_ids: set[str],
) -> None:
    registered_rule_ids = set(list_document_lifecycle_rule_ids(library))
    missing_rule_ids = sorted(required_rule_ids - registered_rule_ids)
    if missing_rule_ids:
        joined_missing_ids = ", ".join(missing_rule_ids)
        raise ValueError(f"Document lifecycle rule source records not found: {joined_missing_ids}")
