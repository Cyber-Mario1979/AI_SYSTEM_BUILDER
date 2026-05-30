from __future__ import annotations

import csv
from io import StringIO

from asbp.controlled_drafting_model import ControlledDraftPacketModel
from asbp.renderer_output_model import (
    REQUIRED_RENDERER_OUTPUT_NON_IMPLEMENTATION_CLAIMS,
    RendererArtifactMetadataModel,
    RendererOutputArtifactModel,
    RendererOutputFormat,
)
from asbp.renderer_output_store import (
    assert_renderer_output_format_supported,
    load_default_renderer_output_contract,
    media_type_for_renderer_output_format,
)
from asbp.standards_backed_output_model import StandardsBackedOutputControlPacketModel


def render_output_artifact(
    *,
    artifact_id: str,
    output_format: RendererOutputFormat,
    draft_packet: ControlledDraftPacketModel,
    standards_packet: StandardsBackedOutputControlPacketModel,
    artifact_filename: str | None = None,
) -> RendererOutputArtifactModel:
    contract = load_default_renderer_output_contract()
    assert_renderer_output_format_supported(contract, output_format)
    _assert_packet_alignment(draft_packet, standards_packet)

    supported_format = output_format  # narrowed by assertion above
    media_type = media_type_for_renderer_output_format(supported_format)
    artifact_filename = artifact_filename or _default_artifact_filename(
        artifact_id,
        supported_format,
    )

    metadata = RendererArtifactMetadataModel(
        artifact_id=artifact_id,
        output_format=supported_format,
        artifact_filename=artifact_filename,
        media_type=media_type,
        source_draft_id=draft_packet.draft_id,
        template_id=draft_packet.template_id,
        schema_id=draft_packet.schema_id,
        standards_control_packet_id=standards_packet.control_packet_id,
        placeholder_present=bool(draft_packet.placeholders),
        limitation_present=(
            bool(draft_packet.limitation_statements)
            or bool(standards_packet.output_limitation_summary)
        ),
        standards_warning_present=standards_packet.output_warning_visibility == "visible",
        non_product_ready=True,
        lifecycle_state_mutated=False,
        approval_claimed=False,
    )

    if supported_format == "markdown":
        rendered_content = _render_markdown(draft_packet, standards_packet, metadata)
    elif supported_format == "csv_summary":
        rendered_content = _render_csv_summary(draft_packet, standards_packet, metadata)
    else:
        raise ValueError(f"Unsupported renderer output format for M29.7: {output_format}")

    return RendererOutputArtifactModel(
        artifact_id=artifact_id,
        version=_version_from_id(artifact_id),
        output_format=supported_format,
        artifact_filename=artifact_filename,
        media_type=media_type,
        metadata=metadata,
        rendered_content=rendered_content,
        explicit_non_implementation_claims=sorted(
            REQUIRED_RENDERER_OUTPUT_NON_IMPLEMENTATION_CLAIMS
        ),
    )


def _assert_packet_alignment(
    draft_packet: ControlledDraftPacketModel,
    standards_packet: StandardsBackedOutputControlPacketModel,
) -> None:
    if standards_packet.draft_id != draft_packet.draft_id:
        raise ValueError(
            "Renderer standards-backed packet draft_id does not match controlled draft: "
            f"{standards_packet.draft_id} / {draft_packet.draft_id}"
        )

    if standards_packet.template_id != draft_packet.template_id:
        raise ValueError(
            "Renderer standards-backed packet template_id does not match controlled draft: "
            f"{standards_packet.template_id} / {draft_packet.template_id}"
        )

    if standards_packet.schema_id != draft_packet.schema_id:
        raise ValueError(
            "Renderer standards-backed packet schema_id does not match controlled draft: "
            f"{standards_packet.schema_id} / {draft_packet.schema_id}"
        )


def _render_markdown(
    draft_packet: ControlledDraftPacketModel,
    standards_packet: StandardsBackedOutputControlPacketModel,
    metadata: RendererArtifactMetadataModel,
) -> str:
    lines: list[str] = [
        "# Controlled Renderer Output",
        "",
        "> NON-PRODUCT-READY CONTROLLED RENDER. Review required before any downstream use.",
        "",
        "## Artifact Metadata",
        "",
        f"- Artifact ID: {metadata.artifact_id}",
        f"- Output format: {metadata.output_format}",
        f"- Source draft ID: {metadata.source_draft_id}",
        f"- Template ID: {metadata.template_id}",
        f"- Schema ID: {metadata.schema_id}",
        f"- Standards control packet ID: {metadata.standards_control_packet_id}",
        f"- Placeholder present: {metadata.placeholder_present}",
        f"- Limitation present: {metadata.limitation_present}",
        f"- Standards warning present: {metadata.standards_warning_present}",
        f"- Non-product-ready: {metadata.non_product_ready}",
        "",
    ]

    if standards_packet.output_warning_visibility == "visible":
        lines.extend(
            [
                "## Standards Warning",
                "",
                standards_packet.output_warning_text
                or "Visible standards warning required by source controls.",
                "",
            ]
        )

    if draft_packet.supplied_field_values:
        lines.extend(["## Supplied Field Values", ""])
        for field_value in draft_packet.supplied_field_values:
            lines.append(f"- {field_value.field_id}: {field_value.value}")
        lines.append("")

    if draft_packet.placeholders:
        lines.extend(["## Visible Placeholders", ""])
        for placeholder in draft_packet.placeholders:
            lines.append(f"- {placeholder.field_id}: {placeholder.placeholder_text} — {placeholder.reason}")
        lines.append("")

    lines.extend(["## Visible Limitations", ""])
    for limitation in _collect_visible_limitations(draft_packet, standards_packet):
        lines.append(f"- {limitation}")
    lines.append("")

    lines.extend(["## Controlled Sections", ""])
    for section in draft_packet.section_drafts:
        lines.extend(
            [
                f"### {section.section_title}",
                "",
                section.draft_text,
                "",
            ]
        )
        if section.limitation_statements:
            lines.append("Limitations:")
            for limitation in section.limitation_statements:
                lines.append(f"- {limitation}")
            lines.append("")

    lines.extend(["## Reviewer Attention Points", ""])
    for point in [*draft_packet.reviewer_attention_points, *standards_packet.reviewer_attention_points]:
        lines.append(f"- {point}")
    lines.append("")

    return "\n".join(lines).strip() + "\n"


def _render_csv_summary(
    draft_packet: ControlledDraftPacketModel,
    standards_packet: StandardsBackedOutputControlPacketModel,
    metadata: RendererArtifactMetadataModel,
) -> str:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["field", "value"])
    writer.writerow(["artifact_id", metadata.artifact_id])
    writer.writerow(["output_format", metadata.output_format])
    writer.writerow(["source_draft_id", metadata.source_draft_id])
    writer.writerow(["template_id", metadata.template_id])
    writer.writerow(["schema_id", metadata.schema_id])
    writer.writerow(["standards_control_packet_id", metadata.standards_control_packet_id])
    writer.writerow(["placeholder_present", str(metadata.placeholder_present)])
    writer.writerow(["limitation_present", str(metadata.limitation_present)])
    writer.writerow(["standards_warning_present", str(metadata.standards_warning_present)])
    writer.writerow(["non_product_ready", str(metadata.non_product_ready)])
    writer.writerow(["section_count", str(len(draft_packet.section_drafts))])
    writer.writerow(["standards_source_count", str(len(standards_packet.source_controls))])
    return output.getvalue()


def _collect_visible_limitations(
    draft_packet: ControlledDraftPacketModel,
    standards_packet: StandardsBackedOutputControlPacketModel,
) -> list[str]:
    limitations = [
        *draft_packet.limitation_statements,
        *standards_packet.output_limitation_summary,
    ]
    if not limitations:
        return ["No limitation was triggered, but artifact remains non-product-ready."]
    return sorted(set(limitations))


def _default_artifact_filename(
    artifact_id: str,
    output_format: str,
) -> str:
    basename = (
        artifact_id.lower()
        .replace("@", "_")
        .replace("-", "_")
    )
    suffix = {
        "markdown": ".md",
        "csv_summary": ".csv",
    }[output_format]
    return f"{basename}{suffix}"


def _version_from_id(identifier: str) -> str:
    return identifier.rsplit("@", 1)[1]
