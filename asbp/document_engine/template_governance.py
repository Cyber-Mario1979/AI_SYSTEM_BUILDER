"""Template-governance foundation for the M12.1 document-engine checkpoint."""

from __future__ import annotations

from typing import Any

CHECKPOINT_ID = "M12.1"

GOVERNED_TEMPLATE_ARTIFACT_KIND = "governed_document_template"
SUPPORTING_TEMPLATE_ARTIFACT_KIND = "supporting_template_reference"

AUTHORITATIVE_TEMPLATE_SOURCE_ROLE = "authoritative_template_only"
NON_AUTHORITATIVE_SUPPORTING_CONTENT_POLICY = (
    "excluded_from_governed_template_selection"
)

EXACT_VERSION_PINNED_SELECTION_MODE = "exact_version_pinned"

SUPPORTED_TEMPLATE_FAMILIES = (
    "urs",
    "dcf",
    "protocol",
    "report",
    "other_governed_document",
)

SUPPORTED_TEMPLATE_ARTIFACT_KINDS = (
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    SUPPORTING_TEMPLATE_ARTIFACT_KIND,
)

_REQUIRED_IDENTITY_FIELDS = (
    "template_family",
    "template_id",
    "template_version",
    "artifact_kind",
)

_REQUIRED_RETRIEVAL_FIELDS = (
    "template_family",
    "template_id",
    "template_version",
    "artifact_kind",
    "selection_mode",
    "authority_role",
)

_PROHIBITED_RETRIEVAL_FIELDS = (
    "query_text",
    "search_scope",
    "fallback_to_latest",
    "probabilistic_lookup",
    "source_authority_override",
    "resolver_bypass",
)


def build_template_governance_baseline() -> dict[str, Any]:
    """Return the explicit M12.1 template-governance baseline."""

    return {
        "checkpoint": CHECKPOINT_ID,
        "template_identity_rules": {
            "required_fields": list(_REQUIRED_IDENTITY_FIELDS),
            "supported_template_families": list(SUPPORTED_TEMPLATE_FAMILIES),
            "supported_artifact_kinds": list(SUPPORTED_TEMPLATE_ARTIFACT_KINDS),
            "version_policy": EXACT_VERSION_PINNED_SELECTION_MODE,
        },
        "governed_template_retrieval": {
            "authority_role": AUTHORITATIVE_TEMPLATE_SOURCE_ROLE,
            "selection_mode": EXACT_VERSION_PINNED_SELECTION_MODE,
            "artifact_kind": GOVERNED_TEMPLATE_ARTIFACT_KIND,
            "supporting_content_policy": (
                NON_AUTHORITATIVE_SUPPORTING_CONTENT_POLICY
            ),
            "authority_boundary": "may_not_fall_back_to_non_authoritative_content",
        },
        "canonical_governed_template_families": list(
            SUPPORTED_TEMPLATE_FAMILIES
        ),
    }


def build_governed_template_retrieval_request(
    *,
    template_family: str,
    template_id: str,
    template_version: str,
    artifact_kind: str = GOVERNED_TEMPLATE_ARTIFACT_KIND,
) -> dict[str, Any]:
    """Build an authoritative governed template-retrieval request.

    The M12.1 contract is intentionally narrow:
    - exact family/id/version identity
    - exact version-pinned selection
    - authoritative template surfaces only
    - no probabilistic or fallback behavior
    """

    request: dict[str, object] = {
        "template_family": template_family,
        "template_id": template_id,
        "template_version": template_version,
        "artifact_kind": artifact_kind,
        "selection_mode": EXACT_VERSION_PINNED_SELECTION_MODE,
        "authority_role": AUTHORITATIVE_TEMPLATE_SOURCE_ROLE,
    }
    validate_template_retrieval_request(request)
    return request


def validate_template_identity(
    template_identity: dict[str, object],
    *,
    allow_supporting_artifacts: bool = True,
) -> None:
    """Validate template identity fields for the M12.1 baseline."""

    _validate_required_string_fields(
        template_identity,
        _REQUIRED_IDENTITY_FIELDS,
        error_prefix="Template identity",
    )

    template_family = str(template_identity["template_family"])
    artifact_kind = str(template_identity["artifact_kind"])

    if template_family not in SUPPORTED_TEMPLATE_FAMILIES:
        raise ValueError(
            "Unsupported template_family. "
            f"Expected one of: {', '.join(SUPPORTED_TEMPLATE_FAMILIES)}."
        )

    if allow_supporting_artifacts:
        if artifact_kind not in SUPPORTED_TEMPLATE_ARTIFACT_KINDS:
            raise ValueError(
                "Unsupported artifact_kind. "
                f"Expected one of: {', '.join(SUPPORTED_TEMPLATE_ARTIFACT_KINDS)}."
            )
        return

    if artifact_kind != GOVERNED_TEMPLATE_ARTIFACT_KIND:
        raise ValueError(
            "Governed template retrieval may target only "
            f"{GOVERNED_TEMPLATE_ARTIFACT_KIND!r} artifacts."
        )


def validate_template_retrieval_request(request: dict[str, object]) -> None:
    """Validate an authoritative template-retrieval request."""

    _validate_required_string_fields(
        request,
        _REQUIRED_RETRIEVAL_FIELDS,
        error_prefix="Template retrieval request",
    )
    _validate_prohibited_fields(request, _PROHIBITED_RETRIEVAL_FIELDS)

    validate_template_identity(request, allow_supporting_artifacts=False)

    selection_mode = request.get("selection_mode")
    if selection_mode != EXACT_VERSION_PINNED_SELECTION_MODE:
        raise ValueError(
            "Template retrieval request declares an invalid selection_mode: "
            f"expected {EXACT_VERSION_PINNED_SELECTION_MODE!r}, "
            f"got {selection_mode!r}."
        )

    authority_role = request.get("authority_role")
    if authority_role != AUTHORITATIVE_TEMPLATE_SOURCE_ROLE:
        raise ValueError(
            "Template retrieval request declares an invalid authority_role: "
            f"expected {AUTHORITATIVE_TEMPLATE_SOURCE_ROLE!r}, "
            f"got {authority_role!r}."
        )


def _validate_required_string_fields(
    payload: dict[str, object],
    required_fields: tuple[str, ...],
    *,
    error_prefix: str,
) -> None:
    for field_name in required_fields:
        value = payload.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"{error_prefix} must declare non-empty {field_name}."
            )


def _validate_prohibited_fields(
    payload: dict[str, object],
    prohibited_fields: tuple[str, ...],
) -> None:
    for field_name in prohibited_fields:
        if field_name in payload:
            raise ValueError(
                f"{field_name} is not allowed in governed template retrieval."
            )