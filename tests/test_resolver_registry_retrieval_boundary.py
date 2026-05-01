import pytest

from asbp.resolver_registry import (
    COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
    DEPLOYMENT_COMPILED_LOOKUP_ROLE,
    GOVERNED_DETERMINISTIC_RETRIEVAL_MODE,
    GOVERNED_RETRIEVAL_ROLE,
    GOVERNED_RETRIEVAL_SOURCE_AUTHORITY_POLICY,
    RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID,
    RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION,
    RETRIEVAL_BOUNDARY_CONTENT_POLICY,
    RETRIEVAL_BOUNDARY_FAILURE_POLICY,
    SUPPORT_RETRIEVAL_AI_COMPATIBILITY_POLICY,
    SUPPORT_RETRIEVAL_MODE,
    SUPPORT_RETRIEVAL_ROLE,
    SUPPORT_RETRIEVAL_SOURCE_AUTHORITY_POLICY,
    TEMPLATE_ASSET_FAMILY,
    build_deployment_compiled_lookup_record,
    build_governed_retrieval_request_from_compiled_lookup,
    build_retrieval_boundary_baseline,
    build_support_retrieval_request,
    validate_governed_retrieval_request,
    validate_retrieval_boundary_request,
    validate_support_retrieval_request,
)


def _compiled_lookup_record() -> dict[str, str]:
    return build_deployment_compiled_lookup_record(
        asset_family=TEMPLATE_ASSET_FAMILY,
        asset_id="URS_TEMPLATE",
        asset_version="v1",
        compiled_record_ref="compiled://templates/URS_TEMPLATE@v1",
        compiled_surface_id="deployment-compiled://templates/v1",
        source_record_ref="authored://templates/URS_TEMPLATE@v1",
    )


def _support_request() -> dict[str, object]:
    return build_support_retrieval_request(
        support_request_id="SUPPORT-001",
        query_text="find related template guidance",
        support_context_ref="operator-support",
        caller_context_ref="ai_context_packaging_future",
    )


def test_retrieval_boundary_baseline_exposes_m14_5_rules() -> None:
    baseline = build_retrieval_boundary_baseline()

    assert baseline["checkpoint"] == RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID
    assert baseline["contract_version"] == RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION
    assert GOVERNED_DETERMINISTIC_RETRIEVAL_MODE in baseline["retrieval_modes"]
    assert SUPPORT_RETRIEVAL_MODE in baseline["retrieval_modes"]
    assert baseline["governed_retrieval_role"] == GOVERNED_RETRIEVAL_ROLE
    assert baseline["support_retrieval_role"] == SUPPORT_RETRIEVAL_ROLE
    assert baseline["compiled_lookup_not_source_authority_policy"] == COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY
    assert "support_retrieval_non_authority_validation" in baseline["owned_by_m14_5"]
    assert "vector_search_execution" in baseline["not_owned_by_m14_5"]


def test_governed_retrieval_request_preserves_compiled_lookup_roles() -> None:
    request = build_governed_retrieval_request_from_compiled_lookup(
        deployment_compiled_record=_compiled_lookup_record(),
        caller_context_ref="document_engine",
    )

    assert request["checkpoint"] == RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID
    assert request["retrieval_mode"] == GOVERNED_DETERMINISTIC_RETRIEVAL_MODE
    assert request["lookup_key"] == "template:URS_TEMPLATE@v1"
    assert request["asset_ref"] == "URS_TEMPLATE@v1"
    assert request["compiled_lookup_role"] == DEPLOYMENT_COMPILED_LOOKUP_ROLE
    assert request["retrieval_role"] == GOVERNED_RETRIEVAL_ROLE
    assert request["source_authority_policy"] == GOVERNED_RETRIEVAL_SOURCE_AUTHORITY_POLICY
    assert request["asset_payload_included"] is False
    assert request["support_retrieval_used"] is False
    validate_governed_retrieval_request(request)


def test_governed_retrieval_rejects_support_and_override_fields() -> None:
    request = build_governed_retrieval_request_from_compiled_lookup(
        deployment_compiled_record=_compiled_lookup_record(),
        caller_context_ref="document_engine",
    )
    request["support_search_results"] = ["maybe"]

    with pytest.raises(ValueError, match="support_search_results is not allowed"):
        validate_governed_retrieval_request(request)

    request = build_governed_retrieval_request_from_compiled_lookup(
        deployment_compiled_record=_compiled_lookup_record(),
        caller_context_ref="document_engine",
    )
    request["source_truth_override"] = "support_search"

    with pytest.raises(ValueError, match="source_truth_override is not allowed"):
        validate_governed_retrieval_request(request)


def test_governed_retrieval_rejects_payload_and_support_usage() -> None:
    request = build_governed_retrieval_request_from_compiled_lookup(
        deployment_compiled_record=_compiled_lookup_record(),
        caller_context_ref="document_engine",
    )
    request["asset_payload_included"] = True

    with pytest.raises(ValueError, match="must not include asset payload"):
        validate_governed_retrieval_request(request)

    request = build_governed_retrieval_request_from_compiled_lookup(
        deployment_compiled_record=_compiled_lookup_record(),
        caller_context_ref="document_engine",
    )
    request["support_retrieval_used"] = True

    with pytest.raises(ValueError, match="must not use support retrieval"):
        validate_governed_retrieval_request(request)


def test_support_retrieval_request_returns_support_only_metadata() -> None:
    request = _support_request()

    assert request["checkpoint"] == RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID
    assert request["retrieval_mode"] == SUPPORT_RETRIEVAL_MODE
    assert request["retrieval_role"] == SUPPORT_RETRIEVAL_ROLE
    assert request["source_authority_policy"] == SUPPORT_RETRIEVAL_SOURCE_AUTHORITY_POLICY
    assert request["ai_compatibility_policy"] == SUPPORT_RETRIEVAL_AI_COMPATIBILITY_POLICY
    assert request["governed_lookup_authority"] is False
    assert request["execution_truth_authority"] is False
    assert request["compiled_lookup_authority"] is False
    assert request["asset_payload_included"] is False
    validate_support_retrieval_request(request)


def test_support_retrieval_rejects_source_truth_and_execution_truth_overrides() -> None:
    request = _support_request()
    request["source_truth_override"] = "support_result"

    with pytest.raises(ValueError, match="source_truth_override is not allowed"):
        validate_support_retrieval_request(request)

    request = _support_request()
    request["execution_truth_override"] = "support_result"

    with pytest.raises(ValueError, match="execution_truth_override is not allowed"):
        validate_support_retrieval_request(request)


def test_support_retrieval_rejects_governed_lookup_ownership_fields() -> None:
    request = _support_request()
    request["lookup_key"] = "template:URS_TEMPLATE@v1"

    with pytest.raises(ValueError, match="lookup_key is not allowed"):
        validate_support_retrieval_request(request)

    request = _support_request()
    request["compiled_record_ref"] = "compiled://templates/URS_TEMPLATE@v1"

    with pytest.raises(ValueError, match="compiled_record_ref is not allowed"):
        validate_support_retrieval_request(request)


def test_support_retrieval_rejects_payload_and_compiled_authority() -> None:
    request = _support_request()
    request["asset_payload"] = {"content": "not allowed"}

    with pytest.raises(ValueError, match="asset_payload is not allowed"):
        validate_support_retrieval_request(request)

    request = _support_request()
    request["compiled_authority"] = True

    with pytest.raises(ValueError, match="compiled_authority is not allowed"):
        validate_support_retrieval_request(request)


def test_support_retrieval_rejects_authority_booleans_set_true() -> None:
    request = _support_request()
    request["governed_lookup_authority"] = True

    with pytest.raises(ValueError, match="governed_lookup_authority false"):
        validate_support_retrieval_request(request)


def test_retrieval_boundary_validator_dispatches_supported_modes() -> None:
    governed_request = build_governed_retrieval_request_from_compiled_lookup(
        deployment_compiled_record=_compiled_lookup_record(),
        caller_context_ref="document_engine",
    )
    support_request = _support_request()

    validate_retrieval_boundary_request(governed_request)
    validate_retrieval_boundary_request(support_request)


def test_retrieval_boundary_validator_fails_closed_for_unsupported_mode() -> None:
    request = {
        "checkpoint": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION,
        "retrieval_mode": "external_web_search",
    }

    with pytest.raises(ValueError, match="Unsupported resolver registry retrieval mode"):
        validate_retrieval_boundary_request(request)


def test_support_retrieval_requires_non_empty_query_text() -> None:
    with pytest.raises(ValueError, match="query_text"):
        build_support_retrieval_request(
            support_request_id="SUPPORT-010",
            query_text=" ",
            support_context_ref="operator-support",
            caller_context_ref="ai_context_packaging_future",
        )


def test_governed_retrieval_exposes_boundary_policies() -> None:
    request = build_governed_retrieval_request_from_compiled_lookup(
        deployment_compiled_record=_compiled_lookup_record(),
        caller_context_ref="document_engine",
    )

    assert request["failure_policy"] == RETRIEVAL_BOUNDARY_FAILURE_POLICY
    assert request["content_policy"] == RETRIEVAL_BOUNDARY_CONTENT_POLICY
    assert request["support_retrieval_policy"] == "support_retrieval_not_used_for_governed_lookup_authority"
