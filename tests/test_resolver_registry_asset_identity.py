import pytest

from asbp.resolver_registry import (
    CALENDAR_ASSET_FAMILY,
    DEFERRED_RESOLUTION_ASSET_FAMILIES,
    GOVERNED_ASSET_CONTENT_POLICY,
    GOVERNED_ASSET_LOOKUP_FAILURE_POLICY,
    GOVERNED_ASSET_LOOKUP_ROLE,
    GOVERNED_ASSET_SOURCE_AUTHORITY_ROLE,
    GOVERNED_ASSET_VERSION_PIN_POLICY,
    MAPPING_METADATA_ASSET_FAMILY,
    PLANNING_BASIS_ASSET_FAMILY,
    PRESET_ASSET_FAMILY,
    PROFILE_ASSET_FAMILY,
    RESOLVER_REGISTRY_LOOKUP_CHECKPOINT_ID,
    RESOLVER_REGISTRY_LOOKUP_CONTRACT_VERSION,
    RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY,
    STANDARDS_BUNDLE_ASSET_FAMILY,
    SUPPORTED_VERSION_PINNED_GOVERNED_ASSET_FAMILIES,
    TASK_POOL_ASSET_FAMILY,
    TEMPLATE_ASSET_FAMILY,
    build_governed_asset_identity,
    build_governed_asset_identity_baseline,
    build_governed_asset_lookup_entry,
    build_governed_asset_lookup_key,
    build_governed_asset_registry,
    build_version_pinned_asset_ref,
    parse_version_pinned_asset_ref,
    resolve_version_pinned_governed_asset,
    validate_governed_asset_identity,
    validate_governed_asset_lookup_entry,
)


def _entry() -> dict[str, object]:
    return build_governed_asset_lookup_entry(
        asset_family=TEMPLATE_ASSET_FAMILY,
        asset_id="urs_template",
        asset_version="V1",
        asset_record_ref="governed://templates/URS_TEMPLATE/v1",
    )


def test_build_governed_asset_identity_baseline_exposes_m14_2_rules() -> None:
    baseline = build_governed_asset_identity_baseline()

    assert baseline["checkpoint"] == RESOLVER_REGISTRY_LOOKUP_CHECKPOINT_ID
    assert baseline["contract_version"] == RESOLVER_REGISTRY_LOOKUP_CONTRACT_VERSION
    assert TEMPLATE_ASSET_FAMILY in baseline["supported_version_pinned_asset_families"]
    assert PRESET_ASSET_FAMILY in baseline["supported_version_pinned_asset_families"]
    assert TASK_POOL_ASSET_FAMILY in baseline["supported_version_pinned_asset_families"]
    assert STANDARDS_BUNDLE_ASSET_FAMILY in baseline["supported_version_pinned_asset_families"]
    assert PROFILE_ASSET_FAMILY in baseline["supported_version_pinned_asset_families"]
    assert MAPPING_METADATA_ASSET_FAMILY in baseline["supported_version_pinned_asset_families"]
    assert CALENDAR_ASSET_FAMILY in baseline["deferred_resolution_asset_families"]
    assert PLANNING_BASIS_ASSET_FAMILY in baseline["deferred_resolution_asset_families"]
    assert baseline["lookup_role"] == GOVERNED_ASSET_LOOKUP_ROLE
    assert baseline["version_pin_policy"] == GOVERNED_ASSET_VERSION_PIN_POLICY
    assert baseline["content_policy"] == GOVERNED_ASSET_CONTENT_POLICY


def test_supported_and_deferred_family_sets_preserve_m14_boundary() -> None:
    assert SUPPORTED_VERSION_PINNED_GOVERNED_ASSET_FAMILIES == (
        TEMPLATE_ASSET_FAMILY,
        PRESET_ASSET_FAMILY,
        TASK_POOL_ASSET_FAMILY,
        STANDARDS_BUNDLE_ASSET_FAMILY,
        PROFILE_ASSET_FAMILY,
        MAPPING_METADATA_ASSET_FAMILY,
    )
    assert DEFERRED_RESOLUTION_ASSET_FAMILIES == (
        CALENDAR_ASSET_FAMILY,
        PLANNING_BASIS_ASSET_FAMILY,
    )


def test_build_version_pinned_asset_ref_normalizes_id_and_version() -> None:
    assert (
        build_version_pinned_asset_ref(
            asset_id="urs_template",
            asset_version="V1",
        )
        == "URS_TEMPLATE@v1"
    )


def test_parse_version_pinned_asset_ref_requires_single_separator() -> None:
    parsed = parse_version_pinned_asset_ref("URS_TEMPLATE@v1")

    assert parsed == {
        "asset_id": "URS_TEMPLATE",
        "asset_version": "v1",
        "asset_ref": "URS_TEMPLATE@v1",
    }

    with pytest.raises(ValueError, match="exactly one '@'"):
        parse_version_pinned_asset_ref("URS_TEMPLATE")


def test_build_governed_asset_lookup_key_uses_family_ref_and_version() -> None:
    assert (
        build_governed_asset_lookup_key(
            asset_family=TEMPLATE_ASSET_FAMILY,
            asset_id="urs_template",
            asset_version="v1",
        )
        == "template:URS_TEMPLATE@v1"
    )


def test_build_governed_asset_identity_returns_canonical_shape() -> None:
    identity = build_governed_asset_identity(
        asset_family=TEMPLATE_ASSET_FAMILY,
        asset_id="urs_template",
        asset_version="V1",
    )

    assert identity["checkpoint"] == RESOLVER_REGISTRY_LOOKUP_CHECKPOINT_ID
    assert identity["contract_version"] == RESOLVER_REGISTRY_LOOKUP_CONTRACT_VERSION
    assert identity["asset_family"] == TEMPLATE_ASSET_FAMILY
    assert identity["asset_id"] == "URS_TEMPLATE"
    assert identity["asset_version"] == "v1"
    assert identity["asset_ref"] == "URS_TEMPLATE@v1"
    assert identity["lookup_key"] == "template:URS_TEMPLATE@v1"
    assert identity["lookup_role"] == GOVERNED_ASSET_LOOKUP_ROLE
    assert identity["source_authority_role"] == GOVERNED_ASSET_SOURCE_AUTHORITY_ROLE
    assert identity["source_truth_policy"] == RESOLVER_REGISTRY_SOURCE_TRUTH_POLICY
    assert identity["version_pin_policy"] == GOVERNED_ASSET_VERSION_PIN_POLICY
    assert identity["failure_policy"] == GOVERNED_ASSET_LOOKUP_FAILURE_POLICY
    assert identity["content_policy"] == GOVERNED_ASSET_CONTENT_POLICY


def test_validate_governed_asset_identity_rejects_latest_current_and_wildcards() -> None:
    for invalid_version in ("latest", "current", "*"):
        with pytest.raises(ValueError, match="explicit pinned version"):
            build_governed_asset_identity(
                asset_family=TEMPLATE_ASSET_FAMILY,
                asset_id="URS_TEMPLATE",
                asset_version=invalid_version,
            )


def test_validate_governed_asset_identity_rejects_noncanonical_identity_mutation() -> None:
    identity = build_governed_asset_identity(
        asset_family=TEMPLATE_ASSET_FAMILY,
        asset_id="URS_TEMPLATE",
        asset_version="v1",
    )
    identity["asset_ref"] = "URS_TEMPLATE@v2"

    with pytest.raises(ValueError, match="invalid asset_ref"):
        validate_governed_asset_identity(identity)


def test_build_lookup_entry_keeps_payload_out_of_m14_2_result() -> None:
    entry = _entry()

    assert entry["lookup_key"] == "template:URS_TEMPLATE@v1"
    assert entry["asset_record_ref"] == "governed://templates/URS_TEMPLATE/v1"
    assert entry["content_policy"] == GOVERNED_ASSET_CONTENT_POLICY
    validate_governed_asset_lookup_entry(entry)


def test_validate_lookup_entry_rejects_payload_or_resolver_bypass() -> None:
    entry = _entry()
    entry["asset_payload"] = {"unsafe": "payload"}

    with pytest.raises(ValueError, match="asset_payload is not allowed"):
        validate_governed_asset_lookup_entry(entry)

    entry = _entry()
    entry["resolver_bypass"] = True

    with pytest.raises(ValueError, match="resolver_bypass is not allowed"):
        validate_governed_asset_lookup_entry(entry)


def test_build_registry_rejects_duplicate_lookup_key() -> None:
    entry = _entry()
    duplicate = dict(entry)

    with pytest.raises(ValueError, match="Duplicate governed asset lookup entry"):
        build_governed_asset_registry([entry, duplicate])


def test_resolve_version_pinned_governed_asset_returns_identity_resolution_only() -> None:
    registry = build_governed_asset_registry([_entry()])

    resolution = resolve_version_pinned_governed_asset(
        registry=registry,
        asset_family=TEMPLATE_ASSET_FAMILY,
        asset_id="urs_template",
        asset_version="v1",
        caller_context_ref="document_engine",
    )

    assert resolution["lookup_result"] == "resolved"
    assert resolution["caller_context_ref"] == "document_engine"
    assert resolution["resolved_lookup_key"] == "template:URS_TEMPLATE@v1"
    assert resolution["asset_record_ref"] == "governed://templates/URS_TEMPLATE/v1"
    assert resolution["asset_payload_included"] is False
    assert resolution["resolved_identity"]["asset_ref"] == "URS_TEMPLATE@v1"


def test_resolve_version_pinned_governed_asset_fails_closed_when_missing() -> None:
    registry = build_governed_asset_registry([_entry()])

    with pytest.raises(ValueError, match="failed closed"):
        resolve_version_pinned_governed_asset(
            registry=registry,
            asset_family=TEMPLATE_ASSET_FAMILY,
            asset_id="URS_TEMPLATE",
            asset_version="v2",
            caller_context_ref="document_engine",
        )


def test_version_pinned_lookup_defers_calendar_and_planning_basis_to_m14_3() -> None:
    for deferred_family in (CALENDAR_ASSET_FAMILY, PLANNING_BASIS_ASSET_FAMILY):
        with pytest.raises(ValueError, match="deferred to a later resolver checkpoint"):
            build_governed_asset_identity(
                asset_family=deferred_family,
                asset_id="DEFAULT",
                asset_version="v1",
            )
