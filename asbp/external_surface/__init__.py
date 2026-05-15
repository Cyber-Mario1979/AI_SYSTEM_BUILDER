"""Shared external-surface contract discipline for ASBP.

The external-surface layer aligns API and UI contract vocabulary only.
It must not own domain logic, validation truth, execution truth, source truth,
raw state access, raw persistence access, deployment behavior, or
productization behavior.
"""

from .consistency import (
    FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS,
    SUPPORTED_UI_API_CONSISTENCY_RULES,
    OperatorVisibleState,
    UiApiConsistencyDecision,
    UiApiConsistencyResult,
    UiApiConsistencyRule,
    evaluate_ui_api_consistency,
    get_ui_api_consistency_rule,
    list_ui_api_consistency_rules,
    normalize_operator_visible_state,
)
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
    "FORBIDDEN_UI_API_CONSISTENCY_BEHAVIORS",
    "SUPPORTED_EXTERNAL_CONTRACT_FIELDS",
    "SUPPORTED_EXTERNAL_SURFACE_CHANNELS",
    "SUPPORTED_EXTERNAL_SURFACE_ROLES",
    "SUPPORTED_UI_API_CONSISTENCY_RULES",
    "ExternalContractCompatibilityDecision",
    "ExternalContractCompatibilityResult",
    "ExternalContractDiscipline",
    "ExternalContractField",
    "ExternalSurfaceChannel",
    "ExternalSurfaceRole",
    "OperatorVisibleState",
    "UiApiConsistencyDecision",
    "UiApiConsistencyResult",
    "UiApiConsistencyRule",
    "build_external_contract_discipline",
    "evaluate_external_contract_compatibility",
    "evaluate_ui_api_consistency",
    "get_supported_external_contract_fields",
    "get_ui_api_consistency_rule",
    "list_ui_api_consistency_rules",
    "normalize_external_contract_field",
    "normalize_external_surface_channel",
    "normalize_external_surface_role",
    "normalize_operator_visible_state",
]