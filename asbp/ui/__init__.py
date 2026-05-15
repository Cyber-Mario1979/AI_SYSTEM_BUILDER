"""UI product-surface boundary package.

The UI layer is a downstream product surface and visibility adapter only.
It must consume API/service boundaries and must not own domain logic,
validation truth, execution truth, source truth, or raw persistence access.
"""

from .boundary import UI_BOUNDARY_CONTRACT, UiBoundaryContract, get_ui_boundary_contract
from .interaction_flow import (
    SUPPORTED_UI_INTERACTION_FLOWS,
    UI_INTERACTION_FLOW_CONTRACTS,
    UiActionIntakeDecision,
    UiActionIntakeDecisionResult,
    UiActionIntakeRequest,
    UiInteractionFlowContract,
    UiInteractionFlowName,
    UiInteractionMode,
    build_ui_action_intake_request,
    evaluate_ui_action_intake,
    get_ui_interaction_flow_contract,
    list_ui_interaction_flow_contracts,
    normalize_ui_interaction_flow,
    normalize_ui_interaction_mode,
)

__all__ = [
    "SUPPORTED_UI_INTERACTION_FLOWS",
    "UI_BOUNDARY_CONTRACT",
    "UI_INTERACTION_FLOW_CONTRACTS",
    "UiActionIntakeDecision",
    "UiActionIntakeDecisionResult",
    "UiActionIntakeRequest",
    "UiBoundaryContract",
    "UiInteractionFlowContract",
    "UiInteractionFlowName",
    "UiInteractionMode",
    "build_ui_action_intake_request",
    "evaluate_ui_action_intake",
    "get_ui_boundary_contract",
    "get_ui_interaction_flow_contract",
    "list_ui_interaction_flow_contracts",
    "normalize_ui_interaction_flow",
    "normalize_ui_interaction_mode",
]
