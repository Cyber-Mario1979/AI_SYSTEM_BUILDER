# ARCHITECTURE_GUARDRAILS

CLI is an adapter only.
New domain behavior must attach through approved core module boundaries created by the architectural hardening refactor.
State/persistence access must go through approved state boundary helpers/modules.
If a future slice requires bypassing these boundaries, pause implementation and open a planning checkpoint before coding.