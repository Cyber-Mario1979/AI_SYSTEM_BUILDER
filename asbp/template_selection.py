from __future__ import annotations

from asbp.document_template_model import (
    DocumentTemplateLibraryModel,
    DocumentTemplateRecordModel,
)
from asbp.document_template_store import (
    get_document_template_by_id,
    load_default_document_template_library,
)
from asbp.mapping_source_model import MappingLibraryModel
from asbp.mapping_source_store import load_default_mapping_library
from asbp.template_selection_model import (
    REQUIRED_TEMPLATE_SELECTION_NON_IMPLEMENTATION_CLAIMS,
    TemplateSelectionCandidateRejectionModel,
    TemplateSelectionInputModel,
    TemplateSelectionResultModel,
)


def select_template_for_request(
    request: TemplateSelectionInputModel,
    *,
    template_library: DocumentTemplateLibraryModel | None = None,
    mapping_library: MappingLibraryModel | None = None,
) -> TemplateSelectionResultModel:
    template_library = template_library or load_default_document_template_library()
    mapping_library = mapping_library or load_default_mapping_library()

    mapped_template_ids, source_mapping_ids = collect_template_ids_from_standard_mappings(
        mapping_library,
        request.standards_bundle_refs,
    )

    matched_templates: list[DocumentTemplateRecordModel] = []
    rejected_candidates: list[TemplateSelectionCandidateRejectionModel] = []

    for template in template_library.template_records:
        rejection = _first_rejection_for_template(
            template,
            request,
            mapped_template_ids,
        )
        if rejection is not None:
            rejected_candidates.append(rejection)
            continue

        matched_templates.append(template)

    candidate_template_ids = [template.template_id for template in matched_templates]

    if len(matched_templates) == 1:
        selected_template = matched_templates[0]
        return TemplateSelectionResultModel(
            selection_id=request.selection_id,
            status="selected",
            selected_template_id=selected_template.template_id,
            candidate_template_ids=candidate_template_ids,
            rejected_candidates=rejected_candidates,
            source_mapping_ids=source_mapping_ids,
            decision_reason=(
                "Selected deterministic template record by document family, "
                "document type, standards-bundle compatibility, standards-to-template "
                "mapping where available, intake route, and active lifecycle status."
            ),
            explicit_non_implementation_claims=sorted(
                REQUIRED_TEMPLATE_SELECTION_NON_IMPLEMENTATION_CLAIMS
            ),
        )

    if not matched_templates:
        return TemplateSelectionResultModel(
            selection_id=request.selection_id,
            status="no_match",
            candidate_template_ids=[],
            rejected_candidates=rejected_candidates,
            source_mapping_ids=source_mapping_ids,
            decision_reason="No deterministic template matched the request constraints.",
            explicit_non_implementation_claims=sorted(
                REQUIRED_TEMPLATE_SELECTION_NON_IMPLEMENTATION_CLAIMS
            ),
        )

    return TemplateSelectionResultModel(
        selection_id=request.selection_id,
        status="ambiguous",
        candidate_template_ids=candidate_template_ids,
        rejected_candidates=rejected_candidates,
        source_mapping_ids=source_mapping_ids,
        decision_reason="Multiple deterministic template records matched the request constraints.",
        explicit_non_implementation_claims=sorted(
            REQUIRED_TEMPLATE_SELECTION_NON_IMPLEMENTATION_CLAIMS
        ),
    )


def load_template_for_request(
    request: TemplateSelectionInputModel,
    *,
    template_library: DocumentTemplateLibraryModel | None = None,
    mapping_library: MappingLibraryModel | None = None,
) -> DocumentTemplateRecordModel:
    template_library = template_library or load_default_document_template_library()
    result = select_template_for_request(
        request,
        template_library=template_library,
        mapping_library=mapping_library,
    )

    if result.status != "selected" or result.selected_template_id is None:
        raise ValueError(
            "Template selection did not resolve to exactly one template: "
            f"{result.status}"
        )

    return get_document_template_by_id(template_library, result.selected_template_id)


def collect_template_ids_from_standard_mappings(
    mapping_library: MappingLibraryModel,
    standards_bundle_refs: list[str],
) -> tuple[set[str], list[str]]:
    if not standards_bundle_refs:
        return set(), []

    requested_standard_refs = set(standards_bundle_refs)
    template_ids: set[str] = set()
    source_mapping_ids: list[str] = []

    for mapping in mapping_library.mappings:
        if mapping.mapping_kind != "standard_to_template":
            continue

        mapping_standard_refs = {
            reference.reference_id
            for reference in mapping.source_refs
            if reference.reference_type == "standard_bundle"
            and reference.reference_status == "resolved_source"
        }
        if not requested_standard_refs.issubset(mapping_standard_refs):
            continue

        for reference in mapping.target_refs:
            if (
                reference.reference_type == "template"
                and reference.reference_status == "resolved_source"
            ):
                template_ids.add(reference.reference_id)

        source_mapping_ids.append(mapping.mapping_id)

    return template_ids, source_mapping_ids


def _first_rejection_for_template(
    template: DocumentTemplateRecordModel,
    request: TemplateSelectionInputModel,
    mapped_template_ids: set[str],
) -> TemplateSelectionCandidateRejectionModel | None:
    if template.lifecycle_status != "active":
        return _build_rejection(
            template,
            "inactive_lifecycle_status",
            "Template record is not active.",
        )

    if template.document_family_id != request.document_family_id:
        return _build_rejection(
            template,
            "document_family_mismatch",
            "Template document family does not match request.",
        )

    if _normalize(template.document_type) != _normalize(request.document_type):
        return _build_rejection(
            template,
            "document_type_mismatch",
            "Template document type does not match request.",
        )

    requested_standards = set(request.standards_bundle_refs)
    template_standards = set(template.standards_bundle_refs)
    if requested_standards and not requested_standards.issubset(template_standards):
        return _build_rejection(
            template,
            "standards_bundle_mismatch",
            "Template does not support all requested standards bundle refs.",
        )

    if mapped_template_ids and template.template_id not in mapped_template_ids:
        return _build_rejection(
            template,
            "standards_mapping_mismatch",
            "Template is not linked by the resolved standards-to-template mapping.",
        )

    if request.intake_route_ref not in template.intake_route_refs:
        return _build_rejection(
            template,
            "intake_route_mismatch",
            "Template does not support requested intake route.",
        )

    return None


def _build_rejection(
    template: DocumentTemplateRecordModel,
    reason_code,
    message: str,
) -> TemplateSelectionCandidateRejectionModel:
    return TemplateSelectionCandidateRejectionModel(
        template_id=template.template_id,
        reason_code=reason_code,
        message=message,
    )


def _normalize(value: str) -> str:
    return " ".join(value.casefold().split())
