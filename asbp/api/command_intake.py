"""Minimal API command/intake surfaces for ASBP.

M19.6 introduces deterministic command-intake validation and preview behavior.
It does not introduce HTTP routes, framework behavior, endpoint behavior, raw
state mutation, broad workflow orchestration, AI provider calls, document/report
generation, approval/release authority, or UI/cloud behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType
from typing import Any, Mapping

from .contracts import ApiResponse, build_error_response, build_success_response
from .safety import evaluate_api_intake_safety
from .service_boundary import evaluate_api_dependency_target


class ApiCommandName(StrEnum):
    """Stable minimal command-intake vocabulary."""

    PREVIEW_COMMAND = "preview_command"
    VALIDATE_CONTRACT = "validate_contract"


SUPPORTED_API_COMMANDS = frozenset(command.value for command in ApiCommandName)

_COMMAND_ALIASES = {
    "preview": ApiCommandName.PREVIEW_COMMAND.value,
    "preview_command": ApiCommandName.PREVIEW_COMMAND.value,
    "command_preview": ApiCommandName.PREVIEW_COMMAND.value,
    "intake_preview": ApiCommandName.PREVIEW_COMMAND.value,
    "validate": ApiCommandName.VALIDATE_CONTRACT.value,
    "validate_contract": ApiCommandName.VALIDATE_CONTRACT.value,
    "contract_validation": ApiCommandName.VALIDATE_CONTRACT.value,
    "intake_validation": ApiCommandName.VALIDATE_CONTRACT.value,
}


def _freeze_mapping(value: Mapping[str, Any] | None) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})

    if not isinstance(value, Mapping):
        raise TypeError("payload and metadata values must be mappings")

    return MappingProxyType(dict(value))


@dataclass(frozen=True)
class ApiCommandIntakeRequest:
    """Stable request shape for minimal API command/intake validation."""

    command: str
    target: str = "service"
    payload: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    metadata: Mapping[str, Any] = field(default_factory=lambda: MappingProxyType({}))
    execute: bool = False

    def __post_init__(self) -> None:
        if not isinstance(self.command, str) or not self.command.strip():
            raise ValueError("API command must be a non-empty string")

        if not isinstance(self.target, str) or not self.target.strip():
            raise ValueError("API command target must be a non-empty string")

        if not isinstance(self.execute, bool):
            raise TypeError("execute must be a boolean")

        object.__setattr__(self, "command", self.command.strip())
        object.__setattr__(self, "target", self.target.strip())
        object.__setattr__(self, "payload", _freeze_mapping(self.payload))
        object.__setattr__(self, "metadata", _freeze_mapping(self.metadata))

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": self.command,
            "target": self.target,
            "payload": dict(self.payload),
            "metadata": dict(self.metadata),
            "execute": self.execute,
        }


@dataclass(frozen=True)
class ApiCommandIntakeDecision:
    """Deterministic decision for one API command/intake request."""

    command: str
    normalized_command: str
    target: str
    normalized_target: str
    accepted: bool
    execution_allowed: bool
    reason: str
    response: ApiResponse

    def to_dict(self) -> dict[str, Any]:
        return {
            "command": self.command,
            "normalized_command": self.normalized_command,
            "target": self.target,
            "normalized_target": self.normalized_target,
            "accepted": self.accepted,
            "execution_allowed": self.execution_allowed,
            "reason": self.reason,
            "response": self.response.to_dict(),
        }


def normalize_api_command_name(command: str) -> str:
    """Normalize an API command-intake name without guessing unsupported meanings."""

    if not isinstance(command, str) or not command.strip():
        raise ValueError("API command must be a non-empty string")

    normalized = command.strip().lower().replace("-", "_").replace(" ", "_")
    return _COMMAND_ALIASES.get(normalized, normalized)


def build_api_command_intake_request(
    *,
    command: str,
    target: str = "service",
    payload: Mapping[str, Any] | None = None,
    metadata: Mapping[str, Any] | None = None,
    execute: bool = False,
) -> ApiCommandIntakeRequest:
    """Build a deterministic minimal API command/intake request."""

    return ApiCommandIntakeRequest(
        command=command,
        target=target,
        payload=_freeze_mapping(payload),
        metadata=_freeze_mapping(metadata),
        execute=execute,
    )


def evaluate_api_command_intake(
    request: ApiCommandIntakeRequest,
) -> ApiCommandIntakeDecision:
    """Evaluate a minimal API command/intake request without executing it.

    M19.6 accepts bounded command intake and preview only. Actual command
    execution remains blocked unless a later roadmap-authorized checkpoint
    explicitly allows it.
    """

    try:
        normalized_command = normalize_api_command_name(request.command)
    except ValueError as exc:
        return ApiCommandIntakeDecision(
            command=request.command,
            normalized_command="",
            target=request.target,
            normalized_target="",
            accepted=False,
            execution_allowed=False,
            reason="invalid_api_command",
            response=build_error_response(
                code="API_COMMAND_INTAKE_INVALID",
                message=str(exc),
                details={"command": request.command},
            ),
        )

    if normalized_command not in SUPPORTED_API_COMMANDS:
        return ApiCommandIntakeDecision(
            command=request.command,
            normalized_command=normalized_command,
            target=request.target,
            normalized_target="",
            accepted=False,
            execution_allowed=False,
            reason="unsupported_api_command",
            response=build_error_response(
                code="API_COMMAND_UNSUPPORTED",
                message="API command is not supported by the M19.6 intake boundary.",
                details={
                    "command": normalized_command,
                    "supported_commands": sorted(SUPPORTED_API_COMMANDS),
                },
            ),
        )

    if request.execute:
        safety_decision = evaluate_api_intake_safety("command")
        return ApiCommandIntakeDecision(
            command=request.command,
            normalized_command=normalized_command,
            target=request.target,
            normalized_target="",
            accepted=False,
            execution_allowed=False,
            reason=safety_decision.reason,
            response=safety_decision.response,
        )

    dependency_decision = evaluate_api_dependency_target(request.target)
    if not dependency_decision.allowed:
        return ApiCommandIntakeDecision(
            command=request.command,
            normalized_command=normalized_command,
            target=request.target,
            normalized_target=dependency_decision.normalized_target,
            accepted=False,
            execution_allowed=False,
            reason=dependency_decision.reason,
            response=dependency_decision.response,
        )

    safety_decision = evaluate_api_intake_safety("contract_validation")
    if not safety_decision.allowed:
        return ApiCommandIntakeDecision(
            command=request.command,
            normalized_command=normalized_command,
            target=request.target,
            normalized_target=dependency_decision.normalized_target,
            accepted=False,
            execution_allowed=False,
            reason=safety_decision.reason,
            response=safety_decision.response,
        )

    mode = (
        "contract_validation_only"
        if normalized_command == ApiCommandName.VALIDATE_CONTRACT.value
        else "intake_preview_only"
    )

    return ApiCommandIntakeDecision(
        command=request.command,
        normalized_command=normalized_command,
        target=request.target,
        normalized_target=dependency_decision.normalized_target,
        accepted=True,
        execution_allowed=False,
        reason="api_command_intake_accepted_without_execution",
        response=build_success_response(
            payload={
                "command": normalized_command,
                "target": dependency_decision.normalized_target,
                "accepted": True,
                "execution_allowed": False,
                "mode": mode,
                "request_payload": dict(request.payload),
                "request_metadata": dict(request.metadata),
            }
        ),
    )
