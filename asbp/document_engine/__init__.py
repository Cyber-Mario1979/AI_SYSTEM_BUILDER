"""Document-engine foundation package for the M12.1 template-governance baseline."""

from .template_governance import (
    AUTHORITATIVE_TEMPLATE_SOURCE_ROLE,
    CHECKPOINT_ID,
    EXACT_VERSION_PINNED_SELECTION_MODE,
    GOVERNED_TEMPLATE_ARTIFACT_KIND,
    NON_AUTHORITATIVE_SUPPORTING_CONTENT_POLICY,
    SUPPORTING_TEMPLATE_ARTIFACT_KIND,
    SUPPORTED_TEMPLATE_ARTIFACT_KINDS,
    SUPPORTED_TEMPLATE_FAMILIES,
    build_governed_template_retrieval_request,
    build_template_governance_baseline,
    validate_template_identity,
    validate_template_retrieval_request,
)

__all__ = [
    "AUTHORITATIVE_TEMPLATE_SOURCE_ROLE",
    "CHECKPOINT_ID",
    "EXACT_VERSION_PINNED_SELECTION_MODE",
    "GOVERNED_TEMPLATE_ARTIFACT_KIND",
    "NON_AUTHORITATIVE_SUPPORTING_CONTENT_POLICY",
    "SUPPORTING_TEMPLATE_ARTIFACT_KIND",
    "SUPPORTED_TEMPLATE_ARTIFACT_KINDS",
    "SUPPORTED_TEMPLATE_FAMILIES",
    "build_governed_template_retrieval_request",
    "build_template_governance_baseline",
    "validate_template_identity",
    "validate_template_retrieval_request",
]