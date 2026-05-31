from asbp.document_input_dependency_store import (
    get_document_dependency_contract_by_ref,
    get_urs_dcf_by_domain,
    list_document_dependency_refs,
    list_urs_dcf_ids,
    list_vendor_document_source_ids,
    load_default_document_dependency_contract_library,
    load_default_urs_dcf_intake_catalog,
    load_default_vendor_document_extraction_library,
)

EXPECTED_DCF_DOMAINS = {
    "cleanroom_hvac",
    "process_equipment",
    "utilities",
    "computerized_systems",
}

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


def test_default_urs_dcf_catalog_loads_four_domain_forms_only():
    catalog = load_default_urs_dcf_intake_catalog()

    assert catalog.catalog_id == "M29_URS_DCF_INTAKE_CATALOG@v1"
    assert len(list_urs_dcf_ids(catalog)) == 4
    assert {record.domain for record in catalog.dcf_records} == EXPECTED_DCF_DOMAINS
    assert {record.target_document_ref for record in catalog.dcf_records} == {"URS"}


def test_process_equipment_dcf_uses_vertical_granulator_not_vacuum():
    catalog = load_default_urs_dcf_intake_catalog()
    record = get_urs_dcf_by_domain(catalog, "process_equipment")
    scope_text = " ".join(record.supported_asset_scope).casefold()

    assert "vertical granulator" in scope_text
    assert "vacuum granulator" not in scope_text


def test_document_dependency_contracts_cover_must_have_documents():
    library = load_default_document_dependency_contract_library()

    assert set(list_document_dependency_refs(library)) >= MUST_HAVE_DOCUMENT_REFS


def test_urs_is_only_dcf_driven_document():
    library = load_default_document_dependency_contract_library()

    for contract in library.dependency_contracts:
        if contract.document_ref == "URS":
            assert contract.uses_dcf is True
            assert contract.input_mode == "urs_dcf_intake"
            assert "DCF_URS_INTAKE" in contract.upstream_input_sources
        else:
            assert contract.uses_dcf is False
            assert "DCF_URS_INTAKE" not in contract.upstream_input_sources


def test_downstream_documents_rely_on_urs_not_raw_dcf():
    library = load_default_document_dependency_contract_library()

    for document_ref in ["DQ", "RTM", "IQ_PROTOCOL_REPORT", "OQ_PROTOCOL_REPORT", "PQ_PROTOCOL_REPORT", "VSR"]:
        contract = get_document_dependency_contract_by_ref(library, document_ref)
        assert "URS" in contract.upstream_input_sources
        assert "DCF_URS_INTAKE" not in contract.upstream_input_sources


def test_ccf_and_vendor_docs_are_not_dcf_generated():
    library = load_default_document_dependency_contract_library()

    ccf = get_document_dependency_contract_by_ref(library, "CCF")
    assert ccf.input_mode == "external_adopted_source"
    assert ccf.uses_dcf is False
    assert ccf.target_template_body_ref is None

    vendor_docs = get_document_dependency_contract_by_ref(library, "VENDOR_DOCS")
    assert vendor_docs.input_mode == "vendor_document_extraction_source"
    assert vendor_docs.uses_dcf is False


def test_vendor_extraction_sources_support_traceability_and_qualification_outputs():
    library = load_default_vendor_document_extraction_library()

    assert set(list_vendor_document_source_ids(library)) >= {
        "VENDOR-SOURCE-FDS@v1",
        "VENDOR-SOURCE-SDS@v1",
        "VENDOR-SOURCE-PID@v1",
        "VENDOR-SOURCE-MANUAL@v1",
        "VENDOR-SOURCE-CERTIFICATE@v1",
    }
    all_targets = {
        target
        for source in library.vendor_sources
        for target in source.extraction_targets
    }
    assert {"RTM", "DQ", "IQ_PROTOCOL_REPORT", "OQ_PROTOCOL_REPORT"} <= all_targets


def test_wave5_sources_do_not_claim_release_or_uat_acceptance():
    catalog = load_default_urs_dcf_intake_catalog()
    dependency_library = load_default_document_dependency_contract_library()
    vendor_library = load_default_vendor_document_extraction_library()
    searchable_text = " ".join(
        [
            *catalog.catalog_controls,
            *catalog.explicit_non_implementation_claims,
            *dependency_library.library_controls,
            *dependency_library.explicit_non_implementation_claims,
            *vendor_library.library_controls,
            *vendor_library.explicit_non_implementation_claims,
            *[
                value
                for record in catalog.dcf_records
                for value in [
                    *record.dcf_controls,
                    *record.explicit_non_implementation_claims,
                ]
            ],
            *[
                value
                for contract in dependency_library.dependency_contracts
                for value in [
                    *contract.derivation_controls,
                    *contract.blocking_conditions,
                    *contract.explicit_non_implementation_claims,
                ]
            ],
        ]
    ).casefold()

    assert "does_not_generate_documents" in searchable_text
    assert "does_not_create_uat_acceptance" in searchable_text
    assert "does_not_approve_release_or_productize" in searchable_text
