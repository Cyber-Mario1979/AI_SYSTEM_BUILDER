import pytest
from pydantic import ValidationError

from asbp.standards_citation_model import (
    StandardsCitationContractModel,
    StandardsCitationRecordModel,
    StandardsCitationSourceRecordModel,
)


def _verified_annex_15_source() -> StandardsCitationSourceRecordModel:
    return StandardsCitationSourceRecordModel(
        std_id="STD-EU-GMP-ANNEX-15",
        registry_version="v0.1",
        source_name="EU GMP Annex 15",
        authority_status="authoritative",
        verification_status="verified",
        version_or_effective_date="verified-test-version",
        available_citation_depths=["document", "version", "section", "clause"],
        available_section_refs=["1"],
        available_clause_refs=["1.1"],
        source_location="controlled-test-source",
    )


def _pending_annex_11_source() -> StandardsCitationSourceRecordModel:
    return StandardsCitationSourceRecordModel(
        std_id="STD-EU-GMP-ANNEX-11",
        registry_version="v0.1",
        source_name="EU GMP Annex 11",
        authority_status="authoritative",
        verification_status="pending_verification",
        version_or_effective_date="TBD",
        available_citation_depths=["document", "version"],
        source_limitations=[
            "Version, effective date, and clause references are pending verification."
        ],
    )


def _local_cleanroom_source() -> StandardsCitationSourceRecordModel:
    return StandardsCitationSourceRecordModel(
        std_id="STD-LOCAL-CLEANROOM-NONSTERILE",
        registry_version="v0.1",
        source_name="Local non-sterile cleanroom matrix",
        authority_status="tbd",
        verification_status="user_provided",
        version_or_effective_date="TBD",
        available_citation_depths=["document", "table_row", "requirement"],
        available_table_rows=["LOCAL-CR-002"],
        available_requirement_ids=["LOCAL-CR-002"],
        source_limitations=[
            "User-provided local matrix is not approved as internal authority."
        ],
    )


def _valid_clause_citation() -> StandardsCitationRecordModel:
    return StandardsCitationRecordModel(
        citation_id="CIT-EU-GMP-ANNEX-15-CLAUSE@v1",
        source=_verified_annex_15_source(),
        reference={
            "citation_level": "clause",
            "clause_ref": "1.1",
        },
        applicability_decision_id="APP-EU-GMP-ANNEX-15-QUALIFICATION@v1",
        citation_context="source_traceability",
        downstream_use_limits=[
            "Citation does not include controlled source text."
        ],
    )


def _required_non_implementation_claims() -> list[str]:
    return [
        "does_not_parse_runtime_registry",
        "does_not_implement_standards_retrieval_or_embedding",
        "does_not_generate_product_ready_standards_output",
        "does_not_claim_audit_ready_clause_authority",
        "does_not_store_or_fabricate_source_text",
        "does_not_interpret_regulatory_meaning",
        "does_not_close_ddr_005_or_ddr_006",
    ]


def test_citation_contract_accepts_verified_clause_citation():
    contract = StandardsCitationContractModel(
        contract_id="M28_3_STANDARDS_CITATION_CONTRACT@v1",
        version="v1",
        registry_version="v0.1",
        citation_records=[_valid_clause_citation()],
        contract_controls=[
            "Citation depth must not exceed verified source evidence."
        ],
        explicit_non_implementation_claims=_required_non_implementation_claims(),
    )

    assert contract.contract_id == "M28_3_STANDARDS_CITATION_CONTRACT@v1"
    assert contract.citation_records[0].reference.citation_level == "clause"


def test_clause_citation_requires_available_verified_clause_reference():
    with pytest.raises(ValidationError) as exc_info:
        StandardsCitationRecordModel(
            citation_id="CIT-EU-GMP-ANNEX-15-UNKNOWN-CLAUSE@v1",
            source=_verified_annex_15_source(),
            reference={
                "citation_level": "clause",
                "clause_ref": "99.99",
            },
            citation_context="source_traceability",
        )

    assert "Clause-level citation requires an available verified clause reference" in str(
        exc_info.value
    )


def test_section_citation_rejects_fabricated_section_reference():
    with pytest.raises(ValidationError) as exc_info:
        StandardsCitationRecordModel(
            citation_id="CIT-EU-GMP-ANNEX-15-UNKNOWN-SECTION@v1",
            source=_verified_annex_15_source(),
            reference={
                "citation_level": "section",
                "section_ref": "9",
            },
            citation_context="source_traceability",
        )

    assert "Section-level citation requires an available verified section reference" in str(
        exc_info.value
    )


def test_limited_source_requires_visible_citation_limitations():
    with pytest.raises(ValidationError) as exc_info:
        StandardsCitationRecordModel(
            citation_id="CIT-EU-GMP-ANNEX-11-DOCUMENT@v1",
            source=_pending_annex_11_source(),
            reference={
                "citation_level": "document",
            },
            citation_context="planning",
        )

    assert "Limited standards sources require visible citation limitations" in str(
        exc_info.value
    )


def test_missing_requested_clause_depth_requires_visible_limitation():
    with pytest.raises(ValidationError) as exc_info:
        StandardsCitationRecordModel(
            citation_id="CIT-EU-GMP-ANNEX-15-MISSING-CLAUSE@v1",
            source=_verified_annex_15_source(),
            reference={
                "citation_level": "document",
                "requested_citation_depth": "clause",
            },
            citation_context="planning",
        )

    assert "Missing requested citation depth requires visible limitation" in str(
        exc_info.value
    )


def test_requirement_level_user_provided_source_can_be_traced_with_limitations():
    citation = StandardsCitationRecordModel(
        citation_id="CIT-LOCAL-CLEANROOM-REQ@v1",
        source=_local_cleanroom_source(),
        reference={
            "citation_level": "requirement",
            "requirement_id": "LOCAL-CR-002",
        },
        citation_context="planning",
        limitation_statements=[
            "Local matrix is user-provided and not approved as internal authority."
        ],
        limitation_acceptance="visible_limitation",
        downstream_use_limits=[
            "May support planning only until internal authority is approved."
        ],
    )

    assert citation.reference.requirement_id == "LOCAL-CR-002"
    assert citation.limitation_acceptance == "visible_limitation"


def test_audit_ready_citation_blocked_for_pending_source():
    with pytest.raises(ValidationError) as exc_info:
        StandardsCitationRecordModel(
            citation_id="CIT-EU-GMP-ANNEX-11-AUDIT@v1",
            source=_pending_annex_11_source(),
            reference={
                "citation_level": "document",
            },
            citation_context="planning",
            limitation_statements=[
                "Version and clause references are pending verification."
            ],
            limitation_acceptance="visible_limitation",
            audit_ready_claimed=True,
        )

    assert "Audit-ready citation is not allowed for limited standards source" in str(
        exc_info.value
    )


def test_source_text_claims_are_rejected():
    with pytest.raises(ValidationError) as exc_info:
        StandardsCitationRecordModel(
            citation_id="CIT-EU-GMP-ANNEX-15-SOURCE-TEXT@v1",
            source=_verified_annex_15_source(),
            reference={
                "citation_level": "document",
            },
            citation_context="source_traceability",
            source_text_claim="Synthetic controlled source text must not be carried.",
        )

    assert "M28.3 citation records must not carry source text claims" in str(
        exc_info.value
    )


def test_contract_requires_explicit_non_implementation_claims():
    with pytest.raises(ValidationError) as exc_info:
        StandardsCitationContractModel(
            contract_id="M28_3_STANDARDS_CITATION_CONTRACT@v1",
            version="v1",
            registry_version="v0.1",
            citation_records=[_valid_clause_citation()],
            contract_controls=[
                "Citation depth must not exceed verified source evidence."
            ],
            explicit_non_implementation_claims=[
                "does_not_parse_runtime_registry",
            ],
        )

    assert "M28.3 contract is missing explicit non-implementation claims" in str(
        exc_info.value
    )
