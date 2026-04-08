---
doc_type: architecture_guardrails
canonical_name: ARCHITECTURE_GUARDRAILS
status: ACTIVE
governs_execution: true
document_state_mode: permanent_governance_reference
authority: permanent_design_governance
scope_type: architectural_boundaries
---

This file defines permanent design boundaries only.
It does not define roadmap direction, live progress, or tracker state.

# ARCHITECTURE_GUARDRAILS

- CLI is an adapter only.
- New domain behavior must attach through approved core module boundaries created by the architectural hardening refactor.
- State/persistence access must go through approved state boundary helpers/modules.
- If a future slice requires bypassing these boundaries, pause implementation and open a planning checkpoint before coding.
