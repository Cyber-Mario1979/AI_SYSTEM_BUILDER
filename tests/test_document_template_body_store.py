import pytest

from asbp.document_template_body_store import (
    MVP_MUST_HAVE_DOCUMENT_REFS,
    assert_document_template_body_refs_exist,
    assert_mvp_document_template_body_coverage,
    find_missing_document_template_body_refs,
    get_document_template_body_by_ref,
    list_document_template_bodies_by_output_role,
    list_document_template_body_document_refs,
    list_document_template_body_ids,
    load_default_document_template_body_library,
    load_document_template_body_library_from_payload,
)


def test_default_mvp_document_template_body_library_loads():
    library = load_default_document_template_body_library()

    assert library.library_id == "M29_DOCUMENT_TEMPLATE_BODY_LIBRARY@v1"
    assert set(list_document_template_body_document_refs(library)) == (
        MVP_MUST_HAVE_DOCUMENT_REFS
    )
    assert len(list_document_template_body_ids(library)) == len(
        MVP_MUST_HAVE_DOCUMENT_REFS
    )
    assert_mvp_document_template_body_coverage(library)


def test_mvp_document_template_body_core_records_have_sections_and_controls():
    library = load_default_document_template_body_library()

    for document_ref in MVP_MUST_HAVE_DOCUMENT_REFS:
        body_record = get_document_template_body_by_ref(library, document_ref)

        assert body_record.priority == "P0"
        assert body_record.owner_review_required is True
        assert body_record.sections
        assert body_record.template_controls
        assert "does_not_generate_documents" in (
            body_record.explicit_non_implementation_claims
        )


def test_template_examples_are_structure_references_only():
    library = load_default_document_template_body_library()

    source_refs = {
        source_ref
        for body_record in library.body_records
        for source_ref in body_record.source_structure_references
    }

    assert any(
        source_ref.startswith("ARCH_BUNDLE_DocumentTemplates_v1.md::")
        for source_ref in source_refs
    )
    assert any(source_ref == "owner_must_have_document_list" for source_ref in source_refs)


def test_key_document_body_records_preserve_expected_structures():
    library = load_default_document_template_body_library()

    urs = get_document_template_body_by_ref(library, "URS")
    assert _section_titles(urs) >= {
        "Purpose and scope",
        "Functional requirements",
        "Design and materials requirements",
        "Utilities, computerized systems, safety, health and environment requirements",
    }

    rtm = get_document_template_body_by_ref(library, "RTM")
    assert any(table.table_id == "TBL-RTM" for table in rtm.tables)

    dq = get_document_template_body_by_ref(library, "DQ")
    assert any(table.table_id == "TBL-DQ-COMPLIANCE" for table in dq.tables)

    vsr = get_document_template_body_by_ref(library, "VSR")
    assert "Conclusion and recommendation" in _section_titles(vsr)


def test_vendor_and_certificate_records_do_not_claim_authored_templates():
    library = load_default_document_template_body_library()

    vendor_doc = get_document_template_body_by_ref(
        library,
        "VENDOR_DOC_EXTRACTION_SOURCE",
    )
    assert vendor_doc.template_body_kind == "data_extraction_plan"
    assert vendor_doc.linked_template_id is None

    a0_certificate = get_document_template_body_by_ref(library, "A0_CERTIFICATE")
    assert a0_certificate.template_body_kind == "certificate_record_plan"


def test_body_records_by_output_role_are_listable():
    library = load_default_document_template_body_library()

    qualification_records = list_document_template_bodies_by_output_role(
        library,
        "qualification",
    )
    qualification_refs = {
        record.document_ref
        for record in qualification_records
    }

    assert {"IQ_PROTOCOL_REPORT", "OQ_PROTOCOL_REPORT", "PQ_PROTOCOL_REPORT"} <= (
        qualification_refs
    )


def test_missing_template_body_refs_are_reported():
    library = load_default_document_template_body_library()

    assert find_missing_document_template_body_refs(
        library,
        {"URS", "DQ"},
    ) == []

    assert find_missing_document_template_body_refs(
        library,
        {"MISSING_DOCUMENT"},
    ) == ["MISSING_DOCUMENT"]

    with pytest.raises(ValueError) as exc_info:
        assert_document_template_body_refs_exist(library, {"MISSING_DOCUMENT"})

    assert "MISSING_DOCUMENT" in str(exc_info.value)


def test_persisted_state_payload_is_not_template_body_truth():
    persisted_state_payload = {
        "project": "AI_SYSTEM_BUILDER",
        "version": "0.8.0",
        "status": "in_flight",
        "tasks": [],
    }

    with pytest.raises(ValueError) as exc_info:
        load_document_template_body_library_from_payload(persisted_state_payload)

    assert "document template body library payload must include body_records" in str(
        exc_info.value
    )


def test_template_body_library_does_not_create_uat_or_release_claims():
    library = load_default_document_template_body_library()
    searchable_text = " ".join(
        [
            *library.library_controls,
            *library.explicit_non_implementation_claims,
            *[
                value
                for body_record in library.body_records
                for value in [
                    *body_record.template_controls,
                    *body_record.explicit_non_implementation_claims,
                ]
            ],
        ]
    ).casefold()

    assert "does_not_generate_documents" in searchable_text
    assert "does_not_create_signed_or_approved_records" in searchable_text
    assert "does_not_claim_product_release" in searchable_text
    assert "m29.12" not in searchable_text or "does not" in searchable_text


def _section_titles(body_record) -> set[str]:
    return {
        section.title
        for section in body_record.sections
    }
