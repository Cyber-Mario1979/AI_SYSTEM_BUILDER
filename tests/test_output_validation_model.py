from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.output_validation_model import (
    OutputValidationResultModel,
    OutputValidationRuleLibraryModel,
    OutputValidationRuleModel,
)


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_create_uat_acceptance",
        "does_not_approve_sign_or_release_documents",
        "does_not_generate_trial_document_sets",
        "does_not_deploy_or_productize_outputs",
    ]


def _minimal_rule_payload() -> dict:
    return {
        "rule_id": "OUTVALRULE-TEST-MARKDOWN@v1",
        "version": "v1",
        "status": "runtime_facing_output_validation_rule",
        "supported_formats": ["markdown"],
        "allowed_lifecycle_states": ["draft", "in_review"],
        "required_checks": [
            "artifact_content_presence",
            "metadata_alignment",
            "placeholder_policy",
        ],
        "metadata_controls": ["Metadata must align."],
        "placeholder_policy_controls": ["Placeholders must remain visible."],
        "limitation_visibility_controls": ["Limitations must remain visible."],
        "standards_warning_controls": ["Standards warnings must remain visible."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def _minimal_library_payload(rule: dict | None = None) -> dict:
    return {
        "library_id": "M29_OUTPUT_VALIDATION_RULE_LIBRARY@v1",
        "version": "v1",
        "status": "runtime_facing_output_validation_rule_source",
        "validation_rules": [rule or _minimal_rule_payload()],
        "library_controls": ["Output validation rules control validation only."],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def _minimal_result_payload() -> dict:
    return {
        "validation_id": "OUTVAL-TEST-MARKDOWN@v1",
        "version": "v1",
        "status": "passed",
        "artifact_id": "ART-TEST-MARKDOWN@v1",
        "lifecycle_record_id": "LIFECYCLE-TEST-MARKDOWN@v1",
        "output_format": "markdown",
        "rule_id": "OUTVALRULE-TEST-MARKDOWN@v1",
        "checks_performed": ["artifact_content_presence", "metadata_alignment"],
        "issues": [],
        "explicit_non_implementation_claims": _required_non_implementation_claims(),
    }


def test_output_validation_rule_accepts_controlled_minimum():
    rule = OutputValidationRuleModel(**_minimal_rule_payload())

    assert rule.rule_id == "OUTVALRULE-TEST-MARKDOWN@v1"
    assert rule.supported_formats == ["markdown"]
    assert "draft" in rule.allowed_lifecycle_states


def test_output_validation_rule_rejects_version_mismatch():
    rule = _minimal_rule_payload()
    rule["version"] = "v2"

    with pytest.raises(ValidationError) as exc_info:
        OutputValidationRuleModel(**rule)

    assert "version must match rule_id suffix" in str(exc_info.value)


def test_output_validation_rule_rejects_duplicate_checks():
    rule = _minimal_rule_payload()
    rule["required_checks"].append("metadata_alignment")

    with pytest.raises(ValidationError) as exc_info:
        OutputValidationRuleModel(**rule)

    assert "Duplicate output validation required_checks" in str(exc_info.value)


def test_output_validation_rule_requires_non_implementation_claims():
    rule = _minimal_rule_payload()
    rule["explicit_non_implementation_claims"] = ["does_not_create_uat_acceptance"]

    with pytest.raises(ValidationError) as exc_info:
        OutputValidationRuleModel(**rule)

    assert "M29.9 output validation rule is missing explicit" in str(exc_info.value)


def test_output_validation_library_rejects_duplicate_rule_ids():
    rule = _minimal_rule_payload()
    payload = _minimal_library_payload(rule)
    payload["validation_rules"].append(deepcopy(rule))

    with pytest.raises(ValidationError) as exc_info:
        OutputValidationRuleLibraryModel(**payload)

    assert "Duplicate output validation rule id is not allowed" in str(exc_info.value)


def test_output_validation_result_status_must_match_issues():
    payload = _minimal_result_payload()
    payload["issues"] = [
        {
            "issue_code": "EMPTY_RENDERED_CONTENT",
            "message": "Content is empty.",
            "related_ids": ["ART-TEST-MARKDOWN@v1"],
        }
    ]

    with pytest.raises(ValidationError) as exc_info:
        OutputValidationResultModel(**payload)

    assert "cannot pass with error issues" in str(exc_info.value)


def test_output_validation_result_requires_non_implementation_claims():
    payload = _minimal_result_payload()
    payload["explicit_non_implementation_claims"] = ["does_not_create_uat_acceptance"]

    with pytest.raises(ValidationError) as exc_info:
        OutputValidationResultModel(**payload)

    assert "M29.9 output validation result is missing explicit" in str(exc_info.value)
