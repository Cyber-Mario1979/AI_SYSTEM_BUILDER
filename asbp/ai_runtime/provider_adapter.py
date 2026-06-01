"Disabled provider adapter boundary for M31.3 governed AI assistance."

from __future__ import annotations

from typing import Protocol

from asbp.ai_runtime.provider_contracts import (
    DISABLED_PROVIDER_KIND,
    build_ai_provider_adapter_boundary_request,
    validate_ai_provider_adapter_boundary_request,
)


class AIProviderExecutionBlocked(RuntimeError):
    """Raised when a provider adapter is asked to execute before authorization."""


class AIProviderAdapter(Protocol):
    """Provider-neutral adapter protocol.

    M31.3 defines the boundary shape only. Concrete provider execution remains
    blocked until later accepted checkpoints authorize context packets, refusal
    rules, output acceptance, evaluation, validation, and runtime integration.
    """

    provider_kind: str

    def build_boundary_request(self, *, adapter_request_id: str) -> dict[str, object]:
        """Return a validated provider boundary request."""

    def execute(self, request: dict[str, object]) -> dict[str, object]:
        """Execute a provider request when a later checkpoint authorizes it."""


class DisabledAIProviderAdapter:
    """Disabled adapter proving the M31.3 boundary without model execution."""

    provider_kind = DISABLED_PROVIDER_KIND

    def build_boundary_request(self, *, adapter_request_id: str) -> dict[str, object]:
        """Build the only executable-safe M31.3 boundary request."""
        return build_ai_provider_adapter_boundary_request(
            adapter_request_id=adapter_request_id,
            provider_kind=self.provider_kind,
        )

    def execute(self, request: dict[str, object]) -> dict[str, object]:
        """Reject execution until a later checkpoint authorizes real providers."""
        validate_ai_provider_adapter_boundary_request(request)
        raise AIProviderExecutionBlocked(
            "M31.3 defines provider-neutral adapter boundaries only; "
            "real provider calls, local model inference, and prompt execution "
            "remain blocked until later accepted checkpoints."
        )
