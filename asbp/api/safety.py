"""API safety and adapter isolation rules for ASBP.

M19.4 defines fail-closed safety checks for API intake. It does not introduce
routes, framework behavior, endpoint behavior, command execution, production
authentication/authorization, UI behavior, or cloud/deployment assumptions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from .contracts import ApiResponse, build_error_response, build_success_response


class ApiSafetyAction(StrEnum):
    """Stable API intake action vocabulary for safety checks."""

    READ_ONLY = "read_only"
    CONTRACT_VALIDATION = "contract_validation"
    STATE_CHANGING = "state_changing"
    COMMAND = "command"


SAFE_API_INTAKE_ACTIONS = frozenset(
    {
        ApiSafetyAction.READ_ONLY.value,
        ApiSafetyAction.CONTRACT_VALIDATION.value,
    }
)

UNSAFE_API_INTAKE_ACTIONS = frozenset(
    {
        ApiSafetyAction.STATE_CHANGING.value,
        ApiSafetyAction.COMMAND.value,
    }
)

_ACTION_ALIASES = {
    "read": ApiSafetyAction.READ_ONLY.value,
    "read_only": ApiSafetyAction.READ_ONLY.value,
    "show": ApiSafetyAction.READ_ONLY.value,
    "list": ApiSafetyAction.READ_ONLY.value,
    "contract_check": ApiSafetyAction.CONTRACT_VALIDATION.value,
    "contract_validation": ApiSafetyAction.CONTRACT_VALIDATION.value,
    "validate": ApiSafetyAction.CONTRACT_VALIDATION.value,
    "command": ApiSafetyAction.COMMAND.value,
    "execute": ApiSafetyAction.COMMAND.value,
    "write": ApiSafetyAction.STATE_CHANGING.value,
    "mutation": ApiSafetyAction.STATE_CHANGING.value,
    "state_changing": ApiSafetyAction.STATE_CHANGING.value,
    "create": ApiSafetyAction.STATE_CHANGING.value,
    "update": ApiSafetyAction.STATE_CHANGING.value,
    "delete": ApiSafetyAction.STATE_CHANGING.value,
}


@dataclass(frozen=True)
class ApiSafetyDecision:
    """Deterministic safety decision for one API intake action."""

    action: str
    normalized_action: str
    allowed: bool
    reason: str
    response: ApiResponse

    def to_dict(self) -> dict[str, object]:
        return {
            "action": self.action,
            "normalized_action": self.normalized_action,
            "allowed": self.allowed,
            "reason": self.reason,
            "response": self.response.to_dict(),
        }


def normalize_api_intake_action(action: str) -> str:
    """Normalize an API intake action without guessing unsupported meanings."""

    if not isinstance(action, str) or not action.strip():
        raise ValueError("API intake action must be a non-empty string")

    normalized = action.strip().lower().replace("-", "_").replace(" ", "_")
    return _ACTION_ALIASES.get(normalized, normalized)


def evaluate_api_intake_safety(action: str) -> ApiSafetyDecision:
    """Evaluate whether one API intake action is currently safe.

    Unknown, unsafe, command-like, or mutation-like actions fail closed.
    """

    try:
        normalized_action = normalize_api_intake_action(action)
    except ValueError as exc:
        return ApiSafetyDecision(
            action=action,
            normalized_action="",
            allowed=False,
            reason="invalid_api_intake_action",
            response=build_error_response(
                code="API_SAFETY_INVALID_ACTION",
                message=str(exc),
                details={"action": action},
            ),
        )

    if normalized_action in SAFE_API_INTAKE_ACTIONS:
        return ApiSafetyDecision(
            action=action,
            normalized_action=normalized_action,
            allowed=True,
            reason="api_intake_action_allowed",
            response=build_success_response(
                payload={
                    "action": normalized_action,
                    "allowed": True,
                    "reason": "api_intake_action_allowed",
                }
            ),
        )

    if normalized_action in UNSAFE_API_INTAKE_ACTIONS:
        return ApiSafetyDecision(
            action=action,
            normalized_action=normalized_action,
            allowed=False,
            reason="api_intake_action_fails_closed",
            response=build_error_response(
                code="API_SAFETY_UNSAFE_ACTION",
                message=(
                    "API intake action is unsafe for the current checkpoint "
                    "and must fail closed."
                ),
                details={
                    "action": normalized_action,
                    "safe_actions": sorted(SAFE_API_INTAKE_ACTIONS),
                },
            ),
        )

    return ApiSafetyDecision(
        action=action,
        normalized_action=normalized_action,
        allowed=False,
        reason="unknown_api_intake_action_fails_closed",
        response=build_error_response(
            code="API_SAFETY_UNKNOWN_ACTION",
            message="API intake action is not recognized and must fail closed.",
            details={
                "action": normalized_action,
                "safe_actions": sorted(SAFE_API_INTAKE_ACTIONS),
            },
        ),
    )


def is_api_intake_action_allowed(action: str) -> bool:
    """Return whether one API intake action passes the safety gate."""

    return evaluate_api_intake_safety(action).allowed
