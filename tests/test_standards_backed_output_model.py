from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.standards_backed_output_model import (
    StandardsBackedOutputControlLibraryModel,
    StandardsBackedOutputControlPacketModel,
    StandardsBackedOutputSourceControlModel,
)


def _required_claims() -> list[str]:
    return [
        "does_not_generate_product_ready_documents",
        "does_not_render_or_export_documents",
        "does_not_implement_standards_retrieval_or_embedding",
        "does_not_hide_source_or_citation_limitations",
    ]


def _minimal_source_control() -> dict:
    return {
        "std_id": "STD-EU-GMP-ANNEX-15",
        "registry_version": "v0.1",
        "authority_status": "authoritative",
        "verification_status": "pending_verification",
        "mandatory_flag": "mandatory_when_applicable",
        "version_or_effective_date": "TBD",
        "requested_citation_depth": "document",
        "rendered_citation_depth": "document",
        "available_citation_depths": ["document"],
        "source_limitations": ["Version/effective date remains TBD."],
        "limitation_statements": ["Version/effective date remains TBD."],
        "assumption_records": ["Registry metadata only."],
        "warning_text": "Visible standards source/citation limitation applies.",
        "warning_visibility": "visible",
        "source_record_ref": "SB-CQV-GMP@v1::STD-EU-GMP-ANNEX-15",
    }


def _minimal_packet() -> dict:
    return {
        "control_packet_id": "STDOUT-TEST-CONTROLS@v1",
        "version": "v1",
        "status": "standards_backed_output_control_packet",
        "draft_id": "DRAFT-TEST@v1",
        "template_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "schema_id": "SCHEMA-QUALIFICATION-PLAN@v1",
        "standards_bundle_refs": ["SB-CQV-GMP@v1"],
        "source_controls": [_minimal_source_control()],
        "section_controls": [
            {
                "section_id": "section.strategy",
                "standards_relevance": "standards_relevant",
                "standards_source_refs": ["STD-EU-GMP-ANNEX-15"],
                "citation_limitation_statements": [
                    "Version/effective date remains TBD."
                ],
                "assumption_records": ["Section control only."],
                "reviewer_attention_points": ["Review source status."],
            }
        ],
        "output_warning_text": "Standards-backed output controls include visible limitations.",
        "output_warning_visibility": "visible",
        "output_limitation_summary": ["Version/effective date remains TBD."],
        "assumption_records": ["M29.6 output controls only."],
        "reviewer_attention_points": ["Review visible limitations."],
        "explicit_non_implementation_claims": _required_claims(),
    }


def _minimal_library(packet: dict | None = None) -> dict:
    return {
        "library_id": "M29_STANDARDS_BACKED_OUTPUT_LIBRARY@v1",
        "version": "v1",
        "status": "standards_backed_output_control_packet",
        "control_packets": [packet or _minimal_packet()],
        "library_controls": ["Standards-backed output controls only."],
        "explicit_non_implementation_claims": _required_claims(),
    }


def test_standards_backed_output_packet_accepts_controlled_minimum():
    packet = StandardsBackedOutputControlPacketModel(**_minimal_packet())

    assert packet.control_packet_id == "STDOUT-TEST-CONTROLS@v1"
    assert packet.has_limited_sources()
    assert packet.output_warning_visibility == "visible"


def test_limited_source_requires_visible_warning():
    source = _minimal_source_control()
    source["warning_text"] = None
    source["warning_visibility"] = "not_required"

    with pytest.raises(ValidationError) as exc_info:
        StandardsBackedOutputSourceControlModel(**source)

    assert "visible warning text" in str(exc_info.value)


def test_rendered_depth_cannot_exceed_requested_depth():
    source = _minimal_source_control()
    source["version_or_effective_date"] = "2024"
    source["verification_status"] = "verified"
    source["requested_citation_depth"] = "document"
    source["rendered_citation_depth"] = "clause"
    source["available_citation_depths"] = ["document", "clause"]

    with pytest.raises(ValidationError) as exc_info:
        StandardsBackedOutputSourceControlModel(**source)

    assert "cannot be more specific" in str(exc_info.value)


def test_section_marked_relevant_requires_source_refs():
    packet = _minimal_packet()
    packet["section_controls"][0]["standards_source_refs"] = []

    with pytest.raises(ValidationError) as exc_info:
        StandardsBackedOutputControlPacketModel(**packet)

    assert "requires standards_source_refs" in str(exc_info.value)


def test_packet_requires_non_implementation_claims():
    packet = _minimal_packet()
    packet["explicit_non_implementation_claims"] = [
        "does_not_generate_product_ready_documents"
    ]

    with pytest.raises(ValidationError) as exc_info:
        StandardsBackedOutputControlPacketModel(**packet)

    assert "M29.6 standards-backed output control packet is missing explicit" in str(
        exc_info.value
    )


def test_library_rejects_duplicate_packet_ids():
    packet = _minimal_packet()
    library = _minimal_library(packet)
    library["control_packets"].append(deepcopy(packet))

    with pytest.raises(ValidationError) as exc_info:
        StandardsBackedOutputControlLibraryModel(**library)

    assert "Duplicate standards-backed output control packet id" in str(exc_info.value)
