import pytest

from asbp.resolver_registry import (
    CLI_ADAPTER_ENTRY_POINT,
    CLI_ADAPTER_ONLY_POLICY,
    CORE_RESOLVER_REGISTRY_BOUNDARY,
    CORE_SERVICE_ENTRY_POINT,
    DOWNSTREAM_AI_PRODUCT_ROLE,
    RESOLVER_REGISTRY_BOUNDARY_CHECKPOINT_ID,
    RESOLVER_REGISTRY_BOUNDARY_CONTRACT_VERSION,
    RESOLVER_REGISTRY_FAILURE_POLICY,
    RESOLVER_REGISTRY_LAYER_POSITION,
    RESOLVER_REGISTRY_ROLE,
    RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
    RUNTIME_RESOLVER_REGISTRY_BOUNDARY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    TEMPLATE_ASSET_FAMILY,
    build_resolver_registry_access_request,
    build_resolver_registry_boundary_baseline,
    validate_resolver_registry_access_request,
)


def _valid_request() -> dict[str, object]:
    return build_resolver_registry_access_request(
        access_request_id="RR-REQ-001",
        access_boundary=CORE_RESOLVER_REGISTRY_BOUNDARY,
        entry_point=CORE_SERVICE_ENTRY_POINT,
        requested_asset_family=TEMPLATE_ASSET_FAMILY,
        requested_asset_ref="URS_TEMPLATE@v1",
        caller_context_ref="document_engine",
    )


def test_build_resolver_registry_boundary_baseline_exposes_m14_1_rules() -> None:
    baseline = build_resolver_registry_boundary_baseline()

    assert baseline["checkpoint"] == RESOLVER_REGISTRY_BOUNDARY_CHECKPOINT_ID
    assert baseline["contract_version"] == RESOLVER_REGISTRY_BOUNDARY_CONTRACT_VERSION
    assert CORE_RESOLVER_REGISTRY_BOUNDARY in baseline["supported_boundaries"]
    assert RUNTIME_RESOLVER_REGISTRY_BOUNDARY in baseline["supported_boundaries"]
    assert CORE_SERVICE_ENTRY_POINT in baseline["supported_entry_points"]
    assert CLI_ADAPTER_ENTRY_POINT in baseline["supported_entry_points"]
    assert TEMPLATE_ASSET_FAMILY in baseline["supported_resolvable_asset_families"]
    assert STANDARDS_BUNDLE_ASSET_FAMILY in baseline["supported_resolvable_asset_families"]
    assert baseline["resolver_registry_role"] == RESOLVER_REGISTRY_ROLE
    assert baseline["downstream_ai_product_role"] == DOWNSTREAM_AI_PRODUCT_ROLE
    assert baseline["layer_position"] == RESOLVER_REGISTRY_LAYER_POSITION
    assert baseline["source_truth_policy"] == RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY
    assert baseline["failure_policy"] == RESOLVER_REGISTRY_FAILURE_POLICY
    assert baseline["cli_adapter_policy"] == CLI_ADAPTER_ONLY_POLICY
    assert "version_pinned_asset_identity_lookup" in baseline["not_yet_implemented"]


def test_build_resolver_registry_access_request_returns_valid_shape() -> None:
    request = _valid_request()

    assert request["checkpoint"] == RESOLVER_REGISTRY_BOUNDARY_CHECKPOINT_ID
    assert request["contract_version"] == RESOLVER_REGISTRY_BOUNDARY_CONTRACT_VERSION
    assert request["access_boundary"] == CORE_RESOLVER_REGISTRY_BOUNDARY
    assert request["entry_point"] == CORE_SERVICE_ENTRY_POINT
    assert request["requested_asset_family"] == TEMPLATE_ASSET_FAMILY
    assert request["resolver_registry_role"] == RESOLVER_REGISTRY_ROLE
    assert request["adapter_policy"] == CLI_ADAPTER_ONLY_POLICY


def test_validate_resolver_registry_access_request_accepts_cli_adapter_call_only() -> None:
    request = build_resolver_registry_access_request(
        access_request_id="RR-REQ-002",
        access_boundary=RUNTIME_RESOLVER_REGISTRY_BOUNDARY,
        entry_point=CLI_ADAPTER_ENTRY_POINT,
        requested_asset_family=STANDARDS_BUNDLE_ASSET_FAMILY,
        requested_asset_ref="CQV_CORE@v1",
        caller_context_ref="cli_adapter",
    )

    assert request["entry_point"] == CLI_ADAPTER_ENTRY_POINT
    assert request["adapter_policy"] == CLI_ADAPTER_ONLY_POLICY
    validate_resolver_registry_access_request(request)


def test_validate_resolver_registry_access_request_rejects_unsupported_boundary() -> None:
    request = _valid_request()
    request["access_boundary"] = "ui_resolver_boundary"

    with pytest.raises(ValueError, match="Unsupported resolver registry access boundary"):
        validate_resolver_registry_access_request(request)


def test_validate_resolver_registry_access_request_rejects_unsupported_entry_point() -> None:
    request = _valid_request()
    request["entry_point"] = "ui_surface"

    with pytest.raises(ValueError, match="Unsupported resolver registry entry point"):
        validate_resolver_registry_access_request(request)


def test_validate_resolver_registry_access_request_rejects_unsupported_asset_family() -> None:
    request = _valid_request()
    request["requested_asset_family"] = "external_web_page"

    with pytest.raises(ValueError, match="Unsupported resolver registry asset family"):
        validate_resolver_registry_access_request(request)


def test_validate_resolver_registry_access_request_rejects_cli_owned_lookup() -> None:
    request = _valid_request()
    request["cli_owned_lookup"] = True

    with pytest.raises(ValueError, match="cli_owned_lookup is not allowed"):
        validate_resolver_registry_access_request(request)


def test_validate_resolver_registry_access_request_rejects_ai_owned_source_truth() -> None:
    request = _valid_request()
    request["ai_owned_source_truth"] = True

    with pytest.raises(ValueError, match="ai_owned_source_truth is not allowed"):
        validate_resolver_registry_access_request(request)


def test_validate_resolver_registry_access_request_rejects_filesystem_bypass() -> None:
    request = _valid_request()
    request["direct_filesystem_lookup"] = "templates/*.md"

    with pytest.raises(ValueError, match="direct_filesystem_lookup is not allowed"):
        validate_resolver_registry_access_request(request)


def test_validate_resolver_registry_access_request_rejects_state_bypass() -> None:
    request = _valid_request()
    request["state_bypass"] = True

    with pytest.raises(ValueError, match="state_bypass is not allowed"):
        validate_resolver_registry_access_request(request)
