import pytest
from pydantic import ValidationError

from asbp.document_input_dependency_model import (
    DocumentDependencyContractLibraryModel,
    DocumentDependencyContractModel,
    UrsDcfIntakeCatalogModel,
)


def _claims():
    return [
        "does_not_generate_documents",
        "does_not_create_uat_acceptance",
        "does_not_approve_release_or_productize",
        "does_not_replace_human_review",
    ]


def _minimal_dcf_record():
    return {
        "dcf_id": "DCF-URS-TEST@v1",
        "version": "v1",
        "status": "mvp_runtime_source",
        "domain": "process_equipment",
        "display_name": "URS DCF test",
        "source_file_name": "test.docx",
        "target_document_ref": "URS",
        "target_template_body_ref": "TPLBODY-URS@v1",
        "supported_asset_scope": ["Tablet Compression Machine"],
        "field_groups": [
            {
                "group_id": "system_profile",
                "display_name": "System profile",
                "source_section_label": "1. System profile",
                "group_controls": ["Group is controlled."],
            }
        ],
        "fields": [
            {
                "field_id": "system_name",
                "display_name": "System name",
                "group_id": "system_profile",
                "requirement_status": "required",
                "value_type": "string",
                "source_table_label": "DCF table",
                "target_urs_section_refs": ["section.urs_scope"],
                "extraction_notes": [],
            }
        ],
        "dcf_controls": ["DCF feeds URS only."],
        "explicit_non_implementation_claims": _claims(),
    }


def _minimal_contract(document_ref="URS", uses_dcf=True, input_mode="urs_dcf_intake"):
    return {
        "contract_id": f"DOCCONTRACT-{document_ref}@v1",
        "version": "v1",
        "status": "mvp_runtime_source",
        "document_ref": document_ref,
        "display_name": document_ref,
        "input_mode": input_mode,
        "uses_dcf": uses_dcf,
        "upstream_input_sources": ["DCF_URS_INTAKE"] if uses_dcf else ["URS"],
        "target_template_body_ref": f"TPLBODY-{document_ref}@v1" if input_mode != "external_adopted_source" else None,
        "derivation_controls": ["Controlled dependency only."],
        "blocking_conditions": ["Missing URS blocks downstream flow."],
        "explicit_non_implementation_claims": _claims(),
    }


def test_urs_dcf_intake_catalog_accepts_urs_only_catalog():
    catalog = UrsDcfIntakeCatalogModel(
        catalog_id="M29_URS_DCF_INTAKE_CATALOG@v1",
        version="v1",
        dcf_records=[_minimal_dcf_record()],
        catalog_controls=["Only URS uses DCF."],
        explicit_non_implementation_claims=_claims(),
    )

    assert catalog.dcf_records[0].target_document_ref == "URS"


def test_urs_dcf_rejects_unknown_field_group_reference():
    record = _minimal_dcf_record()
    record["fields"][0]["group_id"] = "missing_group"

    with pytest.raises(ValidationError) as exc_info:
        UrsDcfIntakeCatalogModel(
            catalog_id="M29_URS_DCF_INTAKE_CATALOG@v1",
            version="v1",
            dcf_records=[record],
            catalog_controls=["Only URS uses DCF."],
            explicit_non_implementation_claims=_claims(),
        )

    assert "unknown group_id" in str(exc_info.value)


def test_downstream_document_cannot_use_dcf():
    contract = _minimal_contract(
        document_ref="DQ",
        uses_dcf=True,
        input_mode="derived_from_upstream_documents",
    )

    with pytest.raises(ValidationError) as exc_info:
        DocumentDependencyContractModel(**contract)

    assert "Only URS may use DCF intake" in str(exc_info.value)


def test_downstream_document_cannot_reference_raw_dcf_source():
    contract = _minimal_contract(
        document_ref="DQ",
        uses_dcf=False,
        input_mode="derived_from_upstream_documents",
    )
    contract["upstream_input_sources"] = ["DCF_URS_INTAKE"]

    with pytest.raises(ValidationError) as exc_info:
        DocumentDependencyContractModel(**contract)

    assert "depend on URS" in str(exc_info.value)


def test_external_adopted_source_cannot_require_template_body():
    contract = _minimal_contract(
        document_ref="CCF",
        uses_dcf=False,
        input_mode="external_adopted_source",
    )
    contract["upstream_input_sources"] = ["HUMAN_REVIEW"]
    contract["target_template_body_ref"] = "TPLBODY-CCF@v1"

    with pytest.raises(ValidationError) as exc_info:
        DocumentDependencyContractModel(**contract)

    assert "External/adopted documents" in str(exc_info.value)


def test_dependency_library_rejects_duplicate_document_refs():
    first = _minimal_contract()
    second = dict(first)
    second["contract_id"] = "DOCCONTRACT-URS-COPY@v1"

    with pytest.raises(ValidationError) as exc_info:
        DocumentDependencyContractLibraryModel(
            library_id="M29_DOCUMENT_DEPENDENCY_CONTRACT_LIBRARY@v1",
            version="v1",
            dependency_contracts=[first, second],
            library_controls=["Contracts are controlled."],
            explicit_non_implementation_claims=_claims(),
        )

    assert "Duplicate document dependency document_ref" in str(exc_info.value)
