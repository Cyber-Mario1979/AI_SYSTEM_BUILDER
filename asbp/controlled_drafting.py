from __future__ import annotations

from typing import Any

from asbp.controlled_drafting_model import (
    REQUIRED_CONTROLLED_DRAFTING_NON_IMPLEMENTATION_CLAIMS,
    ControlledDraftInputFieldValueModel,
    ControlledDraftPacketModel,
    ControlledDraftPlaceholderModel,
    ControlledDraftSectionModel,
)
from asbp.controlled_drafting_store import (
    assert_drafting_mode_supports_template_and_schema,
    get_controlled_drafting_mode_by_id,
    load_default_controlled_drafting_library,
)
from asbp.document_input_schema_binding import (
    load_document_input_schema_for_selection_result,
    load_document_input_schema_for_template_id,
)
from asbp.document_input_schema_model import (
    DocumentInputSchemaFieldModel,
    DocumentInputSchemaRecordModel,
    DocumentInputRouteRef,
)
from asbp.document_input_schema_store import load_default_document_input_schema_library
from asbp.document_template_store import load_default_document_template_library
from asbp.template_selection_model import TemplateSelectionResultModel


def build_controlled_draft_packet_for_template(
    *,
    draft_id: str,
    drafting_mode_id: str,
    template_id: str,
    input_values: dict[str, Any],
    intake_route_ref: DocumentInputRouteRef = "ROUTE-DCF",
) -> ControlledDraftPacketModel:
    template_library = load_default_document_template_library()
    schema_library = load_default_document_input_schema_library()
    schema = load_document_input_schema_for_template_id(
        template_id,
        template_library=template_library,
        schema_library=schema_library,
    )
    return _build_controlled_draft_packet(
        draft_id=draft_id,
        drafting_mode_id=drafting_mode_id,
        schema=schema,
        input_values=input_values,
        intake_route_ref=intake_route_ref,
    )


def build_controlled_draft_packet_for_selection(
    *,
    draft_id: str,
    drafting_mode_id: str,
    selection_result: TemplateSelectionResultModel,
    input_values: dict[str, Any],
    intake_route_ref: DocumentInputRouteRef = "ROUTE-DCF",
) -> ControlledDraftPacketModel:
    template_library = load_default_document_template_library()
    schema_library = load_default_document_input_schema_library()
    schema = load_document_input_schema_for_selection_result(
        selection_result,
        template_library=template_library,
        schema_library=schema_library,
    )
    return _build_controlled_draft_packet(
        draft_id=draft_id,
        drafting_mode_id=drafting_mode_id,
        schema=schema,
        input_values=input_values,
        intake_route_ref=intake_route_ref,
    )


def _build_controlled_draft_packet(
    *,
    draft_id: str,
    drafting_mode_id: str,
    schema: DocumentInputSchemaRecordModel,
    input_values: dict[str, Any],
    intake_route_ref: DocumentInputRouteRef,
) -> ControlledDraftPacketModel:
    drafting_library = load_default_controlled_drafting_library()
    mode_definition = get_controlled_drafting_mode_by_id(
        drafting_library,
        drafting_mode_id,
    )
    assert_drafting_mode_supports_template_and_schema(
        mode_definition,
        schema.template_id,
        schema.schema_id,
    )

    route_field_ids = _field_ids_for_route(schema, intake_route_ref)
    schema_fields = [
        field for field in _all_schema_fields(schema) if field.field_id in route_field_ids
    ]
    required_fields = [
        field for field in schema.required_fields if field.field_id in route_field_ids
    ]

    supplied_values = _collect_supplied_field_values(schema_fields, input_values)
    supplied_ids = {field_value.field_id for field_value in supplied_values}
    missing_required_fields = [
        field for field in required_fields if field.field_id not in supplied_ids
    ]

    if mode_definition.drafting_mode == "strong_input_fill" and missing_required_fields:
        missing_ids = ", ".join(field.field_id for field in missing_required_fields)
        raise ValueError(f"Strong input fill requires all required fields: {missing_ids}")

    placeholders = _build_placeholders(
        mode_definition.drafting_mode,
        schema_fields,
        supplied_ids,
        missing_required_fields,
    )
    section_drafts = _build_section_drafts(
        mode_definition.drafting_mode,
        schema_fields,
        supplied_values,
        placeholders,
    )
    limitation_statements = _build_limitation_statements(
        mode_definition.drafting_mode,
        missing_required_fields,
        placeholders,
    )
    reviewer_attention_points = _build_reviewer_attention_points(
        mode_definition.drafting_mode,
        missing_required_fields,
        schema,
    )

    return ControlledDraftPacketModel(
        draft_id=draft_id,
        drafting_mode_id=mode_definition.drafting_mode_id,
        drafting_mode=mode_definition.drafting_mode,
        template_id=schema.template_id,
        schema_id=schema.schema_id,
        supplied_field_values=supplied_values,
        missing_required_field_ids=[field.field_id for field in missing_required_fields],
        placeholders=placeholders,
        section_drafts=section_drafts,
        limitation_statements=limitation_statements,
        reviewer_attention_points=reviewer_attention_points,
        explicit_non_implementation_claims=sorted(
            REQUIRED_CONTROLLED_DRAFTING_NON_IMPLEMENTATION_CLAIMS
        ),
    )


def _all_schema_fields(schema: DocumentInputSchemaRecordModel) -> list[DocumentInputSchemaFieldModel]:
    return [*schema.required_fields, *schema.optional_fields, *schema.conditional_fields]


def _field_ids_for_route(
    schema: DocumentInputSchemaRecordModel,
    intake_route_ref: DocumentInputRouteRef,
) -> set[str]:
    if intake_route_ref == "ROUTE-DCF":
        return set(schema.dcf_intake_mapping.field_ids)
    return set(schema.skip_dcf_minimum_input_mapping.field_ids)


def _collect_supplied_field_values(
    schema_fields: list[DocumentInputSchemaFieldModel],
    input_values: dict[str, Any],
) -> list[ControlledDraftInputFieldValueModel]:
    known_fields = {field.field_id: field for field in schema_fields}
    supplied_values: list[ControlledDraftInputFieldValueModel] = []

    for field_id, raw_value in input_values.items():
        if field_id not in known_fields:
            continue

        value = _stringify_value(raw_value)
        if value is None:
            continue

        field = known_fields[field_id]
        supplied_values.append(
            ControlledDraftInputFieldValueModel(
                field_id=field_id,
                value=value,
                source_ref=field.source_input_refs[0] if field.source_input_refs else None,
            )
        )

    return supplied_values


def _build_placeholders(
    drafting_mode,
    schema_fields: list[DocumentInputSchemaFieldModel],
    supplied_ids: set[str],
    missing_required_fields: list[DocumentInputSchemaFieldModel],
) -> list[ControlledDraftPlaceholderModel]:
    if drafting_mode == "strong_input_fill":
        return []

    if drafting_mode == "minimal_scaffold_with_placeholders":
        placeholder_fields = schema_fields
    else:
        placeholder_fields = missing_required_fields

    placeholders: list[ControlledDraftPlaceholderModel] = []
    for field in placeholder_fields:
        if field.field_id in supplied_ids and drafting_mode != "minimal_scaffold_with_placeholders":
            continue
        placeholders.append(
            ControlledDraftPlaceholderModel(
                field_id=field.field_id,
                placeholder_text=f"{{{{ {field.field_id} }}}}",
                reason=(
                    "Visible placeholder retained because controlled drafting must not "
                    "invent missing source data."
                ),
            )
        )
    return placeholders


def _build_section_drafts(
    drafting_mode,
    schema_fields: list[DocumentInputSchemaFieldModel],
    supplied_values: list[ControlledDraftInputFieldValueModel],
    placeholders: list[ControlledDraftPlaceholderModel],
) -> list[ControlledDraftSectionModel]:
    supplied_by_id = {field_value.field_id: field_value for field_value in supplied_values}
    placeholder_by_id = {placeholder.field_id: placeholder for placeholder in placeholders}

    if drafting_mode == "minimal_scaffold_with_placeholders":
        selected_fields = schema_fields
    else:
        selected_fields = [
            field
            for field in schema_fields
            if field.field_id in supplied_by_id or field.field_id in placeholder_by_id
        ]

    if not selected_fields:
        selected_fields = schema_fields[:1]

    section_drafts: list[ControlledDraftSectionModel] = []
    for field in selected_fields:
        if field.field_id in supplied_by_id and drafting_mode != "minimal_scaffold_with_placeholders":
            draft_text = (
                f"Controlled draft field packet for {field.display_name}: "
                f"{supplied_by_id[field.field_id].value}"
            )
            limitations = [
                "Draft text is bounded to supplied input and is not product-ready output."
            ]
        else:
            placeholder_text = placeholder_by_id.get(field.field_id)
            visible_placeholder = (
                placeholder_text.placeholder_text
                if placeholder_text is not None
                else f"{{{{ {field.field_id} }}}}"
            )
            draft_text = (
                f"Controlled placeholder scaffold for {field.display_name}: "
                f"{visible_placeholder}"
            )
            limitations = [
                "Placeholder scaffold preserves missing data visibility.",
                "No technical, regulatory, site, test, or acceptance content is invented.",
            ]

        rationale_refs = (
            field.section_binding_refs
            if drafting_mode == "rationale_bound_section_drafting"
            else []
        )
        section_drafts.append(
            ControlledDraftSectionModel(
                section_id=f"draft_section.{field.field_id}",
                section_title=field.display_name,
                draft_text=draft_text,
                field_ids=[field.field_id],
                rationale_refs=list(rationale_refs),
                limitation_statements=limitations,
                reviewer_attention_points=[
                    f"Review controlled input for field: {field.field_id}"
                ],
            )
        )

    return section_drafts


def _build_limitation_statements(
    drafting_mode,
    missing_required_fields: list[DocumentInputSchemaFieldModel],
    placeholders: list[ControlledDraftPlaceholderModel],
) -> list[str]:
    limitations = [
        "M29.5 controlled drafting creates bounded draft packets only.",
        "This output is not a product-ready document and is not rendered/exported.",
    ]

    if missing_required_fields:
        missing_ids = ", ".join(field.field_id for field in missing_required_fields)
        limitations.append(f"Missing required field(s) remain visible: {missing_ids}")

    if placeholders:
        limitations.append("Placeholder records must remain visible to reviewers.")

    if drafting_mode == "rationale_bound_section_drafting":
        limitations.append("Section drafts must remain tied to visible rationale references.")

    return limitations


def _build_reviewer_attention_points(
    drafting_mode,
    missing_required_fields: list[DocumentInputSchemaFieldModel],
    schema: DocumentInputSchemaRecordModel,
) -> list[str]:
    attention_points = [
        f"Confirm schema boundary before downstream drafting/output: {schema.schema_id}",
    ]

    for field in missing_required_fields:
        attention_points.append(f"Missing required input requires review: {field.field_id}")

    if drafting_mode == "minimal_scaffold_with_placeholders":
        attention_points.append("Scaffold-only output requires user completion before drafting.")

    return attention_points


def _stringify_value(raw_value: Any) -> str | None:
    if raw_value is None:
        return None

    if isinstance(raw_value, list):
        value = ", ".join(str(item).strip() for item in raw_value if str(item).strip())
    else:
        value = str(raw_value).strip()

    return value or None
