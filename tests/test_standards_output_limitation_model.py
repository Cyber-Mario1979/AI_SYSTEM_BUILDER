import pytest
from pydantic import ValidationError

from asbp.standards_output_limitation_model import (
    StandardsOutputLimitationContractModel,
    StandardsOutputLimitationRecordModel,
    StandardsOutputSourceLimitationModel,
)


def _verified_annex_15_source() -> StandardsOutputSourceLimitationModel:
    return StandardsOutputSourceLimitationModel(
        std_id="STD-EU-GMP-ANNEX-15",
        registry_version="v0.1",
        authority_status="authoritative",
        verification_status="verified",
        mandatory_flag="mandatory_when_applicable",
        version_or_effective_date="Annex 15 verified baseline",
        available_citation_depths=["document", "section"],
        requested_citation_depth="section",
        rendered_citation_depth="section",
    )


def _pending_annex_15_source() -> StandardsOutputSourceLimitationModel:
    return StandardsOutputSourceLimitationModel(
        std_id="STD-EU-GMP-ANNEX-15",
        registry_version="v0.1",
        authority_status="authoritative",
        verification_status="pending_verification",
        mandatory_flag="mandatory_when_applicable",
        version_or_effective_date="TBD",
        available_citation_depths=["document"],
        requested_citation_depth="clause",
        rendered_citation_depth="document",
        source_limitations=[
            "Version/effective date and clause references are pending verification."
        ],
        limitation_statements=[
            "Rendered citation is document-level only because clause evidence is unavailable."
        ],
        warning_text="Source is pending verification; do not treat this as audit-ready.",
        warning_visibility="visible",
    )


def _reference_iso_source() -> StandardsOutputSourceLimitationModel:
    return StandardsOutputSourceLimitationModel(
        std_id="STD-ISO-14644",
        registry_version="v0.1",
        authority_status="reference",
        verification_status="pending_verification",
        mandatory_flag="not_mandatory_unless_adopted",
        version_or_effective_date="TBD",
        available_citation_depths=["document"],
        requested_citation_depth="section",
        rendered_citation_depth="document",
        source_limitations=[
            "Reference source remains pending verification and adoption."
        ],
        limitation_statements=[
            "Reference source cannot drive mandatory output unless adopted."
        ],
        warning_text="ISO 14644 is reference-only unless adopted for the applicable scope.",
        warning_visibility="visible",
    )


def _limited_record() -> StandardsOutputLimitationRecordModel:
    return StandardsOutputLimitationRecordModel(
        limitation_id="LIM-STANDARDS-LIMITED-OUTPUT@v1",
        version="v1",
        output_context="standards_output_future_contract",
        registry_version="v0.1",
        source_limitations=[_pending_annex_15_source(), _reference_iso_source()],
        output_warning_text=(
            "Standards limitations are visible; do not treat pending or reference-only "
            "sources as audit-ready or product-ready output."
        ),
        output_warning_visibility="visible",
        limitation_summary=[
            "Pending, TBD, and reference-only sources remain visibly limited."
        ],
        downstream_use_limits=[
            "Output may support planning only until verification/adoption is complete."
        ],
    )


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_generate_product_ready_standards_output",
        "does_not_implement_standards_retrieval_or_embedding",
        "does_not_render_documents_or_exports",
        "does_not_hide_source_or_citation_limitations",
    ]


def test_output_limitation_contract_accepts_visible_limited_sources():
    contract = StandardsOutputLimitationContractModel(
        contract_id="M28_9_STANDARDS_OUTPUT_LIMITATION_CONTRACT@v1",
        version="v1",
        registry_version="v0.1",
        limitation_records=[_limited_record()],
        contract_controls=[
            "Standards output limitations must remain visible to downstream consumers."
        ],
        explicit_non_implementation_claims=_required_non_implementation_claims(),
    )

    assert contract.registry_version == "v0.1"
    assert contract.limitation_records[0].has_limited_sources() is True


def test_limitation_record_requires_registry_version_traceability():
    payload = _limited_record().model_dump()
    payload.pop("registry_version")

    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputLimitationRecordModel(**payload)

    assert "registry_version" in str(exc_info.value)


def test_limited_source_requires_visible_warning_text():
    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputSourceLimitationModel(
            std_id="STD-EU-GMP-ANNEX-15",
            registry_version="v0.1",
            authority_status="authoritative",
            verification_status="pending_verification",
            mandatory_flag="mandatory_when_applicable",
            version_or_effective_date="TBD",
            available_citation_depths=["document"],
            requested_citation_depth="document",
            rendered_citation_depth="document",
            source_limitations=[
                "Version/effective date is pending verification."
            ],
            limitation_statements=[
                "Document-level citation only."
            ],
        )

    assert "requires visible warning text" in str(exc_info.value)


def test_hidden_source_warning_is_rejected():
    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputSourceLimitationModel(
            std_id="STD-ISO-14644",
            registry_version="v0.1",
            authority_status="reference",
            verification_status="pending_verification",
            mandatory_flag="not_mandatory_unless_adopted",
            version_or_effective_date="TBD",
            available_citation_depths=["document"],
            requested_citation_depth="document",
            rendered_citation_depth="document",
            source_limitations=["Reference source limitation."],
            limitation_statements=["Reference source cannot drive mandatory output."],
            warning_text="Hidden limitation.",
            warning_visibility="hidden",
        )

    assert "must not be hidden" in str(exc_info.value)


def test_pending_source_cannot_claim_audit_ready_output():
    payload = _pending_annex_15_source().model_dump()
    payload["audit_ready_claimed"] = True

    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputSourceLimitationModel(**payload)

    assert "Audit-ready standards output is not allowed for limited source" in str(
        exc_info.value
    )


def test_product_ready_source_claim_is_rejected():
    payload = _verified_annex_15_source().model_dump()
    payload["product_ready_claimed"] = True

    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputSourceLimitationModel(**payload)

    assert "does not support product-ready standards output claims" in str(
        exc_info.value
    )


def test_record_with_limited_sources_requires_visible_output_warning():
    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputLimitationRecordModel(
            limitation_id="LIM-HIDDEN-OUTPUT@v1",
            version="v1",
            output_context="standards_output_future_contract",
            registry_version="v0.1",
            source_limitations=[_pending_annex_15_source()],
            limitation_summary=["Limited source exists."],
        )

    assert "requires visible output warning" in str(exc_info.value)


def test_record_hidden_output_warning_is_rejected():
    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputLimitationRecordModel(
            limitation_id="LIM-HIDDEN-OUTPUT@v1",
            version="v1",
            output_context="standards_output_future_contract",
            registry_version="v0.1",
            source_limitations=[_pending_annex_15_source()],
            output_warning_text="Hidden warning.",
            output_warning_visibility="hidden",
            limitation_summary=["Limited source exists."],
        )

    assert "warning must not be hidden" in str(exc_info.value)


def test_requested_clause_rendered_as_document_requires_limitation():
    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputSourceLimitationModel(
            std_id="STD-EU-GMP-ANNEX-15",
            registry_version="v0.1",
            authority_status="authoritative",
            verification_status="verified",
            mandatory_flag="mandatory_when_applicable",
            version_or_effective_date="Annex 15 verified baseline",
            available_citation_depths=["document", "clause"],
            requested_citation_depth="clause",
            rendered_citation_depth="document",
        )

    assert "requires limitation_statements" in str(exc_info.value)


def test_rendered_clause_for_unverified_source_is_rejected():
    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputSourceLimitationModel(
            std_id="STD-EU-GMP-ANNEX-15",
            registry_version="v0.1",
            authority_status="authoritative",
            verification_status="pending_verification",
            mandatory_flag="mandatory_when_applicable",
            version_or_effective_date="TBD",
            available_citation_depths=["document", "clause"],
            requested_citation_depth="clause",
            rendered_citation_depth="clause",
            source_limitations=["Clause references are pending verification."],
            limitation_statements=["Clause-level output is not verified."],
            warning_text="Do not use clause-level output.",
            warning_visibility="visible",
        )

    assert "requires verified source evidence" in str(exc_info.value)


def test_record_registry_version_must_match_source_registry_versions():
    source = _pending_annex_15_source().model_copy(update={"registry_version": "v0.2"})

    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputLimitationRecordModel(
            limitation_id="LIM-REGISTRY-MISMATCH@v1",
            version="v1",
            output_context="standards_output_future_contract",
            registry_version="v0.1",
            source_limitations=[source],
            output_warning_text="Registry mismatch.",
            output_warning_visibility="visible",
            limitation_summary=["Mismatch should fail."],
        )

    assert "registry_version must match output registry_version" in str(exc_info.value)


def test_contract_requires_explicit_non_implementation_claims():
    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputLimitationContractModel(
            contract_id="M28_9_STANDARDS_OUTPUT_LIMITATION_CONTRACT@v1",
            version="v1",
            registry_version="v0.1",
            limitation_records=[_limited_record()],
            contract_controls=[
                "Standards output limitations must remain visible."
            ],
            explicit_non_implementation_claims=[
                "does_not_generate_product_ready_standards_output"
            ],
        )

    assert "missing explicit non-implementation claims" in str(exc_info.value)


def test_contract_rejects_duplicate_limitation_records():
    record = _limited_record()

    with pytest.raises(ValidationError) as exc_info:
        StandardsOutputLimitationContractModel(
            contract_id="M28_9_STANDARDS_OUTPUT_LIMITATION_CONTRACT@v1",
            version="v1",
            registry_version="v0.1",
            limitation_records=[record, record],
            contract_controls=[
                "Standards output limitations must remain visible."
            ],
            explicit_non_implementation_claims=_required_non_implementation_claims(),
        )

    assert "Duplicate standards output limitation_id" in str(exc_info.value)
