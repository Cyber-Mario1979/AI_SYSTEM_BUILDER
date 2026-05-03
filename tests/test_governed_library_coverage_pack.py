import pytest

from asbp.governed_library import (
    AUTHORED_SOURCE_REF_ROLE,
    COVERAGE_PACK_ARTIFACT_COORDINATION_POLICY,
    COVERAGE_PACK_EXPANSION_UNIT_POLICY,
    COVERAGE_PACK_ROLE,
    COVERAGE_PACK_SOURCE_TO_COMPILED_LINKAGE_POLICY,
    DEPLOYMENT_COMPILED_REF_ROLE,
    FREEZE_STATUS_UNFROZEN,
    GOVERNED_LIBRARY_COVERAGE_PACK_CHECKPOINT_ID,
    GOVERNED_LIBRARY_COVERAGE_PACK_CONTRACT_VERSION,
    VALIDATION_STATUS_DRAFT,
    build_authored_source_ref,
    build_coverage_pack,
    build_coverage_pack_framework_baseline,
    build_deployment_compiled_ref,
    validate_coverage_pack,
    validate_coverage_pack_reference,
)
from asbp.resolver_registry import (
    AUTHORED_SOURCE_TRUTH_ROLE,
    COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY,
    PRESET_ASSET_FAMILY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    TASK_POOL_ASSET_FAMILY,
)


def _preset_ref() -> dict[str, object]:
    return build_authored_source_ref(
        asset_family=PRESET_ASSET_FAMILY,
        asset_id="PE_RELOCATION_SELECTOR",
        asset_version="v1",
        source_record_ref="authored://presets/PE_RELOCATION_SELECTOR@v1",
    )


def _task_pool_ref() -> dict[str, object]:
    return build_authored_source_ref(
        asset_family=TASK_POOL_ASSET_FAMILY,
        asset_id="PE_RELOCATION_TASK_POOL",
        asset_version="v1",
        source_record_ref="authored://task_pools/PE_RELOCATION_TASK_POOL@v1",
    )


def _standards_ref() -> dict[str, object]:
    return build_authored_source_ref(
        asset_family=STANDARDS_BUNDLE_ASSET_FAMILY,
        asset_id="CQV_CORE",
        asset_version="v1",
        source_record_ref="authored://standards_bundles/CQV_CORE@v1",
    )


def _compiled_preset_ref() -> dict[str, object]:
    return build_deployment_compiled_ref(
        asset_family=PRESET_ASSET_FAMILY,
        asset_id="PE_RELOCATION_SELECTOR",
        asset_version="v1",
        compiled_record_ref="compiled://presets/PE_RELOCATION_SELECTOR@v1",
        compiled_surface_id="deployment-compiled://presets/v1",
        source_record_ref="authored://presets/PE_RELOCATION_SELECTOR@v1",
    )


def _coverage_pack() -> dict[str, object]:
    return build_coverage_pack(
        coverage_pack_id="CP_PE_RELOCATION",
        coverage_pack_version="v1",
        coverage_family="process_equipment",
        variant_scope_layer="post_change_requalification",
        authored_source_refs=[_preset_ref(), _task_pool_ref()],
        deployment_compiled_refs=[_compiled_preset_ref()],
        standards_bundle_refs=[_standards_ref()],
    )


def test_coverage_pack_framework_baseline_exposes_m15_2_rules() -> None:
    baseline = build_coverage_pack_framework_baseline()

    assert baseline["checkpoint"] == GOVERNED_LIBRARY_COVERAGE_PACK_CHECKPOINT_ID
    assert (
        baseline["contract_version"]
        == GOVERNED_LIBRARY_COVERAGE_PACK_CONTRACT_VERSION
    )
    assert baseline["coverage_pack_role"] == COVERAGE_PACK_ROLE
    assert baseline["expansion_unit_policy"] == COVERAGE_PACK_EXPANSION_UNIT_POLICY
    assert (
        baseline["artifact_family_coordination_policy"]
        == COVERAGE_PACK_ARTIFACT_COORDINATION_POLICY
    )
    assert (
        baseline["source_to_compiled_linkage_policy"]
        == COVERAGE_PACK_SOURCE_TO_COMPILED_LINKAGE_POLICY
    )
    assert PRESET_ASSET_FAMILY in baseline["supported_asset_families"]
    assert TASK_POOL_ASSET_FAMILY in baseline["supported_asset_families"]
    assert "bounded_coverage_pack_model" in baseline["owned_by_m15_2"]
    assert "selector_content_expansion" in baseline["not_owned_by_m15_2"]
    assert "deployment_compile_pipeline" in baseline["not_owned_by_m15_2"]


def test_build_authored_source_ref_declares_source_truth_reference_only() -> None:
    reference = _preset_ref()

    assert reference["checkpoint"] == GOVERNED_LIBRARY_COVERAGE_PACK_CHECKPOINT_ID
    assert reference["asset_family"] == PRESET_ASSET_FAMILY
    assert reference["asset_id"] == "PE_RELOCATION_SELECTOR"
    assert reference["asset_version"] == "v1"
    assert reference["asset_ref"] == "PE_RELOCATION_SELECTOR@v1"
    assert reference["record_ref"] == "authored://presets/PE_RELOCATION_SELECTOR@v1"
    assert reference["reference_role"] == AUTHORED_SOURCE_REF_ROLE
    assert reference["source_authority_policy"] == AUTHORED_SOURCE_TRUTH_ROLE
    assert reference["asset_payload_included"] is False
    assert reference["compiled_lookup_is_source_authority"] is False
    validate_coverage_pack_reference(reference)


def test_build_deployment_compiled_ref_declares_runtime_lookup_only() -> None:
    reference = _compiled_preset_ref()

    assert reference["asset_family"] == PRESET_ASSET_FAMILY
    assert reference["asset_ref"] == "PE_RELOCATION_SELECTOR@v1"
    assert reference["record_ref"] == "compiled://presets/PE_RELOCATION_SELECTOR@v1"
    assert reference["compiled_surface_id"] == "deployment-compiled://presets/v1"
    assert (
        reference["source_record_ref"]
        == "authored://presets/PE_RELOCATION_SELECTOR@v1"
    )
    assert reference["reference_role"] == DEPLOYMENT_COMPILED_REF_ROLE
    assert (
        reference["source_authority_policy"]
        == COMPILED_LOOKUP_NOT_SOURCE_AUTHORITY_POLICY
    )
    assert reference["compiled_lookup_is_source_authority"] is False
    validate_coverage_pack_reference(reference)


def test_build_coverage_pack_coordinates_multiple_asset_families() -> None:
    pack = _coverage_pack()

    assert pack["coverage_pack_id"] == "CP_PE_RELOCATION"
    assert pack["coverage_pack_version"] == "v1"
    assert pack["coverage_pack_ref"] == "CP_PE_RELOCATION@v1"
    assert pack["coverage_family"] == "process_equipment"
    assert pack["variant_scope_layer"] == "post_change_requalification"
    assert pack["validation_status"] == VALIDATION_STATUS_DRAFT
    assert pack["freeze_status"] == FREEZE_STATUS_UNFROZEN
    assert len(pack["authored_source_refs"]) == 2
    assert len(pack["deployment_compiled_refs"]) == 1
    assert len(pack["standards_bundle_refs"]) == 1
    validate_coverage_pack(pack)


def test_coverage_pack_requires_at_least_one_authored_source_ref() -> None:
    with pytest.raises(ValueError, match="at least one authored_source_ref"):
        build_coverage_pack(
            coverage_pack_id="CP_EMPTY",
            coverage_pack_version="v1",
            coverage_family="process_equipment",
            variant_scope_layer="post_change_requalification",
            authored_source_refs=[],
        )


def test_coverage_pack_rejects_unsupported_asset_family() -> None:
    with pytest.raises(ValueError, match="Unsupported coverage-pack asset family"):
        build_authored_source_ref(
            asset_family="unsupported_family",
            asset_id="BAD",
            asset_version="v1",
            source_record_ref="authored://bad/BAD@v1",
        )


def test_coverage_pack_rejects_latest_current_and_unversioned_refs() -> None:
    with pytest.raises(ValueError, match="latest/current/wildcard"):
        build_authored_source_ref(
            asset_family=PRESET_ASSET_FAMILY,
            asset_id="PE_RELOCATION_SELECTOR",
            asset_version="latest",
            source_record_ref="authored://presets/PE_RELOCATION_SELECTOR@latest",
        )

    with pytest.raises(ValueError, match="invalid coverage_pack_ref"):
        validate_coverage_pack(
            {
                **_coverage_pack(),
                "coverage_pack_ref": "CP_PE_RELOCATION",
            }
        )


def test_coverage_pack_rejects_duplicate_references() -> None:
    ref = _preset_ref()

    with pytest.raises(ValueError, match="Duplicate coverage-pack reference"):
        build_coverage_pack(
            coverage_pack_id="CP_DUPLICATE",
            coverage_pack_version="v1",
            coverage_family="process_equipment",
            variant_scope_layer="post_change_requalification",
            authored_source_refs=[ref, dict(ref)],
        )


def test_coverage_pack_rejects_payload_and_source_override_fields() -> None:
    ref = _preset_ref()
    ref["asset_payload"] = {"selector": "payload"}

    with pytest.raises(ValueError, match="asset_payload is not allowed"):
        validate_coverage_pack_reference(ref)

    pack = _coverage_pack()
    pack["source_truth_override"] = True

    with pytest.raises(ValueError, match="source_truth_override is not allowed"):
        validate_coverage_pack(pack)


def test_coverage_pack_rejects_compiled_reference_as_source_authority() -> None:
    ref = _compiled_preset_ref()
    ref["compiled_lookup_is_source_authority"] = True

    with pytest.raises(ValueError, match="source authority"):
        validate_coverage_pack_reference(ref)


def test_coverage_pack_rejects_compiled_ref_without_included_source_link() -> None:
    compiled = build_deployment_compiled_ref(
        asset_family=PRESET_ASSET_FAMILY,
        asset_id="PE_RELOCATION_SELECTOR",
        asset_version="v1",
        compiled_record_ref="compiled://presets/PE_RELOCATION_SELECTOR@v1",
        compiled_surface_id="deployment-compiled://presets/v1",
        source_record_ref="authored://presets/MISSING_SELECTOR@v1",
    )

    with pytest.raises(ValueError, match="included authored source_record_ref"):
        build_coverage_pack(
            coverage_pack_id="CP_MISSING_SOURCE_LINK",
            coverage_pack_version="v1",
            coverage_family="process_equipment",
            variant_scope_layer="post_change_requalification",
            authored_source_refs=[_preset_ref()],
            deployment_compiled_refs=[compiled],
        )


def test_coverage_pack_rejects_wrong_family_in_standards_ref_list() -> None:
    with pytest.raises(ValueError, match="standards_bundle_refs contains invalid"):
        build_coverage_pack(
            coverage_pack_id="CP_WRONG_STANDARDS_REF",
            coverage_pack_version="v1",
            coverage_family="process_equipment",
            variant_scope_layer="post_change_requalification",
            authored_source_refs=[_preset_ref()],
            standards_bundle_refs=[_task_pool_ref()],
        )
