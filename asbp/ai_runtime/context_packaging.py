"AI context packaging from governed engine inputs for M16.2."

from __future__ import annotations

from typing import Any

from asbp.resolver_registry.identity import parse_version_pinned_asset_ref

from .runtime_boundary import (
    AI_RUNTIME_BOUNDARY_STATUS_VALIDATED,
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_REPORTING_JOB_FAMILY,
    validate_ai_runtime_entry_request,
)

AI_CONTEXT_PACKAGING_CHECKPOINT_ID = "M16.2"
AI_CONTEXT_PACKAGING_CONTRACT_VERSION = "ai-context-packaging-v1"
AI_CONTEXT_PACKAGE_STATUS_VALIDATED = "ai_context_package_validated"

TEMPLATE_RETRIEVAL_SOURCE_FAMILY = "template_retrieval"
DCF_EXTRACTED_INPUT_SOURCE_FAMILY = "dcf_extracted_input"
DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY = "document_lifecycle_state"
RESOLVED_LIBRARY_ASSET_SOURCE_FAMILY = "resolved_library_asset"
TASK_WORKFLOW_STATE_SOURCE_FAMILY = "task_workflow_state"
EXPORT_REPORTING_REQUIREMENT_SOURCE_FAMILY = "export_reporting_requirement"
STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY = "standards_guardrail_context"
SUPPORTED_CONTEXT_SOURCE_FAMILIES = (
    TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
    DCF_EXTRACTED_INPUT_SOURCE_FAMILY,
    DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
    RESOLVED_LIBRARY_ASSET_SOURCE_FAMILY,
    TASK_WORKFLOW_STATE_SOURCE_FAMILY,
    EXPORT_REPORTING_REQUIREMENT_SOURCE_FAMILY,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
)

AUTHORITATIVE_GOVERNED_SOURCE_ROLE = "authoritative_governed_source"
GOVERNED_ENGINE_INPUT_ROLE = "governed_engine_input"
GOVERNED_CONTRACT_ROLE = "governed_contract"
NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE = "non_authoritative_support_context"
SUPPORTED_CONTEXT_SOURCE_ROLES = (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    GOVERNED_ENGINE_INPUT_ROLE,
    GOVERNED_CONTRACT_ROLE,
    NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE,
)
_AUTHORITATIVE_SOURCE_ROLES = (
    AUTHORITATIVE_GOVERNED_SOURCE_ROLE,
    GOVERNED_ENGINE_INPUT_ROLE,
    GOVERNED_CONTRACT_ROLE,
)

STRUCTURED_INPUT_PAYLOAD_CLASSIFICATION = "structured_input"
STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION = "state_snapshot"
REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION = "requirement_contract"
SUPPORTING_CONTEXT_PAYLOAD_CLASSIFICATION = "supporting_context"
SUPPORTED_PAYLOAD_CLASSIFICATIONS = (
    STRUCTURED_INPUT_PAYLOAD_CLASSIFICATION,
    STATE_SNAPSHOT_PAYLOAD_CLASSIFICATION,
    REQUIREMENT_CONTRACT_PAYLOAD_CLASSIFICATION,
    SUPPORTING_CONTEXT_PAYLOAD_CLASSIFICATION,
)

VALIDATED_EVIDENCE_STATUS = "validated"
PARTIAL_EVIDENCE_STATUS = "partial"
UNAVAILABLE_EVIDENCE_STATUS = "unavailable"
SUPPORTED_EVIDENCE_STATUSES = (
    VALIDATED_EVIDENCE_STATUS,
    PARTIAL_EVIDENCE_STATUS,
    UNAVAILABLE_EVIDENCE_STATUS,
)

_DOCUMENT_REQUIRED_SOURCE_FAMILIES = (
    TEMPLATE_RETRIEVAL_SOURCE_FAMILY,
    DOCUMENT_LIFECYCLE_STATE_SOURCE_FAMILY,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
)
_REPORTING_REQUIRED_SOURCE_FAMILIES = (
    EXPORT_REPORTING_REQUIREMENT_SOURCE_FAMILY,
    STANDARDS_GUARDRAIL_CONTEXT_SOURCE_FAMILY,
)

_PROHIBITED_CONTEXT_FIELDS = (
    "raw_prompt",
    "free_form_prompt",
    "unvalidated_user_prompt",
    "prompt_template",
    "system_prompt",
    "developer_prompt",
    "direct_llm_call",
    "llm_provider",
    "model_name",
    "state_mutation_payload",
    "approval_payload",
    "workflow_release_payload",
    "execution_truth_override",
    "source_truth_override",
    "standards_truth_override",
)

_CONTEXT_ITEM_REQUIRED_STRING_FIELDS = (
    "context_item_id",
    "source_family",
    "source_ref",
    "source_role",
    "payload_classification",
    "evidence_status",
)

_CONTEXT_PACKAGE_REQUIRED_STRING_FIELDS = (
    "checkpoint",
    "contract_version",
    "context_package_id",
    "runtime_request_id",
    "job_family",
    "caller_boundary",
    "context_package_status",
)

_CONTEXT_PACKAGE_REQUIRED_FALSE_FIELDS = (
    "contains_raw_prompt",
    "context_can_define_execution_truth",
    "support_context_can_define_source_truth",
    "missing_required_context",
    "generated_prompt_template",
    "state_mutation_payload_included",
)


def build_ai_context_packaging_baseline() -> dict[str, Any]:
    """Return the M16.2 context-packaging baseline."""
    return {
        "checkpoint": AI_CONTEXT_PACKAGING_CHECKPOINT_ID,
        "contract_version": AI_CONTEXT_PACKAGING_CONTRACT_VERSION,
        "supported_context_source_families": list(SUPPORTED_CONTEXT_SOURCE_FAMILIES),
        "supported_context_source_roles": list(SUPPORTED_CONTEXT_SOURCE_ROLES),
        "supported_payload_classifications": list(SUPPORTED_PAYLOAD_CLASSIFICATIONS),
        "supported_evidence_statuses": list(SUPPORTED_EVIDENCE_STATUSES),
        "document_required_source_families": list(_DOCUMENT_REQUIRED_SOURCE_FAMILIES),
        "reporting_required_source_families": list(_REPORTING_REQUIRED_SOURCE_FAMILIES),
        "source_role_policy": "every_context_item_must_preserve_source_role_clarity",
        "execution_truth_policy": "ai_context_packages_must_never_define_execution_truth",
        "support_context_policy": "support_context_cannot_be_promoted_to_authority",
        "not_owned_by_m16_2": [
            "actual_llm_calls",
            "prompt_templates",
            "generation_modes",
            "document_or_report_text_generation",
            "output_acceptance",
            "retry_fallback_behavior",
            "ai_evaluation",
            "retrieval_use_governance",
            "recommendation_behavior",
            "ui_api_behavior",
        ],
    }


def build_ai_context_item(
    *,
    context_item_id: str,
    source_family: str,
    source_ref: str,
    source_role: str,
    payload_classification: str,
    evidence_status: str,
    is_authoritative: bool,
    may_be_used_for_generation: bool,
    may_define_execution_truth: bool = False,
) -> dict[str, object]:
    """Build and validate one AI context item."""
    item = {
        "context_item_id": _require_non_empty_string(
            context_item_id,
            field_name="context_item_id",
            error_prefix="AI context item",
        ),
        "source_family": _normalize_supported_value(
            source_family,
            field_name="source_family",
            supported_values=SUPPORTED_CONTEXT_SOURCE_FAMILIES,
            error_prefix="AI context item",
        ),
        "source_ref": _parse_version_pinned_ref(
            source_ref,
            field_name="source_ref",
        ),
        "source_role": _normalize_supported_value(
            source_role,
            field_name="source_role",
            supported_values=SUPPORTED_CONTEXT_SOURCE_ROLES,
            error_prefix="AI context item",
        ),
        "payload_classification": _normalize_supported_value(
            payload_classification,
            field_name="payload_classification",
            supported_values=SUPPORTED_PAYLOAD_CLASSIFICATIONS,
            error_prefix="AI context item",
        ),
        "evidence_status": _normalize_supported_value(
            evidence_status,
            field_name="evidence_status",
            supported_values=SUPPORTED_EVIDENCE_STATUSES,
            error_prefix="AI context item",
        ),
        "is_authoritative": is_authoritative,
        "may_be_used_for_generation": may_be_used_for_generation,
        "may_define_execution_truth": may_define_execution_truth,
    }
    validate_ai_context_item(item)
    return item


def validate_ai_context_item(item: dict[str, object]) -> None:
    """Validate one M16.2 AI context item."""
    _validate_prohibited_fields(item, _PROHIBITED_CONTEXT_FIELDS)
    _validate_required_string_fields(
        item,
        _CONTEXT_ITEM_REQUIRED_STRING_FIELDS,
        error_prefix="AI context item",
    )
    _normalize_supported_value(
        item["source_family"],
        field_name="source_family",
        supported_values=SUPPORTED_CONTEXT_SOURCE_FAMILIES,
        error_prefix="AI context item",
    )
    source_role = _normalize_supported_value(
        item["source_role"],
        field_name="source_role",
        supported_values=SUPPORTED_CONTEXT_SOURCE_ROLES,
        error_prefix="AI context item",
    )
    _normalize_supported_value(
        item["payload_classification"],
        field_name="payload_classification",
        supported_values=SUPPORTED_PAYLOAD_CLASSIFICATIONS,
        error_prefix="AI context item",
    )
    evidence_status = _normalize_supported_value(
        item["evidence_status"],
        field_name="evidence_status",
        supported_values=SUPPORTED_EVIDENCE_STATUSES,
        error_prefix="AI context item",
    )
    _parse_version_pinned_ref(item["source_ref"], field_name="source_ref")

    is_authoritative = _require_bool(
        item.get("is_authoritative"),
        field_name="is_authoritative",
        error_prefix="AI context item",
    )
    may_be_used = _require_bool(
        item.get("may_be_used_for_generation"),
        field_name="may_be_used_for_generation",
        error_prefix="AI context item",
    )
    may_define_execution_truth = _require_bool(
        item.get("may_define_execution_truth"),
        field_name="may_define_execution_truth",
        error_prefix="AI context item",
    )

    if source_role == NON_AUTHORITATIVE_SUPPORT_CONTEXT_ROLE and is_authoritative:
        raise ValueError(
            "AI context item cannot mark non-authoritative support context "
            "as authoritative."
        )
    if is_authoritative and source_role not in _AUTHORITATIVE_SOURCE_ROLES:
        raise ValueError(
            "AI context item is_authoritative must align with an authoritative source role."
        )
    if may_define_execution_truth:
        raise ValueError("AI context item must not define execution truth.")
    if may_be_used and evidence_status == UNAVAILABLE_EVIDENCE_STATUS:
        raise ValueError(
            "AI context item with unavailable evidence cannot be used for generation."
        )


def build_ai_context_package(
    *,
    context_package_id: str,
    ai_runtime_entry_request: dict[str, object],
    context_items: list[dict[str, object]],
    required_source_families: list[str] | None = None,
) -> dict[str, object]:
    """Build and validate an AI context package from governed inputs."""
    validate_ai_runtime_entry_request(ai_runtime_entry_request)
    job_family = str(ai_runtime_entry_request["job_family"])
    required_families = list(
        required_source_families
        if required_source_families is not None
        else _default_required_source_families(job_family)
    )
    package = {
        "checkpoint": AI_CONTEXT_PACKAGING_CHECKPOINT_ID,
        "contract_version": AI_CONTEXT_PACKAGING_CONTRACT_VERSION,
        "context_package_id": _require_non_empty_string(
            context_package_id,
            field_name="context_package_id",
            error_prefix="AI context package",
        ),
        "runtime_request_id": str(ai_runtime_entry_request["ai_runtime_request_id"]),
        "job_family": job_family,
        "caller_boundary": str(ai_runtime_entry_request["caller_boundary"]),
        "runtime_boundary_status": str(
            ai_runtime_entry_request["runtime_boundary_status"]
        ),
        "context_package_status": AI_CONTEXT_PACKAGE_STATUS_VALIDATED,
        "required_source_families": required_families,
        "context_items": list(context_items),
        "declared_runtime_refs": _collect_runtime_refs(ai_runtime_entry_request),
        "contains_raw_prompt": False,
        "context_can_define_execution_truth": False,
        "support_context_can_define_source_truth": False,
        "missing_required_context": False,
        "generated_prompt_template": False,
        "state_mutation_payload_included": False,
        "source_role_policy": "context_items_preserve_source_role_and_authority",
        "generation_policy": "context_package_prepares_inputs_only_no_generation",
    }
    validate_ai_context_package(package)
    return package


def validate_ai_context_package(package: dict[str, object]) -> None:
    """Validate one M16.2 AI context package."""
    _validate_prohibited_fields(package, _PROHIBITED_CONTEXT_FIELDS)
    _validate_required_string_fields(
        package,
        _CONTEXT_PACKAGE_REQUIRED_STRING_FIELDS,
        error_prefix="AI context package",
    )
    _validate_expected_exact_value(
        package,
        field_name="checkpoint",
        expected_value=AI_CONTEXT_PACKAGING_CHECKPOINT_ID,
        error_prefix="AI context package",
    )
    _validate_expected_exact_value(
        package,
        field_name="contract_version",
        expected_value=AI_CONTEXT_PACKAGING_CONTRACT_VERSION,
        error_prefix="AI context package",
    )
    _validate_expected_exact_value(
        package,
        field_name="context_package_status",
        expected_value=AI_CONTEXT_PACKAGE_STATUS_VALIDATED,
        error_prefix="AI context package",
    )
    _validate_expected_exact_value(
        package,
        field_name="runtime_boundary_status",
        expected_value=AI_RUNTIME_BOUNDARY_STATUS_VALIDATED,
        error_prefix="AI context package",
    )

    for field_name in _CONTEXT_PACKAGE_REQUIRED_FALSE_FIELDS:
        if package.get(field_name) is not False:
            raise ValueError(
                f"AI context package requires {field_name} to be False."
            )

    context_items = package.get("context_items")
    if not isinstance(context_items, list) or not context_items:
        raise ValueError("AI context package must declare non-empty context_items.")

    declared_runtime_refs = package.get("declared_runtime_refs")
    if not isinstance(declared_runtime_refs, list) or not declared_runtime_refs:
        raise ValueError(
            "AI context package must declare non-empty declared_runtime_refs."
        )
    declared_ref_set = {
        _parse_version_pinned_ref(ref, field_name="declared_runtime_refs")
        for ref in declared_runtime_refs
    }

    required_families = package.get("required_source_families")
    if not isinstance(required_families, list) or not required_families:
        raise ValueError(
            "AI context package must declare non-empty required_source_families."
        )
    normalized_required_families = [
        _normalize_supported_value(
            source_family,
            field_name="required_source_family",
            supported_values=SUPPORTED_CONTEXT_SOURCE_FAMILIES,
            error_prefix="AI context package",
        )
        for source_family in required_families
    ]

    item_ids: list[str] = []
    present_families: set[str] = set()
    for item in context_items:
        if not isinstance(item, dict):
            raise ValueError("AI context package context_items must contain dicts.")
        validate_ai_context_item(item)
        item_ids.append(str(item["context_item_id"]))
        present_families.add(str(item["source_family"]))
        item_ref = _parse_version_pinned_ref(item["source_ref"], field_name="source_ref")
        if item_ref not in declared_ref_set:
            raise ValueError(
                "AI context item source_ref is not declared by the AI runtime "
                f"entry request: {item_ref!r}."
            )

    _reject_duplicates(item_ids, field_name="context_item_id")

    missing = sorted(set(normalized_required_families) - present_families)
    if missing:
        raise ValueError(
            "AI context package is missing required context source families: "
            f"{', '.join(missing)}."
        )


def _default_required_source_families(job_family: str) -> tuple[str, ...]:
    if job_family == GOVERNED_DOCUMENT_JOB_FAMILY:
        return _DOCUMENT_REQUIRED_SOURCE_FAMILIES
    if job_family == GOVERNED_REPORTING_JOB_FAMILY:
        return _REPORTING_REQUIRED_SOURCE_FAMILIES
    raise ValueError(f"Unsupported AI runtime job_family: {job_family!r}.")


def _collect_runtime_refs(ai_runtime_entry_request: dict[str, object]) -> list[str]:
    refs: list[str] = []
    for field_name in ("governed_source_refs", "engine_contract_refs"):
        raw_refs = ai_runtime_entry_request.get(field_name)
        if not isinstance(raw_refs, list):
            raise ValueError(
                f"AI runtime entry request must expose list field {field_name}."
            )
        for raw_ref in raw_refs:
            refs.append(_parse_version_pinned_ref(raw_ref, field_name=field_name))
    _reject_duplicates(refs, field_name="declared_runtime_refs")
    return sorted(refs)


def _parse_version_pinned_ref(raw_ref: object, *, field_name: str) -> str:
    ref = _require_non_empty_string(
        raw_ref,
        field_name=field_name,
        error_prefix="AI context packaging ref",
    )
    return parse_version_pinned_asset_ref(ref)["asset_ref"]


def _normalize_supported_value(
    value: object,
    *,
    field_name: str,
    supported_values: tuple[str, ...],
    error_prefix: str,
) -> str:
    normalized = _require_non_empty_string(
        value,
        field_name=field_name,
        error_prefix=error_prefix,
    )
    if normalized not in supported_values:
        raise ValueError(
            f"{error_prefix} declares unsupported {field_name}. "
            f"Expected one of: {', '.join(supported_values)}."
        )
    return normalized


def _require_bool(value: object, *, field_name: str, error_prefix: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{error_prefix} must declare boolean {field_name}.")
    return value


def _require_non_empty_string(
    value: object,
    *,
    field_name: str,
    error_prefix: str,
) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{error_prefix} must declare non-empty {field_name}.")
    return value.strip()


def _validate_required_string_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    *,
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        _require_non_empty_string(
            payload.get(field_name),
            field_name=field_name,
            error_prefix=error_prefix,
        )


def _validate_expected_exact_value(
    payload: dict[str, object],
    *,
    field_name: str,
    expected_value: str,
    error_prefix: str,
) -> None:
    actual_value = payload.get(field_name)
    if actual_value != expected_value:
        raise ValueError(
            f"{error_prefix} declares an invalid {field_name}: "
            f"expected {expected_value!r}, got {actual_value!r}."
        )


def _validate_prohibited_fields(
    payload: dict[str, object],
    prohibited_fields: tuple[str, ...],
) -> None:
    for field_name in prohibited_fields:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in M16.2 AI context packages."
            )


def _reject_duplicates(values: list[str], *, field_name: str) -> None:
    seen: set[str] = set()
    for value in values:
        if value in seen:
            raise ValueError(f"Duplicate value in {field_name}: {value!r}.")
        seen.add(value)
