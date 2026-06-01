"Provider adapter registry boundary for M31.3 governed AI assistance."

from __future__ import annotations

from asbp.ai_runtime.provider_adapter import DisabledAIProviderAdapter
from asbp.ai_runtime.provider_contracts import (
    DISABLED_PROVIDER_KIND,
    SUPPORTED_PROVIDER_KINDS,
)


class AIProviderAdapterRegistry:
    """Registry for provider-neutral adapters without enabling real providers."""

    def __init__(self) -> None:
        self._adapters = {DISABLED_PROVIDER_KIND: DisabledAIProviderAdapter()}

    def available_provider_kinds(self) -> tuple[str, ...]:
        """Return provider kinds visible at the M31.3 boundary."""
        return tuple(self._adapters.keys())

    def get(self, provider_kind: str = DISABLED_PROVIDER_KIND) -> DisabledAIProviderAdapter:
        """Return a registered adapter or reject unimplemented real providers."""
        if provider_kind not in SUPPORTED_PROVIDER_KINDS:
            raise ValueError(f"Unsupported provider_kind: {provider_kind!r}.")
        try:
            return self._adapters[provider_kind]
        except KeyError as exc:
            raise ValueError(
                f"Provider kind {provider_kind!r} is strategy-only in M31.3 and "
                "has no executable adapter implementation yet."
            ) from exc


def build_ai_provider_adapter_registry() -> AIProviderAdapterRegistry:
    """Build the M31.3 provider adapter registry."""
    return AIProviderAdapterRegistry()
