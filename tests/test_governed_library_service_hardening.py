import pytest

from asbp.governed_library import (
    GOVERNED_LIBRARY_SERVICE_HARDENING_CHECKPOINT_ID,
    GOVERNED_LIBRARY_SERVICE_HARDENING_CONTRACT_VERSION,
    OPERATION_PREPARE_DOCUMENT_INVOCATION_CONTEXT,
    OPERATION_RESOLVE_GOVERNED_ASSET_CONTEXT,
    PREFLIGHT_VALIDATION_STATUS_VALIDATED,
    RELEASE_STATUS_DRAFT,
    RELEASE_STATUS_FREEZE_CANDIDATE,
    SERVICE_CALLER_BOUNDARY_ORCHESTRATION,
    SERVICE_ENTRY_POINT_ORCHESTRATION,
    build_governed_library_service_request,
    build_library_release_manifest,
    build_library_service_hardening_baseline,
    validate_governed_library_service_request,
    validate_service_preflight_from_release_manifest,
)


def _release_manifest(release_status: str = RELEASE_STATUS_FREEZE_CANDIDATE) -> dict[str, object]:
    return build_library_release_manifest(
        release_manifest_id="M15_7_TEST_RELEASE",
        release_manifest_version="v1",
        release_status=release_status,
        selector_refs=["CS-PE-QUAL@v1", "CS-CSV-DECOM@v1"],
        task_pool_refs=["TP-PE-QUAL@v1", "TP-CSV-DECOM@v1"],
        profile_refs=["PROF-PE-QUAL@v1", "PROF-CSV-DECOM@v1"],
        standards_bundle_refs=["SB-CQV-CORE-EG@v1", "SB-CSV-ADDON@v1"],
        calendar_refs=["CAL-WORKWEEK@v1"],
        planning_basis_refs=["PB-PE-QUAL@v1", "PB-CSV-DECOM@v1"],
        mapping_metadata_refs=["MAP-M15-5@v1"],
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
                "standards_bundle_refs": ["SB-CQV-CORE-EG@v1", "SB-CSV-ADDON@v1"],
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


def test_service_hardening_baseline_exposes_m15_7_rules() -> None:
    baseline = build_library_service_hardening_baseline()

    assert baseline["checkpoint"] == GOVERNED_LIBRARY_SERVICE_HARDENING_CHECKPOINT_ID
    assert baseline["contract_version"] == GOVERNED_LIBRARY_SERVICE_HARDENING_CONTRACT_VERSION
    assert OPERATION_PREPARE_DOCUMENT_INVOCATION_CONTEXT in baseline["supported_operations"]
    assert "runtime migration" in baseline["not_owned_by_m15_7"]


def test_build_governed_library_service_request_accepts_valid_preflight() -> None:
    request = build_governed_library_service_request(
        service_request_id="REQ-001",
        caller_boundary=SERVICE_CALLER_BOUNDARY_ORCHESTRATION,
        entry_point=SERVICE_ENTRY_POINT_ORCHESTRATION,
        requested_operation=OPERATION_RESOLVE_GOVERNED_ASSET_CONTEXT,
        release_manifest=_release_manifest(),
        requested_asset_refs=["CS-PE-QUAL@v1", "TP-PE-QUAL@v1"],
    )

    assert request["checkpoint"] == GOVERNED_LIBRARY_SERVICE_HARDENING_CHECKPOINT_ID
    assert request["preflight_validation_status"] == PREFLIGHT_VALIDATION_STATUS_VALIDATED
    assert request["runtime_migration_requested"] is False
    validate_governed_library_service_request(request)


def test_service_preflight_rejects_draft_release_status() -> None:
    with pytest.raises(ValueError, match="release_status"):
        build_governed_library_service_request(
            service_request_id="REQ-DRAFT",
            caller_boundary=SERVICE_CALLER_BOUNDARY_ORCHESTRATION,
            entry_point=SERVICE_ENTRY_POINT_ORCHESTRATION,
            requested_operation=OPERATION_RESOLVE_GOVERNED_ASSET_CONTEXT,
            release_manifest=_release_manifest(RELEASE_STATUS_DRAFT),
            requested_asset_refs=["CS-PE-QUAL@v1"],
        )


def test_service_request_rejects_adapter_leakage_and_unsupported_boundary() -> None:
    request = build_governed_library_service_request(
        service_request_id="REQ-002",
        caller_boundary=SERVICE_CALLER_BOUNDARY_ORCHESTRATION,
        entry_point=SERVICE_ENTRY_POINT_ORCHESTRATION,
        requested_operation=OPERATION_RESOLVE_GOVERNED_ASSET_CONTEXT,
        release_manifest=_release_manifest(),
        requested_asset_refs=["CS-PE-QUAL@v1"],
    )
    request["caller_boundary"] = "cli_adapter"

    with pytest.raises(ValueError, match="unsupported caller_boundary"):
        validate_governed_library_service_request(request)

    request = build_governed_library_service_request(
        service_request_id="REQ-003",
        caller_boundary=SERVICE_CALLER_BOUNDARY_ORCHESTRATION,
        entry_point=SERVICE_ENTRY_POINT_ORCHESTRATION,
        requested_operation=OPERATION_RESOLVE_GOVERNED_ASSET_CONTEXT,
        release_manifest=_release_manifest(),
        requested_asset_refs=["CS-PE-QUAL@v1"],
    )
    request["adapter_owns_lookup"] = True

    with pytest.raises(ValueError, match="adapter_owns_lookup"):
        validate_governed_library_service_request(request)


def test_service_request_rejects_undeclared_requested_asset_ref() -> None:
    with pytest.raises(ValueError, match="not declared"):
        build_governed_library_service_request(
            service_request_id="REQ-MISSING",
            caller_boundary=SERVICE_CALLER_BOUNDARY_ORCHESTRATION,
            entry_point=SERVICE_ENTRY_POINT_ORCHESTRATION,
            requested_operation=OPERATION_RESOLVE_GOVERNED_ASSET_CONTEXT,
            release_manifest=_release_manifest(),
            requested_asset_refs=["CS-PE-MISSING@v1"],
        )


def test_service_request_rejects_runtime_migration_and_free_form_mutation_flags() -> None:
    request = build_governed_library_service_request(
        service_request_id="REQ-FLAG",
        caller_boundary=SERVICE_CALLER_BOUNDARY_ORCHESTRATION,
        entry_point=SERVICE_ENTRY_POINT_ORCHESTRATION,
        requested_operation=OPERATION_PREPARE_DOCUMENT_INVOCATION_CONTEXT,
        release_manifest=_release_manifest(),
        requested_asset_refs=["CS-CSV-DECOM@v1"],
    )
    request["runtime_migration_requested"] = True

    with pytest.raises(ValueError, match="runtime_migration_requested"):
        validate_governed_library_service_request(request)

    request["runtime_migration_requested"] = False
    request["free_form_mutation_requested"] = True

    with pytest.raises(ValueError, match="free_form_mutation_requested"):
        validate_governed_library_service_request(request)


def test_service_preflight_helper_returns_passed_result() -> None:
    result = validate_service_preflight_from_release_manifest(
        release_manifest=_release_manifest(),
        requested_asset_refs=["CS-PE-QUAL@v1", "PROF-PE-QUAL@v1"],
        requested_operation=OPERATION_PREPARE_DOCUMENT_INVOCATION_CONTEXT,
    )

    assert result["preflight_result"] == "passed"
    assert result["requested_operation"] == OPERATION_PREPARE_DOCUMENT_INVOCATION_CONTEXT
