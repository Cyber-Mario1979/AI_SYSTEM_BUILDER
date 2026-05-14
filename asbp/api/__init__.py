"""API adapter boundary package.

The API layer is a downstream adapter surface only.
It must consume approved service/runtime/core boundaries and must not own domain logic,
validation truth, or raw persistence access.
"""

from .boundary import API_BOUNDARY_CONTRACT, get_api_boundary_contract

__all__ = ["API_BOUNDARY_CONTRACT", "get_api_boundary_contract"]
