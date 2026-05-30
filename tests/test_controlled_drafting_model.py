from copy import deepcopy

import pytest
from pydantic import ValidationError

from asbp.controlled_drafting_model import (
    ControlledDraftPacketModel,
    ControlledDraftSectionModel,
    ControlledDraftingLibraryModel,
    ControlledDraftingModeDefinitionModel,
)


def _required_claims() -> list[str]:
    return [
        "does_not_create_product_ready_documents",
        "does_not_render_or_export_documents",
        "does_not_apply_standards_backed_output_controls",
        "does_not_mutate_lifecycle_or_review_state",
    ]


def _minimal_mode_payload() -> dict:
    return {
        "drafting_mode_id": "DRAFTMODE-TEST-STRONG@v1",
        "version": "v1",
        "status": "runtime_facing_controlled_drafting_mode",
        "drafting_mode": "strong_input_fill",
        "display_name": "Test strong input fill",
        "supported_template_ids": ["TPL-FUTURE-QUALIFICATION-PLAN@v1"],
        "supported_schema_ids": ["SCHEMA-QUALIFICATION-PLAN@v1"],
        "mode_controls": ["Controlled drafting mode source record only."],
        "explicit_non_implementation_claims": _required_claims(),
    }


def _minimal_library_payload(mode: dict | None = None) -> dict:
    return {
        "library_id": "M29_CONTROLLED_DRAFTING_LIBRARY@v1",
        "version": "v1",
        "status": "runtime_facing_controlled_drafting_source",
        "drafting_modes": [mode or _minimal_mode_payload()],
        "library_controls": ["Controlled drafting library source only."],
        "explicit_non_implementation_claims": _required_claims(),
    }


def _minimal_packet_payload() -> dict:
    return {
        "draft_id": "DRAFT-TEST-QUALIFICATION-PLAN@v1",
        "status": "controlled_draft_packet",
        "drafting_mode_id": "DRAFTMODE-TEST-STRONG@v1",
        "drafting_mode": "strong_input_fill",
        "template_id": "TPL-FUTURE-QUALIFICATION-PLAN@v1",
        "schema_id": "SCHEMA-QUALIFICATION-PLAN@v1",
        "supplied_field_values": [
            {"field_id": "project_title", "value": "Project A"},
        ],
        "missing_required_field_ids": [],
        "placeholders": [],
        "section_drafts": [
            {
                "section_id": "draft_section.project_title",
                "section_title": "Project title",
                "draft_text": "Controlled draft field packet for Project title: Project A",
                "field_ids": ["project_title"],
                "limitation_statements": [
                    "Draft text is bounded to supplied input and is not product-ready output."
                ],
            }
        ],
        "limitation_statements": [
            "M29.5 controlled drafting creates bounded draft packets only.",
        ],
        "reviewer_attention_points": ["Review controlled input for field: project_title"],
        "explicit_non_implementation_claims": _required_claims(),
    }


def test_controlled_drafting_mode_accepts_controlled_minimum():
    mode = ControlledDraftingModeDefinitionModel(**_minimal_mode_payload())

    assert mode.drafting_mode_id == "DRAFTMODE-TEST-STRONG@v1"
    assert mode.drafting_mode == "strong_input_fill"


def test_controlled_drafting_mode_rejects_version_mismatch():
    mode = _minimal_mode_payload()
    mode["version"] = "v2"

    with pytest.raises(ValidationError) as exc_info:
        ControlledDraftingModeDefinitionModel(**mode)

    assert "version must match drafting_mode_id suffix" in str(exc_info.value)


def test_controlled_drafting_mode_requires_explicit_non_implementation_claims():
    mode = _minimal_mode_payload()
    mode["explicit_non_implementation_claims"] = [
        "does_not_create_product_ready_documents"
    ]

    with pytest.raises(ValidationError) as exc_info:
        ControlledDraftingModeDefinitionModel(**mode)

    assert "M29.5 controlled drafting mode is missing explicit" in str(exc_info.value)


def test_controlled_drafting_library_rejects_duplicate_mode_ids():
    mode = _minimal_mode_payload()
    payload = _minimal_library_payload(mode)
    payload["drafting_modes"].append(deepcopy(mode))

    with pytest.raises(ValidationError) as exc_info:
        ControlledDraftingLibraryModel(**payload)

    assert "Duplicate controlled drafting mode id is not allowed" in str(exc_info.value)


def test_controlled_draft_packet_rejects_duplicate_section_ids():
    packet = _minimal_packet_payload()
    packet["section_drafts"].append(deepcopy(packet["section_drafts"][0]))

    with pytest.raises(ValidationError) as exc_info:
        ControlledDraftPacketModel(**packet)

    assert "Duplicate controlled draft section_id is not allowed" in str(exc_info.value)


def test_controlled_draft_packet_rejects_duplicate_section_field_ids():
    with pytest.raises(ValidationError) as exc_info:
        ControlledDraftSectionModel(
            section_id="draft_section.duplicate",
            section_title="Duplicate",
            draft_text="Duplicate field draft",
            field_ids=["project_title", "project_title"],
        )

    assert "Duplicate controlled draft section field_ids" in str(exc_info.value)


def test_strong_input_fill_packet_cannot_include_placeholders():
    packet = _minimal_packet_payload()
    packet["placeholders"] = [
        {
            "field_id": "cqv_scope",
            "placeholder_text": "{{ cqv_scope }}",
            "reason": "Missing input.",
        }
    ]

    with pytest.raises(ValidationError) as exc_info:
        ControlledDraftPacketModel(**packet)

    assert "Strong input fill controlled draft cannot include placeholders" in str(
        exc_info.value
    )


def test_controlled_draft_packet_requires_explicit_non_implementation_claims():
    packet = _minimal_packet_payload()
    packet["explicit_non_implementation_claims"] = [
        "does_not_create_product_ready_documents"
    ]

    with pytest.raises(ValidationError) as exc_info:
        ControlledDraftPacketModel(**packet)

    assert "M29.5 controlled draft packet is missing explicit" in str(exc_info.value)
