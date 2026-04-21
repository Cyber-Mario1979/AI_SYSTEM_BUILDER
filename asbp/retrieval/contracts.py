# asbp/retrieval/contracts.py
"""Retrieval architecture baseline for the M11.4 retrieval-architecture-basics checkpoint."""

from __future__ import annotations

GOVERNED_DETERMINISTIC_RETRIEVAL_MODE = "governed_deterministic"
PROBABILISTIC_SEARCH_RETRIEVAL_MODE = "probabilistic_search"

GOVERNED_SOURCE_OF_TRUTH_ROLE = "downstream_consumer_only"
PROBABILISTIC_SOURCE_OF_TRUTH_ROLE = "non_authoritative_support_only"

_GOVERNED_REQUIRED_FIELDS = (
    "artifact_kind",
    "lookup_id",
    "compiled_surface_id",
    "library_version",
    "source_of_truth_role",
)
_PROBABILISTIC_REQUIRED_FIELDS = (
    "query_text",
    "search_scope",
    "source_of_truth_role",
)

_GOVERNED_PROHIBITED_FIELDS = (
    "query_text",
    "search_scope",
    "source_authority_override",
    "resolver_bypass",
)
_PROBABILISTIC_PROHIBITED_FIELDS = (
    "artifact_kind",
    "lookup_id",
    "compiled_surface_id",
    "library_version",
    "source_authority_override",
    "resolver_bypass",
)


def build_retrieval_architecture_baseline() -> dict[str, object]:
    """Return the explicit retrieval-baseline rules for the current roadmap window."""
    return {
        "checkpoint": "M11.4",
        "resolver_registry_dependency": "required_before_live_governed_retrieval",
        "retrieval_categories": {
            GOVERNED_DETERMINISTIC_RETRIEVAL_MODE: {
                "source_of_truth_role": GOVERNED_SOURCE_OF_TRUTH_ROLE,
                "target_surfaces": "compiled_governed_lookup_only",
                "allowed_future_purpose": "version_pinned_governed_lookup",
                "authority_boundary": "may_not_redefine_source_authority",
            },
            PROBABILISTIC_SEARCH_RETRIEVAL_MODE: {
                "source_of_truth_role": PROBABILISTIC_SOURCE_OF_TRUTH_ROLE,
                "target_surfaces": "search_or_index_surfaces_only",
                "allowed_future_purpose": "broad_search_support",
                "authority_boundary": "may_not_redefine_source_authority",
            },
        },
    }


def build_governed_retrieval_request(
    *,
    artifact_kind: str,
    lookup_id: str,
    compiled_surface_id: str,
    library_version: str,
) -> dict[str, object]:
    """Build a governed deterministic retrieval request.

    This request shape is intentionally narrow:
    - version-pinned
    - compiled-surface-targeted
    - non-authoritative with respect to source truth
    """
    request: dict[str, object] = {
        "mode": GOVERNED_DETERMINISTIC_RETRIEVAL_MODE,
        "artifact_kind": artifact_kind,
        "lookup_id": lookup_id,
        "compiled_surface_id": compiled_surface_id,
        "library_version": library_version,
        "source_of_truth_role": GOVERNED_SOURCE_OF_TRUTH_ROLE,
    }
    validate_retrieval_request(request)
    return request


def build_probabilistic_search_retrieval_request(
    *,
    query_text: str,
    search_scope: str,
) -> dict[str, object]:
    """Build a probabilistic search retrieval request.

    This request shape is intentionally non-authoritative:
    - it may support broad search later
    - it may not act as governed source resolution
    """
    request: dict[str, object] = {
        "mode": PROBABILISTIC_SEARCH_RETRIEVAL_MODE,
        "query_text": query_text,
        "search_scope": search_scope,
        "source_of_truth_role": PROBABILISTIC_SOURCE_OF_TRUTH_ROLE,
    }
    validate_retrieval_request(request)
    return request


def validate_retrieval_request(request: dict[str, object]) -> None:
    """Validate a retrieval request against the M11.4 boundary rules."""
    mode = request.get("mode")
    if mode == GOVERNED_DETERMINISTIC_RETRIEVAL_MODE:
        _validate_required_fields(request, _GOVERNED_REQUIRED_FIELDS)
        _validate_prohibited_fields(request, _GOVERNED_PROHIBITED_FIELDS)
        _validate_exact_role(
            request,
            expected_role=GOVERNED_SOURCE_OF_TRUTH_ROLE,
        )
        return

    if mode == PROBABILISTIC_SEARCH_RETRIEVAL_MODE:
        _validate_required_fields(request, _PROBABILISTIC_REQUIRED_FIELDS)
        _validate_prohibited_fields(request, _PROBABILISTIC_PROHIBITED_FIELDS)
        _validate_exact_role(
            request,
            expected_role=PROBABILISTIC_SOURCE_OF_TRUTH_ROLE,
        )
        return

    raise ValueError(
        "Unsupported retrieval mode. "
        f"Expected one of: {GOVERNED_DETERMINISTIC_RETRIEVAL_MODE}, "
        f"{PROBABILISTIC_SEARCH_RETRIEVAL_MODE}."
    )


def _validate_required_fields(
    request: dict[str, object],
    required_fields: tuple[str, ...],
) -> None:
    for field_name in required_fields:
        value = request.get(field_name)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(
                f"Retrieval request must declare non-empty {field_name}."
            )


def _validate_prohibited_fields(
    request: dict[str, object],
    prohibited_fields: tuple[str, ...],
) -> None:
    for field_name in prohibited_fields:
        if field_name in request:
            raise ValueError(
                f"{field_name} is not allowed in this retrieval mode."
            )


def _validate_exact_role(
    request: dict[str, object],
    *,
    expected_role: str,
) -> None:
    actual_role = request.get("source_of_truth_role")
    if actual_role != expected_role:
        raise ValueError(
            "Retrieval request declares an invalid source_of_truth_role: "
            f"expected {expected_role!r}, got {actual_role!r}."
        )