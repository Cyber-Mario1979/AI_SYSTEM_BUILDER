import pytest

from asbp.governed_library import (
    DEPLOYMENT_COMPILED_STATUS_NOT_COMPILED,
    GOVERNED_LIBRARY_RELEASE_CHECKPOINT_ID,
    GOVERNED_LIBRARY_RELEASE_CONTRACT_VERSION,
    RELEASE_STATUS_FREEZE_CANDIDATE,
    RUNTIME_AUTHORITY_STATUS_NOT_AUTHORITY,
    build_library_release_manifest,
    build_library_release_policy_baseline,
    validate_compiled_lookup_candidate,
    validate_library_release_manifest,
)


def _manifest() -> dict[str, object]:
    return build_library_release_manifest(
        release_manifest_id="M15_6_TEST_RELEASE",
        release_manifest_version="v1",
        release_status=RELEASE_STATUS_FREEZE_CANDIDATE,
        selector_refs=[
            "CS-PE-QUAL@v1",
            "CS-CSV-DECOM@v1",
        ],
        task_pool_refs=[
            "TP-PE-QUAL@v1",
            "TP-CSV-DECOM@v1",
        ],
        profile_refs=[
            "PROF-PE-QUAL@v1",
            "PROF-CSV-DECOM@v1",
        ],
        standards_bundle_refs=[
            "SB-CQV-CORE-EG@v1",
            "SB-CSV-ADDON@v1",
        ],
        calendar_refs=[
            "CAL-WORKWEEK@v1",
        ],
        planning_basis_refs=[
            "PB-PE-QUAL@v1",
            "PB-CSV-DECOM@v1",
        ],
        mapping_metadata_refs=[
            "MAP-M15-5@v1",
        ],
        link_records=[
            {
                "selector_ref": "CS-PE-QUAL@v1",
                "task_pool_ref": "TP-PE-QUAL@v1",
                "profile_ref": "PROF-PE-QUAL@v1",
                "calendar_ref": "CAL-WORKWEEK@v1",
                "standards_bundle_refs": ["SB-CQV-CORE-EG@v1"],
                "planning_basis_ref": "PB-PE-QUAL@v1",
            },
            {
                "selector_ref": "CS-CSV-DECOM@v1",
                "task_pool_ref": "TP-CSV-DECOM@v1",
                "profile_ref": "PROF-CSV-DECOM@v1",
                "calendar_ref": "CAL-WORKWEEK@v1",
                "standards_bundle_refs": [
                    "SB-CQV-CORE-EG@v1",
                    "SB-CSV-ADDON@v1",
                ],
                "planning_basis_ref": "PB-CSV-DECOM@v1",
            },
        ],
        task_profile_key_mappings=[
            {
                "task_pool_ref": "TP-PE-QUAL@v1",
                "task_segment": "SCOPE",
                "profile_key": "PEQUAL_SCOPE_DUR",
                "profile_ref": "PROF-PE-QUAL@v1",
            },
            {
                "task_pool_ref": "TP-CSV-DECOM@v1",
                "task_segment": "PLAN",
                "profile_key": "CSVDEC_PLAN_DUR",
                "profile_ref": "PROF-CSV-DECOM@v1",
            },
        ],
        document_obligation_mappings=[
            {
                "task_pool_ref": "TP-PE-QUAL@v1",
                "document_family_obligations": ["RA", "RTM", "Report/VSR"],
            },
            {
                "task_pool_ref": "TP-CSV-DECOM@v1",
                "document_family_obligations": [
                    "Decommissioning plan",
                    "Data retention / DI evidence",
                    "Closure approval",
                ],
            },
        ],
    )


def test_library_release_policy_baseline_exposes_m15_6_rules() -> None:
    baseline = build_library_release_policy_baseline()

    assert baseline["checkpoint"] == GOVERNED_LIBRARY_RELEASE_CHECKPOINT_ID
    assert baseline["contract_version"] == GOVERNED_LIBRARY_RELEASE_CONTRACT_VERSION
    assert baseline["runtime_authority_status"] == RUNTIME_AUTHORITY_STATUS_NOT_AUTHORITY
    assert baseline["deployment_compiled_status"] == DEPLOYMENT_COMPILED_STATUS_NOT_COMPILED
    assert "taxonomy_identity_rules" in baseline
    assert "cross_library_linkage_rules" in baseline
    assert "runtime migration" in baseline["not_owned_by_m15_6"]


def test_build_library_release_manifest_accepts_complete_linked_manifest() -> None:
    manifest = _manifest()

    assert manifest["release_manifest_ref"] == "M15_6_TEST_RELEASE@v1"
    assert manifest["release_status"] == RELEASE_STATUS_FREEZE_CANDIDATE
    assert manifest["runtime_authority_status"] == RUNTIME_AUTHORITY_STATUS_NOT_AUTHORITY
    assert manifest["deployment_compiled_status"] == DEPLOYMENT_COMPILED_STATUS_NOT_COMPILED
    validate_library_release_manifest(manifest)


def test_library_release_manifest_rejects_latest_current_and_unversioned_refs() -> None:
    manifest = _manifest()
    manifest["selector_refs"] = ["CS-PE-QUAL@latest", "CS-CSV-DECOM@v1"]

    with pytest.raises(ValueError, match="latest/current/wildcard"):
        validate_library_release_manifest(manifest)

    manifest = _manifest()
    manifest["task_pool_refs"] = ["TP-PE-QUAL", "TP-CSV-DECOM@v1"]

    with pytest.raises(ValueError, match="exactly one '@'"):
        validate_library_release_manifest(manifest)


def test_library_release_manifest_rejects_legacy_cs_computerized_system_refs() -> None:
    manifest = _manifest()
    manifest["selector_refs"] = ["CS-CS-E2E@v1", "CS-CSV-DECOM@v1"]

    with pytest.raises(ValueError, match="Legacy computerized-system CS refs"):
        validate_library_release_manifest(manifest)


def test_library_release_manifest_rejects_undeclared_cross_library_links() -> None:
    manifest = _manifest()
    manifest["link_records"][0]["profile_ref"] = "PROF-PE-MISSING@v1"  # type: ignore[index]

    with pytest.raises(ValueError, match="undeclared governed library ref"):
        validate_library_release_manifest(manifest)


def test_library_release_manifest_rejects_runtime_authority_override() -> None:
    manifest = _manifest()
    manifest["runtime_authority_status"] = "runtime_authority"

    with pytest.raises(ValueError, match="runtime_authority_status"):
        validate_library_release_manifest(manifest)


def test_compiled_lookup_candidate_requires_source_link_and_non_authority() -> None:
    validate_compiled_lookup_candidate(
        compiled_ref="COMPILED-TP-PE-QUAL@v1",
        source_ref="TP-PE-QUAL@v1",
        authored_source_refs=["TP-PE-QUAL@v1"],
        compiled_lookup_is_source_authority=False,
    )

    with pytest.raises(ValueError, match="included authored source ref"):
        validate_compiled_lookup_candidate(
            compiled_ref="COMPILED-TP-PE-QUAL@v1",
            source_ref="TP-PE-MISSING@v1",
            authored_source_refs=["TP-PE-QUAL@v1"],
            compiled_lookup_is_source_authority=False,
        )

    with pytest.raises(ValueError, match="must not be source authority"):
        validate_compiled_lookup_candidate(
            compiled_ref="COMPILED-TP-PE-QUAL@v1",
            source_ref="TP-PE-QUAL@v1",
            authored_source_refs=["TP-PE-QUAL@v1"],
            compiled_lookup_is_source_authority=True,
        )
