import pytest
from pydantic import ValidationError

from asbp.standards_document_applicability_model import (
    DocumentCitationPolicyLibraryModel,
    DocumentCitationPolicyRecordModel,
    DocumentStandardsApplicabilityMatrixModel,
    DocumentStandardsApplicabilityRecordModel,
)
from asbp.standards_document_applicability_store import (
    assert_document_citation_policy_refs_exist,
    assert_document_standards_applicability_refs_exist,
    get_document_citation_policy_by_ref,
    get_document_standards_applicability_by_ref,
    list_document_citation_policy_refs,
    list_document_standards_applicability_refs,
    load_default_document_citation_policy_library,
    load_default_document_standards_applicability_matrix,
    load_document_citation_policy_library_from_payload,
    load_document_standards_applicability_matrix_from_payload,
)


MUST_HAVE_DOCUMENT_REFS = {
    "CCF",
    "VMP",
    "SIA",
    "URS",
    "VENDOR_DOCS",
    "RA_FMEA",
    "URS_DEVIATION_LIST",
    "RTM",
    "DQ",
    "CP",
    "QP",
    "FAT_PROTOCOL_REPORT",
    "A0_CERTIFICATE",
    "CTOP",
    "A1_CERTIFICATE",
    "SAT_PROTOCOL_REPORT",
    "CR",
    "A2_CERTIFICATE",
    "IQ_PROTOCOL_REPORT",
    "OQ_PROTOCOL_REPORT",
    "PQ_PROTOCOL_REPORT",
    "DEVIATION_INCIDENT_REPORT",
    "CAPA_CLOSURE_FORM",
    "VSR",
    "DECOMMISSIONING_DOCUMENT_SET",
}


def test_document_standards_applicability_matrix_loads_mvp_records():
    matrix = load_default_document_standards_applicability_matrix()

    assert matrix.matrix_id == "M29_DOCUMENT_STANDARDS_APPLICABILITY_MATRIX@v1"
    assert MUST_HAVE_DOCUMENT_REFS <= set(
        list_document_standards_applicability_refs(matrix)
    )

    urs = get_document_standards_applicability_by_ref(matrix, "URS")
    assert "SB-CQV-GMP@v1" in urs.standards_bundle_refs
    assert "document" in urs.allowed_citation_depths
    assert urs.visible_limitation_statements


def test_document_citation_policy_loads_mvp_records():
    policy_library = load_default_document_citation_policy_library()

    assert policy_library.policy_library_id == "M29_DOCUMENT_CITATION_POLICY_LIBRARY@v1"
    assert MUST_HAVE_DOCUMENT_REFS <= set(list_document_citation_policy_refs(policy_library))

    dqi = get_document_citation_policy_by_ref(policy_library, "DQ")
    assert dqi.permitted_citation_depths == ["document"]
    assert "section" in dqi.blocked_citation_depths


def test_all_standards_applicability_records_preserve_visible_limits():
    matrix = load_default_document_standards_applicability_matrix()

    for record in matrix.document_records:
        assert record.visible_limitation_statements
        assert record.allowed_citation_depths == ["document"]
        assert record.mandatory_use_allowed is False
        assert record.audit_ready_claimed is False


def test_all_citation_policies_block_unverified_deep_citation():
    policy_library = load_default_document_citation_policy_library()

    for policy in policy_library.policies:
        assert policy.default_citation_depth == "document"
        assert policy.permitted_citation_depths == ["document"]
        assert {"version", "section", "clause"} <= set(policy.blocked_citation_depths)
        assert policy.source_text_storage_allowed is False
        assert policy.retrieval_or_embedding_allowed is False
        assert policy.mandatory_use_allowed is False
        assert policy.audit_ready_claimed is False


def test_external_or_adopted_docs_do_not_become_standards_backed_templates():
    matrix = load_default_document_standards_applicability_matrix()

    external_refs = {
        "CCF",
        "VENDOR_DOCS",
        "FAT_PROTOCOL_REPORT",
        "A0_CERTIFICATE",
        "CTOP",
        "A1_CERTIFICATE",
        "SAT_PROTOCOL_REPORT",
    }
    for document_ref in external_refs:
        record = get_document_standards_applicability_by_ref(matrix, document_ref)
        assert record.source_mode in {
            "external_or_adopted_document",
            "vendor_document_extraction_source",
        }
        assert record.mandatory_use_allowed is False
        assert record.audit_ready_claimed is False


def test_wave6_sources_do_not_claim_release_uat_or_productization():
    matrix = load_default_document_standards_applicability_matrix()
    policy_library = load_default_document_citation_policy_library()

    searchable_text = " ".join(
        [
            *matrix.matrix_controls,
            *matrix.explicit_non_implementation_claims,
            *[
                value
                for record in matrix.document_records
                for value in [
                    *record.visible_limitation_statements,
                    *record.downstream_use_limits,
                    *record.explicit_non_implementation_claims,
                ]
            ],
            *policy_library.policy_library_controls,
            *policy_library.explicit_non_implementation_claims,
            *[
                value
                for policy in policy_library.policies
                for value in [
                    *policy.policy_controls,
                    *policy.explicit_non_implementation_claims,
                ]
            ],
        ]
    ).casefold()

    assert "does_not_accept_uat" in searchable_text
    assert "does_not_claim_product_release" in searchable_text
    assert "does_not_implement_standards_retrieval_or_embedding" in searchable_text
    assert "does_not_claim_audit_ready_output" in searchable_text
    assert "does_not_generate_product_ready_standards_output" in searchable_text


def test_unverified_section_or_clause_depth_is_rejected():
    record = {
        "document_ref": "URS",
        "version": "v1",
        "status": "runtime_facing_document_standards_applicability_record",
        "document_type": "User Requirements Specification",
        "source_mode": "asbp_owned_template_body",
        "applicability_status": "limited_support_with_visible_limitations",
        "standards_bundle_refs": ["SB-CQV-GMP@v1"],
        "std_ids": ["STD-EU-GMP-ANNEX-15"],
        "allowed_citation_depths": ["document", "clause"],
        "visible_limitation_statements": ["Limited source support."],
        "applicability_rationale": "Test invalid deep citation depth.",
        "downstream_use_limits": ["No product release."],
        "mandatory_use_allowed": False,
        "audit_ready_claimed": False,
        "explicit_non_implementation_claims": [
            "does_not_embed_controlled_standards_text",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_generate_product_ready_standards_output",
            "does_not_claim_audit_ready_output",
            "does_not_accept_uat",
            "does_not_claim_product_release",
        ],
    }

    with pytest.raises(ValidationError) as exc_info:
        DocumentStandardsApplicabilityRecordModel(**record)

    assert "version/section/clause citation depth" in str(exc_info.value)


def test_policy_rejects_retrieval_or_embedding():
    payload = {
        "policy_id": "CITPOL-TEST@v1",
        "version": "v1",
        "status": "runtime_facing_document_citation_policy_record",
        "document_ref": "TEST",
        "citation_mode": "visible_limitation_required",
        "default_citation_depth": "document",
        "permitted_citation_depths": ["document"],
        "blocked_citation_depths": ["version", "section", "clause"],
        "limitation_statement_required": True,
        "source_text_storage_allowed": False,
        "retrieval_or_embedding_allowed": True,
        "mandatory_use_allowed": False,
        "audit_ready_claimed": False,
        "policy_controls": ["Document-level only."],
        "explicit_non_implementation_claims": [
            "does_not_embed_controlled_standards_text",
            "does_not_implement_standards_retrieval_or_embedding",
            "does_not_generate_product_ready_standards_output",
            "does_not_claim_audit_ready_output",
            "does_not_accept_uat",
            "does_not_claim_product_release",
        ],
    }

    with pytest.raises(ValidationError) as exc_info:
        DocumentCitationPolicyRecordModel(**payload)

    assert "retrieval or embedding" in str(exc_info.value)


def test_persisted_state_payload_is_not_standards_wave6_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as matrix_exc:
        load_document_standards_applicability_matrix_from_payload(persisted_state_payload)
    assert "document_records" in str(matrix_exc.value)

    with pytest.raises(ValueError) as policy_exc:
        load_document_citation_policy_library_from_payload(persisted_state_payload)
    assert "policies" in str(policy_exc.value)


def test_assert_helpers_report_missing_document_refs():
    matrix = load_default_document_standards_applicability_matrix()
    policy_library = load_default_document_citation_policy_library()

    assert_document_standards_applicability_refs_exist(matrix, {"URS"})
    assert_document_citation_policy_refs_exist(policy_library, {"URS"})

    with pytest.raises(ValueError) as matrix_exc:
        assert_document_standards_applicability_refs_exist(matrix, {"MISSING_DOC"})
    assert "MISSING_DOC" in str(matrix_exc.value)

    with pytest.raises(ValueError) as policy_exc:
        assert_document_citation_policy_refs_exist(policy_library, {"MISSING_DOC"})
    assert "MISSING_DOC" in str(policy_exc.value)
