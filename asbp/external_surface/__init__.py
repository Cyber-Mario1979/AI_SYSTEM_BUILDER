"""Shared external-surface contract discipline for ASBP.

The external-surface layer aligns API and UI contract vocabulary only.
It must not own domain logic, validation truth, execution truth, source truth,
raw state access, raw persistence access, deployment behavior, or
productization behavior.
"""

from .contracts import (
    FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS,
    FORBIDDEN_EXTERNAL_BEHAVIORS,
    SUPPORTED_EXTERNAL_CONTRACT_FIELDS,
    SUPPORTED_EXTERNAL_SURFACE_CHANNELS,
    SUPPORTED_EXTERNAL_SURFACE_ROLES,
    ExternalContractCompatibilityDecision,
    ExternalContractCompatibilityResult,
    ExternalContractDiscipline,
    ExternalContractField,
    ExternalSurfaceChannel,
    ExternalSurfaceRole,
    build_external_contract_discipline,
    evaluate_external_contract_compatibility,
    get_supported_external_contract_fields,
    normalize_external_contract_field,
    normalize_external_surface_channel,
    normalize_external_surface_role,
)

__all__ = [
    "FORBIDDEN_EXTERNAL_AUTHORITY_CLAIMS",
    "FORBIDDEN_EXTERNAL_BEHAVIORS",
    "SUPPORTED_EXTERNAL_CONTRACT_FIELDS",
    "SUPPORTED_EXTERNAL_SURFACE_CHANNELS",
    "SUPPORTED_EXTERNAL_SURFACE_ROLES",
    "ExternalContractCompatibilityDecision",
    "ExternalContractCompatibilityResult",
    "ExternalContractDiscipline",
    "ExternalContractField",
    "ExternalSurfaceChannel",
    "ExternalSurfaceRole",
    "build_external_contract_discipline",
    "evaluate_external_contract_compatibility",
    "get_supported_external_contract_fields",
    "normalize_external_contract_field",
    "normalize_external_surface_channel",
    "normalize_external_surface_role",
]