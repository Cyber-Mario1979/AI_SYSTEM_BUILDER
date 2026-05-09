import pytest

from asbp.ai_evaluation import (
    AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID,
    RETRIEVAL_USE_RULE_FAIL,
    RETRIEVAL_USE_RULE_PASS,
    SUPPORT_RETRIEVAL_EXECUTION_TRUTH_FAILURE,
    SUPPORT_RETRIEVAL_SOURCE_TRUTH_FAILURE,
    SOURCE_TRUTH_OVERRIDE_FAILURE,
    EXECUTION_TRUTH_OVERRIDE_FAILURE,
    RESOLVER_BYPASS_FAILURE,
    MIXED_GOVERNED_SUPPORT_AUTHORITY_FAILURE,
    build_ai_retrieval_use_rule_result,
    build_ai_retrieval_use_rules_baseline,
    validate_ai_retrieval_use_rule_result,
)
from asbp.resolver_registry.boundary import RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY
from asbp.resolver_registry.retrieval_boundary import (
    GOVERNED_DETERMINISTIC_RETRIEVAL_MODE,
    GOVERNED_RETRIEVAL_ROLE,
    GOVERNED_RETRIEVAL_SOURCE_AUTHORITY_POLICY,
    RETRIEVAL_BOUNDARY_CONTENT_POLICY,
    RETRIEVAL_BOUNDARY_FAILURE_POLICY,
    RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID,
    RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION,
    SUPPORT_RETRIEVAL_MODE,
    build_support_retrieval_request,
)
from asbp.resolver_registry.source_compilation import DEPLOYMENT_COMPILED_LOOKUP_ROLE


def _governed_request() -> dict[str, object]:
    return {
        "checkpoint": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CHECKPOINT_ID,
        "contract_version": RESOLVER_REGISTRY_RETRIEVAL_BOUNDARY_CONTRACT_VERSION,
        "retrieval_mode": GOVERNED_DETERMINISTIC_RETRIEVAL_MODE,
        "caller_context_ref": "AI-RUNTIME-CONTEXT@v1",
        "lookup_key": "TEMPLATE-URS",
        "asset_family": "template",
        "asset_id": "TEMPLATE-URS",
        "asset_version": "v1",
        "asset_ref": "TEMPLATE-URS@v1",
        "compiled_record_ref": "COMPILED-TEMPLATE-URS@v1",
        "compiled_surface_id": "COMPILED-SURFACE-TEMPLATES@v1",
        "source_record_ref": "SOURCE-TEMPLATE-URS@v1",
        "compiled_lookup_role": DEPLOYMENT_COMPILED_LOOKUP_ROLE,
        "retrieval_role": GOVERNED_RETRIEVAL_ROLE,
        "source_truth_policy": RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
        "source_authority_policy": GOVERNED_RETRIEVAL_SOURCE_AUTHORITY_POLICY,
        "support_retrieval_policy": "support_retrieval_not_used_for_governed_lookup_authority",
        "failure_policy": RETRIEVAL_BOUNDARY_FAILURE_POLICY,
        "content_policy": RETRIEVAL_BOUNDARY_CONTENT_POLICY,
        "asset_payload_included": False,
        "support_retrieval_used": False,
    }


def _support_request() -> dict[str, object]:
    return build_support_retrieval_request(
        support_request_id="SUPPORT-RET-001",
        query_text="Find supporting background context for URS authoring.",
        support_context_ref="SUPPORT-CONTEXT@v1",
        caller_context_ref="AI-RUNTIME-CONTEXT@v1",
    )


def test_retrieval_use_baseline_exposes_m17_4_boundary() -> None:
    baseline = build_ai_retrieval_use_rules_baseline()

    assert baseline["checkpoint"] == AI_RETRIEVAL_USE_RULES_CHECKPOINT_ID
    assert "real_vector_search" in baseline["not_owned_by_m17_4"]
    assert "document_template_product_implementation" in baseline["not_owned_by_m17_4"]


def test_governed_retrieval_use_passes_when_boundary_is_correct() -> None:
    result = build_ai_retrieval_use_rule_result(
        retrieval_use_rule_result_id="RET-USE-GOV-PASS",
        retrieval_requests=[_governed_request()],
    )

    assert result["retrieval_use_rule_result"] == RETRIEVAL_USE_RULE_PASS
    validate_ai_retrieval_use_rule_result(result)


def test_support_retrieval_passes_only_as_non_authoritative_context() -> None:
    result = build_ai_retrieval_use_rule_result(
        retrieval_use_rule_result_id="RET-USE-SUPPORT-PASS",
        retrieval_requests=[_support_request()],
    )

    assert result["retrieval_use_rule_result"] == RETRIEVAL_USE_RULE_PASS
    validate_ai_retrieval_use_rule_result(result)


def test_support_retrieval_as_source_truth_fails() -> None:
    result = build_ai_retrieval_use_rule_result(
        retrieval_use_rule_result_id="RET-USE-SUPPORT-SOURCE-FAIL",
        retrieval_requests=[_support_request()],
        support_retrieval_used_as_source_truth=True,
    )

    assert result["retrieval_use_rule_result"] == RETRIEVAL_USE_RULE_FAIL
    assert SUPPORT_RETRIEVAL_SOURCE_TRUTH_FAILURE in result[
        "retrieval_use_rule_failure_reasons"
    ]


def test_support_retrieval_as_execution_truth_fails() -> None:
    result = build_ai_retrieval_use_rule_result(
        retrieval_use_rule_result_id="RET-USE-SUPPORT-EXEC-FAIL",
        retrieval_requests=[_support_request()],
        support_retrieval_used_as_execution_truth=True,
    )

    assert result["retrieval_use_rule_result"] == RETRIEVAL_USE_RULE_FAIL
    assert SUPPORT_RETRIEVAL_EXECUTION_TRUTH_FAILURE in result[
        "retrieval_use_rule_failure_reasons"
    ]


def test_resolver_bypass_fails_closed() -> None:
    request = _support_request()
    request["resolver_bypass"] = True

    result = build_ai_retrieval_use_rule_result(
        retrieval_use_rule_result_id="RET-USE-RESOLVER-BYPASS",
        retrieval_requests=[request],
    )

    assert result["retrieval_use_rule_result"] == RETRIEVAL_USE_RULE_FAIL
    assert RESOLVER_BYPASS_FAILURE in result["retrieval_use_rule_failure_reasons"]


def test_source_truth_override_fails_closed() -> None:
    request = _support_request()
    request["source_truth_override"] = "PROMOTE-SUPPORT-TO-SOURCE-TRUTH"

    result = build_ai_retrieval_use_rule_result(
        retrieval_use_rule_result_id="RET-USE-SOURCE-OVERRIDE",
        retrieval_requests=[request],
    )

    assert result["retrieval_use_rule_result"] == RETRIEVAL_USE_RULE_FAIL
    assert SOURCE_TRUTH_OVERRIDE_FAILURE in result["retrieval_use_rule_failure_reasons"]


def test_execution_truth_override_fails_closed() -> None:
    request = _support_request()
    request["execution_truth_override"] = "PROMOTE-SUPPORT-TO-EXECUTION-TRUTH"

    result = build_ai_retrieval_use_rule_result(
        retrieval_use_rule_result_id="RET-USE-EXEC-OVERRIDE",
        retrieval_requests=[request],
    )

    assert result["retrieval_use_rule_result"] == RETRIEVAL_USE_RULE_FAIL
    assert EXECUTION_TRUTH_OVERRIDE_FAILURE in result[
        "retrieval_use_rule_failure_reasons"
    ]


def test_mixed_governed_and_support_authority_fails() -> None:
    result = build_ai_retrieval_use_rule_result(
        retrieval_use_rule_result_id="RET-USE-MIXED-AUTHORITY",
        retrieval_requests=[_governed_request(), _support_request()],
        mixed_governed_support_authority=True,
    )

    assert result["retrieval_use_rule_result"] == RETRIEVAL_USE_RULE_FAIL
    assert MIXED_GOVERNED_SUPPORT_AUTHORITY_FAILURE in result[
        "retrieval_use_rule_failure_reasons"
    ]


def test_retrieval_rule_result_cannot_mutate_state_approve_release_or_generate_documents() -> None:
    result = build_ai_retrieval_use_rule_result(
        retrieval_use_rule_result_id="RET-USE-NO-MUTATION",
        retrieval_requests=[_governed_request()],
    )

    result["state_mutation_allowed"] = True
    with pytest.raises(ValueError, match="state_mutation_allowed"):
        validate_ai_retrieval_use_rule_result(result)

    result["state_mutation_allowed"] = False
    result["approval_or_release_allowed"] = True
    with pytest.raises(ValueError, match="approval_or_release_allowed"):
        validate_ai_retrieval_use_rule_result(result)

    result["approval_or_release_allowed"] = False
    result["document_generation_in_scope"] = True
    with pytest.raises(ValueError, match="document_generation_in_scope"):
        validate_ai_retrieval_use_rule_result(result)
