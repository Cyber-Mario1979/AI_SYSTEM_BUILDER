import pytest

from asbp.resolver_registry import (
    AUTHORED_SOURCE_EDITABILITY_POLICY,
    AUTHORED_SOURCE_TRUTH_ROLE,
    COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
    DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY,
    DEPLOYMENT_COMPILED_LOOKUP_ROLE,
    RESOLVER_REGISTRY_SOURCE_COMPILATION_CHECKPOINT_ID,
    RESOLVER_REGISTRY_SOURCE_COMPILATION_CONTRACT_VERSION,
    SOURCE_COMPILATION_CONTENT_POLICY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    TEMPLATE_ASSET_FAMILY,
    build_authored_source_record,
    build_deployment_compiled_lookup_record,
    build_deployment_compiled_lookup_registry,
    build_source_compilation_separation_baseline,
    build_source_to_compiled_link,
    resolve_deployment_compiled_lookup,
    validate_authored_source_record,
    validate_deployment_compiled_lookup_record,
    validate_source_to_compiled_link,
)


def _authored_source_record() -> dict[str, str]:
    return build_authored_source_record(
        asset_family=TEMPLATE_ASSET_FAMILY,
        asset_id="URS_TEMPLATE",
        asset_version="v1",
        source_record_ref="authored://templates/URS_TEMPLATE@v1",
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


def test_source_compilation_separation_baseline_exposes_m14_4_rules() -> None:
    baseline = build_source_compilation_separation_baseline()

    assert baseline["checkpoint"] == RESOLVER_REGISTRY_SOURCE_COMPILATION_CHECKPOINT_ID
    assert (
        baseline["contract_version"]
        == RESOLVER_REGISTRY_SOURCE_COMPILATION_CONTRACT_VERSION
    )
    assert TEMPLATE_ASSET_FAMILY in baseline["supported_compiled_lookup_families"]
    assert STANDARDS_BUNDLE_ASSET_FAMILY in baseline["supported_compiled_lookup_families"]
    assert baseline["authored_source_role"] == AUTHORED_SOURCE_TRUTH_ROLE
    assert baseline["deployment_compiled_lookup_role"] == DEPLOYMENT_COMPILED_LOOKUP_ROLE
    assert (
        baseline["compiled_not_source_authority_policy"]
        == COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY
    )
    assert baseline["source_editability_policy"] == AUTHORED_SOURCE_EDITABILITY_POLICY
    assert (
        baseline["compiled_immutability_policy"]
        == DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY
    )
    assert "compiled_lookup_not_source_authority_validation" in baseline["owned_by_m14_4"]
    assert "asset_content_editing" in baseline["not_owned_by_m14_4"]


def test_build_authored_source_record_declares_editable_source_truth() -> None:
    record = _authored_source_record()

    assert record["asset_family"] == TEMPLATE_ASSET_FAMILY
    assert record["asset_id"] == "URS_TEMPLATE"
    assert record["asset_version"] == "v1"
    assert record["asset_ref"] == "URS_TEMPLATE@v1"
    assert record["source_record_ref"] == "authored://templates/URS_TEMPLATE@v1"
    assert record["source_role"] == AUTHORED_SOURCE_TRUTH_ROLE
    assert record["source_editability_policy"] == AUTHORED_SOURCE_EDITABILITY_POLICY
    assert record["content_policy"] == SOURCE_COMPILATION_CONTENT_POLICY
    validate_authored_source_record(record)


def test_build_deployment_compiled_lookup_record_declares_runtime_surface_only() -> None:
    record = _compiled_lookup_record()

    assert record["asset_family"] == TEMPLATE_ASSET_FAMILY
    assert record["asset_id"] == "URS_TEMPLATE"
    assert record["asset_version"] == "v1"
    assert record["asset_ref"] == "URS_TEMPLATE@v1"
    assert record["lookup_key"] == "template:URS_TEMPLATE@v1"
    assert record["compiled_lookup_role"] == DEPLOYMENT_COMPILED_LOOKUP_ROLE
    assert (
        record["compiled_not_source_authority_policy"]
        == COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY
    )
    assert record["compiled_immutability_policy"] == DEPLOYMENT_COMPILED_IMMUTABILITY_POLICY
    validate_deployment_compiled_lookup_record(record)


def test_source_to_compiled_link_requires_matching_identity_and_source_ref() -> None:
    link = build_source_to_compiled_link(
        authored_source_record=_authored_source_record(),
        deployment_compiled_record=_compiled_lookup_record(),
    )

    assert link["asset_ref"] == "URS_TEMPLATE@v1"
    assert link["source_record_ref"] == "authored://templates/URS_TEMPLATE@v1"
    assert link["compiled_record_ref"] == "compiled://templates/URS_TEMPLATE@v1"
    assert link["source_role"] == AUTHORED_SOURCE_TRUTH_ROLE
    assert link["compiled_lookup_role"] == DEPLOYMENT_COMPILED_LOOKUP_ROLE
    validate_source_to_compiled_link(link)


def test_source_to_compiled_link_rejects_mismatched_identity() -> None:
    compiled = build_deployment_compiled_lookup_record(
        asset_family=TEMPLATE_ASSET_FAMILY,
        asset_id="DQ_TEMPLATE",
        asset_version="v1",
        compiled_record_ref="compiled://templates/DQ_TEMPLATE@v1",
        compiled_surface_id="deployment-compiled://templates/v1",
        source_record_ref="authored://templates/URS_TEMPLATE@v1",
    )

    with pytest.raises(ValueError, match="matching version-pinned asset_id"):
        build_source_to_compiled_link(
            authored_source_record=_authored_source_record(),
            deployment_compiled_record=compiled,
        )


def test_source_to_compiled_link_rejects_mismatched_source_ref() -> None:
    compiled = build_deployment_compiled_lookup_record(
        asset_family=TEMPLATE_ASSET_FAMILY,
        asset_id="URS_TEMPLATE",
        asset_version="v1",
        compiled_record_ref="compiled://templates/URS_TEMPLATE@v1",
        compiled_surface_id="deployment-compiled://templates/v1",
        source_record_ref="authored://templates/OTHER_SOURCE@v1",
    )

    with pytest.raises(ValueError, match="same authored source_record_ref"):
        build_source_to_compiled_link(
            authored_source_record=_authored_source_record(),
            deployment_compiled_record=compiled,
        )


def test_source_compilation_rejects_latest_current_and_unversioned_refs() -> None:
    with pytest.raises(ValueError, match="latest/current/wildcard"):
        build_authored_source_record(
            asset_family=TEMPLATE_ASSET_FAMILY,
            asset_id="URS_TEMPLATE",
            asset_version="latest",
            source_record_ref="authored://templates/URS_TEMPLATE@latest",
        )

    with pytest.raises(ValueError, match="latest/current/wildcard"):
        build_deployment_compiled_lookup_record(
            asset_family=TEMPLATE_ASSET_FAMILY,
            asset_id="URS_TEMPLATE",
            asset_version="current",
            compiled_record_ref="compiled://templates/URS_TEMPLATE@current",
            compiled_surface_id="deployment-compiled://templates/v1",
            source_record_ref="authored://templates/URS_TEMPLATE@current",
        )


def test_source_compilation_rejects_compiled_authority_override_fields() -> None:
    record = _compiled_lookup_record()
    record["compiled_as_source_truth"] = True

    with pytest.raises(ValueError, match="compiled_as_source_truth is not allowed"):
        validate_deployment_compiled_lookup_record(record)

    record = _compiled_lookup_record()
    record["runtime_mutates_authored_source"] = True

    with pytest.raises(ValueError, match="runtime_mutates_authored_source is not allowed"):
        validate_deployment_compiled_lookup_record(record)


def test_source_compilation_rejects_raw_lookup_and_payload_fields() -> None:
    record = _authored_source_record()
    record["raw_filesystem_path"] = "assets/templates/urs.md"

    with pytest.raises(ValueError, match="raw_filesystem_path is not allowed"):
        validate_authored_source_record(record)

    record = _compiled_lookup_record()
    record["asset_payload"] = {"template": "payload"}

    with pytest.raises(ValueError, match="asset_payload is not allowed"):
        validate_deployment_compiled_lookup_record(record)


def test_build_deployment_compiled_lookup_registry_rejects_duplicates() -> None:
    record = _compiled_lookup_record()

    with pytest.raises(ValueError, match="Duplicate deployment compiled lookup record"):
        build_deployment_compiled_lookup_registry([record, dict(record)])


def test_resolve_deployment_compiled_lookup_returns_runtime_lookup_only() -> None:
    registry = build_deployment_compiled_lookup_registry([_compiled_lookup_record()])

    result = resolve_deployment_compiled_lookup(
        registry=registry,
        asset_family=TEMPLATE_ASSET_FAMILY,
        asset_id="URS_TEMPLATE",
        asset_version="v1",
        caller_context_ref="document_engine",
    )

    assert result["lookup_result"] == "resolved"
    assert result["resolved_lookup_key"] == "template:URS_TEMPLATE@v1"
    assert result["compiled_record_ref"] == "compiled://templates/URS_TEMPLATE@v1"
    assert result["source_record_ref"] == "authored://templates/URS_TEMPLATE@v1"
    assert result["source_role"] == AUTHORED_SOURCE_TRUTH_ROLE
    assert result["compiled_lookup_role"] == DEPLOYMENT_COMPILED_LOOKUP_ROLE
    assert result["asset_payload_included"] is False
    assert result["compiled_lookup_is_source_authority"] is False
    assert result["runtime_mutates_authored_source"] is False


def test_resolve_deployment_compiled_lookup_fails_closed_for_missing_exact_key() -> None:
    registry = build_deployment_compiled_lookup_registry([_compiled_lookup_record()])

    with pytest.raises(ValueError, match="Deployment compiled lookup failed closed"):
        resolve_deployment_compiled_lookup(
            registry=registry,
            asset_family=TEMPLATE_ASSET_FAMILY,
            asset_id="URS_TEMPLATE",
            asset_version="v2",
            caller_context_ref="document_engine",
        )


def test_deployment_compiled_lookup_supports_calendar_and_planning_basis_families() -> None:
    calendar_record = build_deployment_compiled_lookup_record(
        asset_family="calendar",
        asset_id="EG_CAIRO_5X8",
        asset_version="v1",
        compiled_record_ref="compiled://calendars/EG_CAIRO_5X8@v1",
        compiled_surface_id="deployment-compiled://calendars/v1",
        source_record_ref="authored://calendars/EG_CAIRO_5X8@v1",
    )
    planning_basis_record = build_deployment_compiled_lookup_record(
        asset_family="planning_basis",
        asset_id="CQV_STANDARD_PLANNING",
        asset_version="v1",
        compiled_record_ref="compiled://planning_basis/CQV_STANDARD_PLANNING@v1",
        compiled_surface_id="deployment-compiled://planning_basis/v1",
        source_record_ref="authored://planning_basis/CQV_STANDARD_PLANNING@v1",
    )

    assert calendar_record["lookup_key"] == "calendar:EG_CAIRO_5X8@v1"
    assert planning_basis_record["lookup_key"] == "planning_basis:CQV_STANDARD_PLANNING@v1"
