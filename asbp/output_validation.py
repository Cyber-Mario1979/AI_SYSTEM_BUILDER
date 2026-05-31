from __future__ import annotations

from asbp.document_lifecycle_model import DocumentLifecycleRecordModel
from asbp.output_validation_model import (
    REQUIRED_OUTPUT_VALIDATION_NON_IMPLEMENTATION_CLAIMS,
    OutputValidationIssueModel,
    OutputValidationResultModel,
    OutputValidationRuleLibraryModel,
    OutputValidationRuleModel,
)
from asbp.output_validation_store import (
    get_output_validation_rule_by_id,
    get_output_validation_rule_for_format,
    load_default_output_validation_rule_library,
)
from asbp.renderer_output_model import RendererOutputArtifactModel


def validate_output_artifact(
    *,
    validation_id: str,
    artifact: RendererOutputArtifactModel,
    lifecycle_record: DocumentLifecycleRecordModel,
    rule_id: str | None = None,
    rule_library: OutputValidationRuleLibraryModel | None = None,
) -> OutputValidationResultModel:
    rule_library = rule_library or load_default_output_validation_rule_library()
    rule = (
        get_output_validation_rule_by_id(rule_library, rule_id)
        if rule_id is not None
        else get_output_validation_rule_for_format(rule_library, artifact.output_format)
    )

    issues: list[OutputValidationIssueModel] = []

    _validate_artifact_content_presence(artifact, issues)
    _validate_metadata_alignment(artifact, lifecycle_record, issues)
    _validate_placeholder_policy(artifact, issues)
    _validate_limitation_visibility(artifact, issues)
    _validate_standards_warning_visibility(artifact, issues)
    _validate_lifecycle_state_eligibility(lifecycle_record, rule, issues)
    _validate_no_approval_or_release_claim(artifact, issues)

    return OutputValidationResultModel(
        validation_id=validation_id,
        version=_version_from_id(validation_id),
        status="failed" if _has_error(issues) else "passed",
        artifact_id=artifact.artifact_id,
        lifecycle_record_id=lifecycle_record.lifecycle_record_id,
        output_format=artifact.output_format,
        rule_id=rule.rule_id,
        checks_performed=list(rule.required_checks),
        issues=issues,
        explicit_non_implementation_claims=sorted(
            REQUIRED_OUTPUT_VALIDATION_NON_IMPLEMENTATION_CLAIMS
        ),
    )


def assert_output_validation_passes(result: OutputValidationResultModel) -> None:
    if result.status == "passed":
        return

    issue_summary = "; ".join(
        f"{issue.issue_code}: {issue.message}"
        for issue in result.issues
    )
    raise ValueError(f"Output validation failed: {issue_summary}")


def _validate_artifact_content_presence(
    artifact: RendererOutputArtifactModel,
    issues: list[OutputValidationIssueModel],
) -> None:
    if artifact.rendered_content.strip():
        return

    issues.append(
        _issue(
            "EMPTY_RENDERED_CONTENT",
            "Rendered artifact content must not be empty.",
            [artifact.artifact_id],
        )
    )


def _validate_metadata_alignment(
    artifact: RendererOutputArtifactModel,
    lifecycle_record: DocumentLifecycleRecordModel,
    issues: list[OutputValidationIssueModel],
) -> None:
    expected_pairs = [
        ("artifact_id", lifecycle_record.source_artifact_id, artifact.artifact_id),
        ("source_draft_id", lifecycle_record.source_draft_id, artifact.metadata.source_draft_id),
        ("template_id", lifecycle_record.template_id, artifact.metadata.template_id),
        ("schema_id", lifecycle_record.schema_id, artifact.metadata.schema_id),
        (
            "standards_control_packet_id",
            lifecycle_record.standards_control_packet_id,
            artifact.metadata.standards_control_packet_id,
        ),
        ("output_format", lifecycle_record.output_format, artifact.output_format),
    ]

    for field_name, lifecycle_value, artifact_value in expected_pairs:
        if lifecycle_value == artifact_value:
            continue
        issues.append(
            _issue(
                "METADATA_ALIGNMENT_MISMATCH",
                (
                    "Lifecycle record metadata does not match renderer artifact "
                    f"metadata for {field_name}: {lifecycle_value} / {artifact_value}"
                ),
                [lifecycle_record.lifecycle_record_id, artifact.artifact_id],
            )
        )


def _validate_placeholder_policy(
    artifact: RendererOutputArtifactModel,
    issues: list[OutputValidationIssueModel],
) -> None:
    if not artifact.metadata.placeholder_present:
        return

    if "placeholder" in artifact.rendered_content.casefold():
        return

    issues.append(
        _issue(
            "MISSING_PLACEHOLDER_VISIBILITY",
            "Artifact metadata indicates placeholders, but rendered content does not visibly declare placeholders.",
            [artifact.artifact_id],
        )
    )


def _validate_limitation_visibility(
    artifact: RendererOutputArtifactModel,
    issues: list[OutputValidationIssueModel],
) -> None:
    if not artifact.metadata.limitation_present:
        return

    if "limitation" in artifact.rendered_content.casefold():
        return

    issues.append(
        _issue(
            "MISSING_LIMITATION_VISIBILITY",
            "Artifact metadata indicates limitations, but rendered content does not visibly declare limitations.",
            [artifact.artifact_id],
        )
    )


def _validate_standards_warning_visibility(
    artifact: RendererOutputArtifactModel,
    issues: list[OutputValidationIssueModel],
) -> None:
    if not artifact.metadata.standards_warning_present:
        return

    normalized_content = artifact.rendered_content.casefold()
    if "standards" in normalized_content and "warning" in normalized_content:
        return

    issues.append(
        _issue(
            "MISSING_STANDARDS_WARNING_VISIBILITY",
            "Artifact metadata indicates standards warning, but rendered content does not visibly declare standards warning.",
            [artifact.artifact_id],
        )
    )


def _validate_lifecycle_state_eligibility(
    lifecycle_record: DocumentLifecycleRecordModel,
    rule: OutputValidationRuleModel,
    issues: list[OutputValidationIssueModel],
) -> None:
    if lifecycle_record.lifecycle_state in rule.allowed_lifecycle_states:
        return

    issues.append(
        _issue(
            "INELIGIBLE_LIFECYCLE_STATE",
            (
                "Lifecycle state is not eligible for M29.9 output validation: "
                f"{lifecycle_record.lifecycle_state}"
            ),
            [lifecycle_record.lifecycle_record_id],
        )
    )


def _validate_no_approval_or_release_claim(
    artifact: RendererOutputArtifactModel,
    issues: list[OutputValidationIssueModel],
) -> None:
    if not artifact.metadata.non_product_ready:
        issues.append(
            _issue(
                "PRODUCT_READY_CLAIM_NOT_ALLOWED",
                "M29.9 output validation must not validate product-ready release claims.",
                [artifact.artifact_id],
            )
        )

    if artifact.metadata.approval_claimed or artifact.metadata.lifecycle_state_mutated:
        issues.append(
            _issue(
                "APPROVAL_OR_RELEASE_CLAIM_NOT_ALLOWED",
                "M29.9 output validation must not approve, sign, release, or mutate lifecycle state.",
                [artifact.artifact_id],
            )
        )

    normalized_content = artifact.rendered_content.casefold()
    blocked_phrases = [
        "qms approved",
        "electronically signed",
        "approved for release",
        "released for use",
    ]
    matched_phrases = [
        phrase for phrase in blocked_phrases if phrase in normalized_content
    ]
    if matched_phrases:
        issues.append(
            _issue(
                "APPROVAL_OR_RELEASE_CLAIM_NOT_ALLOWED",
                (
                    "Rendered content includes approval/release language blocked "
                    f"by M29.9: {', '.join(matched_phrases)}"
                ),
                [artifact.artifact_id],
            )
        )


def _issue(
    issue_code,
    message: str,
    related_ids: list[str],
) -> OutputValidationIssueModel:
    return OutputValidationIssueModel(
        issue_code=issue_code,
        message=message,
        related_ids=related_ids,
    )


def _has_error(issues: list[OutputValidationIssueModel]) -> bool:
    return any(issue.severity == "error" for issue in issues)


def _version_from_id(identifier: str) -> str:
    return identifier.rsplit("@", 1)[1]
