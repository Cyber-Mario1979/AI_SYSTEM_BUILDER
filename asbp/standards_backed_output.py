from __future__ import annotations

from asbp.controlled_drafting_model import ControlledDraftPacketModel
from asbp.standards_backed_output_model import (
    REQUIRED_STANDARDS_BACKED_OUTPUT_NON_IMPLEMENTATION_CLAIMS,
    StandardsBackedOutputControlPacketModel,
    StandardsBackedOutputSectionControlModel,
    StandardsBackedOutputSourceControlModel,
)
from asbp.standards_bundle_binding_model import StandardsBundleBindingLibraryModel
from asbp.standards_bundle_binding_store import (
    get_standards_bundle_binding_by_id,
    load_default_standards_bundle_binding_library,
)
from asbp.standards_registry_model import StandardsCitationDepth, StandardsRegistryModel
from asbp.standards_registry_store import (
    get_standard_source_by_id,
    load_default_standards_registry,
)


def build_standards_backed_output_controls_for_draft(
    *,
    control_packet_id: str,
    draft_packet: ControlledDraftPacketModel,
    standards_bundle_refs: list[str],
    requested_citation_depth: StandardsCitationDepth = "document",
    registry: StandardsRegistryModel | None = None,
    bundle_library: StandardsBundleBindingLibraryModel | None = None,
) -> StandardsBackedOutputControlPacketModel:
    registry = registry or load_default_standards_registry()
    bundle_library = bundle_library or load_default_standards_bundle_binding_library()

    source_controls = _build_source_controls(
        standards_bundle_refs=standards_bundle_refs,
        requested_citation_depth=requested_citation_depth,
        registry=registry,
        bundle_library=bundle_library,
    )
    section_controls = _build_section_controls(draft_packet, source_controls)
    output_limitation_summary = _build_output_limitation_summary(source_controls)
    has_limited_sources = any(source.requires_visible_limitations() for source in source_controls)

    return StandardsBackedOutputControlPacketModel(
        control_packet_id=control_packet_id,
        version=_version_from_id(control_packet_id),
        draft_id=draft_packet.draft_id,
        template_id=draft_packet.template_id,
        schema_id=draft_packet.schema_id,
        standards_bundle_refs=standards_bundle_refs,
        source_controls=source_controls,
        section_controls=section_controls,
        output_warning_text=(
            "Standards-backed output controls include visible source/citation "
            "limitations; final output remains non-product-ready."
            if has_limited_sources
            else None
        ),
        output_warning_visibility="visible" if has_limited_sources else "not_required",
        output_limitation_summary=output_limitation_summary,
        assumption_records=[
            "Standards-backed output controls are attached to controlled draft packets only.",
            "Standards retrieval and embedding remain out of scope for M29.6.",
        ],
        reviewer_attention_points=[
            "Review source verification status before using standards-backed wording.",
            "Review visible limitation statements before any downstream rendering step.",
        ],
        explicit_non_implementation_claims=sorted(
            REQUIRED_STANDARDS_BACKED_OUTPUT_NON_IMPLEMENTATION_CLAIMS
        ),
    )


def assert_no_product_ready_standards_output_claim(packet: StandardsBackedOutputControlPacketModel) -> None:
    blocked_terms = {
        "product_ready",
        "audit_ready",
        "final_output",
        "rendered_document",
    }
    searchable_values = [
        packet.output_warning_text or "",
        *packet.output_limitation_summary,
        *packet.assumption_records,
        *packet.reviewer_attention_points,
    ]
    for value in searchable_values:
        normalized_value = value.casefold().replace("-", "_").replace(" ", "_")
        if any(term in normalized_value for term in blocked_terms):
            raise ValueError(
                "Standards-backed output controls must not claim product-ready, "
                "audit-ready, final, or rendered output"
            )


def _build_source_controls(
    *,
    standards_bundle_refs: list[str],
    requested_citation_depth: StandardsCitationDepth,
    registry: StandardsRegistryModel,
    bundle_library: StandardsBundleBindingLibraryModel,
) -> list[StandardsBackedOutputSourceControlModel]:
    source_controls: list[StandardsBackedOutputSourceControlModel] = []
    seen_source_ids: set[str] = set()

    for bundle_ref in standards_bundle_refs:
        binding = get_standards_bundle_binding_by_id(bundle_library, bundle_ref)
        for source_binding in binding.source_bindings:
            if source_binding.std_id in seen_source_ids:
                continue
            source_record = get_standard_source_by_id(registry, source_binding.std_id)
            output_available_depths = _output_available_citation_depths(
                list(source_binding.allowed_citation_depths)
            )
            rendered_depth = _resolve_rendered_citation_depth(
                requested_citation_depth,
                output_available_depths,
                source_record.verification_status,
                source_record.version_or_effective_date,
            )
            limitation_statements = _build_source_limitation_statements(
                requested_citation_depth,
                rendered_depth,
                source_record.source_limitations,
                source_binding.source_limitations,
            )
            visible_warning_required = bool(limitation_statements)
            source_controls.append(
                StandardsBackedOutputSourceControlModel(
                    std_id=source_record.std_id,
                    registry_version=source_binding.registry_version,
                    authority_status=source_record.authority_status,
                    verification_status=source_record.verification_status,
                    mandatory_flag=source_record.mandatory_flag,
                    version_or_effective_date=source_record.version_or_effective_date,
                    requested_citation_depth=requested_citation_depth,
                    rendered_citation_depth=rendered_depth,
                    available_citation_depths=output_available_depths,
                    source_limitations=[
                        *source_record.source_limitations,
                        *source_binding.source_limitations,
                    ],
                    limitation_statements=limitation_statements,
                    assumption_records=[
                        "Source status is taken from the controlled standards registry and standards bundle binding.",
                    ],
                    warning_text=(
                        "Visible standards source/citation limitation applies."
                        if visible_warning_required
                        else None
                    ),
                    warning_visibility="visible" if visible_warning_required else "not_required",
                    source_record_ref=f"{binding.bundle_id}::{source_record.std_id}",
                )
            )
            seen_source_ids.add(source_binding.std_id)

    if not source_controls:
        raise ValueError("Standards-backed output controls require at least one source control")

    return source_controls


def _output_available_citation_depths(
    available_citation_depths: list[StandardsCitationDepth],
) -> list[StandardsCitationDepth]:
    # M29.6 output controls may always downgrade to document-level output as
    # the safest visible fallback. This does not upgrade source authority; it
    # preserves source limitations and keeps any downgrade visible.
    normalized_depths: list[StandardsCitationDepth] = []
    for depth in ["document", *available_citation_depths]:
        if depth not in normalized_depths:
            normalized_depths.append(depth)
    return normalized_depths


def _resolve_rendered_citation_depth(
    requested_citation_depth: StandardsCitationDepth,
    available_citation_depths: list[StandardsCitationDepth],
    verification_status: str,
    version_or_effective_date: str,
) -> StandardsCitationDepth:
    if verification_status != "verified":
        return "document"

    if (
        requested_citation_depth == "version"
        and version_or_effective_date.strip().upper() == "TBD"
    ):
        return "document"

    if requested_citation_depth in available_citation_depths:
        return requested_citation_depth

    safe_depths = [
        depth
        for depth in available_citation_depths
        if CITATION_DEPTH_ORDER[depth] <= CITATION_DEPTH_ORDER[requested_citation_depth]
    ]
    if safe_depths:
        return max(safe_depths, key=lambda depth: CITATION_DEPTH_ORDER[depth])

    return "document"


def _build_source_limitation_statements(
    requested_depth: StandardsCitationDepth,
    rendered_depth: StandardsCitationDepth,
    registry_limitations: list[str],
    bundle_limitations: list[str],
) -> list[str]:
    limitation_statements: list[str] = []
    if requested_depth != rendered_depth:
        limitation_statements.append(
            f"Requested citation depth {requested_depth} was limited to {rendered_depth}."
        )
    limitation_statements.extend(registry_limitations)
    limitation_statements.extend(bundle_limitations)
    return limitation_statements


def _build_section_controls(
    draft_packet: ControlledDraftPacketModel,
    source_controls: list[StandardsBackedOutputSourceControlModel],
) -> list[StandardsBackedOutputSectionControlModel]:
    source_refs = [source.std_id for source in source_controls]
    limitation_statements = [
        limitation
        for source in source_controls
        for limitation in source.limitation_statements
    ]
    return [
        StandardsBackedOutputSectionControlModel(
            section_id=section.section_id,
            standards_relevance="standards_relevant",
            standards_source_refs=source_refs,
            citation_limitation_statements=limitation_statements or [
                "No source limitation was triggered for this standards-backed control packet."
            ],
            assumption_records=[
                "Section control references standards source IDs only; it does not generate final standards-backed prose.",
            ],
            reviewer_attention_points=[
                "Confirm standards relevance before downstream document rendering.",
            ],
        )
        for section in draft_packet.section_drafts
    ]


def _build_output_limitation_summary(
    source_controls: list[StandardsBackedOutputSourceControlModel],
) -> list[str]:
    limitations = [
        limitation
        for source in source_controls
        for limitation in source.limitation_statements
    ]
    if limitations:
        return sorted(set(limitations))
    return ["No standards source limitation was triggered by this control packet."]


def _version_from_id(identifier: str) -> str:
    return identifier.rsplit("@", 1)[1]
