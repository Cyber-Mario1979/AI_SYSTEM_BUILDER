import pytest

from asbp.ai_runtime import (
    AI_RUNTIME_BOUNDARY_CHECKPOINT_ID,
    AI_RUNTIME_BOUNDARY_CONTRACT_VERSION,
    AI_RUNTIME_BOUNDARY_STATUS_VALIDATED,
    BOUNDED_SUMMARIZATION_PROFILE,
    CANDIDATE_LANGUAGE_OUTPUT_ROLE,
    CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
    DOCUMENT_ENGINE_CALLER_BOUNDARY,
    EXPORT_ENGINE_CALLER_BOUNDARY,
    GOVERNED_DOCUMENT_JOB_FAMILY,
    GOVERNED_REPORTING_JOB_FAMILY,
    ORCHESTRATION_SERVICE_CALLER_BOUNDARY,
    build_ai_runtime_boundary_baseline,
    build_ai_runtime_entry_request,
    validate_ai_runtime_blocked_state,
    validate_ai_runtime_entry_request,
)


def _document_request() -> dict[str, object]:
    return build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-DOC-001",
        job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
        caller_boundary=DOCUMENT_ENGINE_CALLER_BOUNDARY,
        model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
        governed_source_refs=[
            "DOCUMENT-INPUT-CONTRACT@v1",
            "TEMPLATE-URS@v1",
            "STANDARDS-GUARDRAILS@v1",
        ],
        engine_contract_refs=[
            "DOCUMENT-REQUEST-CONTRACT@v1",
            "DOCUMENT-OUTPUT-CONTRACT@v1",
        ],
    )


def test_ai_runtime_boundary_baseline_exposes_m16_1_rules() -> None:
    baseline = build_ai_runtime_boundary_baseline()

    assert baseline["checkpoint"] == AI_RUNTIME_BOUNDARY_CHECKPOINT_ID
    assert baseline["contract_version"] == AI_RUNTIME_BOUNDARY_CONTRACT_VERSION
    assert GOVERNED_DOCUMENT_JOB_FAMILY in baseline["supported_job_families"]
    assert GOVERNED_REPORTING_JOB_FAMILY in baseline["supported_job_families"]
    assert "actual_llm_calls" in baseline["not_owned_by_m16_1"]
    assert "own_execution_truth" in baseline["prohibited_ai_actions"]


def test_build_ai_runtime_entry_request_accepts_governed_document_job() -> None:
    request = _document_request()

    assert request["checkpoint"] == AI_RUNTIME_BOUNDARY_CHECKPOINT_ID
    assert request["runtime_boundary_status"] == AI_RUNTIME_BOUNDARY_STATUS_VALIDATED
    assert request["requested_output_role"] == CANDIDATE_LANGUAGE_OUTPUT_ROLE
    assert request["ai_can_mutate_state"] is False
    validate_ai_runtime_entry_request(request)


def test_build_ai_runtime_entry_request_accepts_governed_reporting_job() -> None:
    request = build_ai_runtime_entry_request(
        ai_runtime_request_id="AIRUN-REP-001",
        job_family=GOVERNED_REPORTING_JOB_FAMILY,
        caller_boundary=EXPORT_ENGINE_CALLER_BOUNDARY,
        model_permission_profile=BOUNDED_SUMMARIZATION_PROFILE,
        governed_source_refs=[
            "REPORTING-EXPORT-PAYLOAD@v1",
            "EXPORT-INVOCATION-REQUEST@v1",
        ],
        engine_contract_refs=[
            "EXPORT-REQUEST-CONTRACT@v1",
            "REPORTING-SURFACE-CONTRACT@v1",
        ],
    )

    assert request["job_family"] == GOVERNED_REPORTING_JOB_FAMILY
    validate_ai_runtime_entry_request(request)


def test_ai_runtime_entry_request_rejects_adapter_and_free_form_boundaries() -> None:
    with pytest.raises(ValueError, match="unsupported caller_boundary"):
        build_ai_runtime_entry_request(
            ai_runtime_request_id="AIRUN-BAD-BOUNDARY",
            job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
            caller_boundary="cli_adapter",
            model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
            governed_source_refs=["DOCUMENT-INPUT-CONTRACT@v1"],
            engine_contract_refs=["DOCUMENT-REQUEST-CONTRACT@v1"],
        )

    with pytest.raises(ValueError, match="unsupported caller_boundary"):
        build_ai_runtime_entry_request(
            ai_runtime_request_id="AIRUN-FREE-FORM",
            job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
            caller_boundary="free_form_chat",
            model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
            governed_source_refs=["DOCUMENT-INPUT-CONTRACT@v1"],
            engine_contract_refs=["DOCUMENT-REQUEST-CONTRACT@v1"],
        )


def test_ai_runtime_entry_request_rejects_unversioned_and_latest_refs() -> None:
    with pytest.raises(ValueError, match="exactly one '@'"):
        build_ai_runtime_entry_request(
            ai_runtime_request_id="AIRUN-UNVERSIONED",
            job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
            caller_boundary=DOCUMENT_ENGINE_CALLER_BOUNDARY,
            model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
            governed_source_refs=["DOCUMENT-INPUT-CONTRACT"],
            engine_contract_refs=["DOCUMENT-REQUEST-CONTRACT@v1"],
        )

    with pytest.raises(ValueError, match="latest/current/wildcard"):
        build_ai_runtime_entry_request(
            ai_runtime_request_id="AIRUN-LATEST",
            job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
            caller_boundary=DOCUMENT_ENGINE_CALLER_BOUNDARY,
            model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
            governed_source_refs=["DOCUMENT-INPUT-CONTRACT@latest"],
            engine_contract_refs=["DOCUMENT-REQUEST-CONTRACT@v1"],
        )


def test_ai_runtime_entry_request_rejects_missing_engine_contract_truth() -> None:
    with pytest.raises(ValueError, match="engine_contract_refs"):
        build_ai_runtime_entry_request(
            ai_runtime_request_id="AIRUN-NO-CONTRACT",
            job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
            caller_boundary=DOCUMENT_ENGINE_CALLER_BOUNDARY,
            model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
            governed_source_refs=["DOCUMENT-INPUT-CONTRACT@v1"],
            engine_contract_refs=[],
        )


def test_ai_runtime_entry_request_rejects_wrong_contract_family() -> None:
    with pytest.raises(ValueError, match="engine contract ref aligned"):
        build_ai_runtime_entry_request(
            ai_runtime_request_id="AIRUN-WRONG-CONTRACT",
            job_family=GOVERNED_DOCUMENT_JOB_FAMILY,
            caller_boundary=DOCUMENT_ENGINE_CALLER_BOUNDARY,
            model_permission_profile=CONTROLLED_LANGUAGE_DRAFTING_PROFILE,
            governed_source_refs=["DOCUMENT-INPUT-CONTRACT@v1"],
            engine_contract_refs=["EXPORT-REQUEST-CONTRACT@v1"],
        )


def test_ai_runtime_entry_request_rejects_execution_truth_or_state_mutation_flags() -> None:
    request = _document_request()
    request["ai_owns_execution_truth"] = True

    with pytest.raises(ValueError, match="ai_owns_execution_truth"):
        validate_ai_runtime_entry_request(request)

    request = _document_request()
    request["ai_can_mutate_state"] = True

    with pytest.raises(ValueError, match="ai_can_mutate_state"):
        validate_ai_runtime_entry_request(request)


def test_ai_runtime_blocked_state_rejects_direct_prompt_and_evidence_invention() -> None:
    request = _document_request()
    request["direct_user_prompt_as_source_truth"] = True

    with pytest.raises(ValueError, match="direct_user_prompt_as_source_truth"):
        validate_ai_runtime_blocked_state(request)

    request = _document_request()
    request["ai_can_invent_evidence"] = True

    with pytest.raises(ValueError, match="ai_can_invent_evidence"):
        validate_ai_runtime_blocked_state(request)


def test_ai_runtime_entry_request_rejects_actual_prompt_or_llm_fields() -> None:
    request = _document_request()
    request["prompt_template"] = "write a report"

    with pytest.raises(ValueError, match="prompt_template"):
        validate_ai_runtime_entry_request(request)

    request = _document_request()
    request["direct_llm_call"] = True

    with pytest.raises(ValueError, match="direct_llm_call"):
        validate_ai_runtime_entry_request(request)
