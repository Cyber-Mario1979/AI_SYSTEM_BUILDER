"""UI product-surface boundary package.

The UI layer is a downstream product surface and visibility adapter only.
It must consume API/service boundaries and must not own domain logic,
validation truth, execution truth, source truth, or raw persistence access.
"""

from .boundary import UI_BOUNDARY_CONTRACT, UiBoundaryContract, get_ui_boundary_contract

__all__ = [
    "UI_BOUNDARY_CONTRACT",
    "UiBoundaryContract",
    "get_ui_boundary_contract",
]
