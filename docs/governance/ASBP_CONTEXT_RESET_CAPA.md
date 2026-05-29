---
doc_type: capa_record
canonical_name: ASBP_CONTEXT_RESET_CAPA
status: ACTIVE
governs_execution: true
document_state_mode: active_capa_record
authority: active_context_boundary_and_build_first_control
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
created_date: 2026-05-30
---

# ASBP Context Reset CAPA

## Purpose

This CAPA records the correction for repeated ASBP drift into governance-only work when the active checkpoint requires implementation, source, data, code, model, contract, validator, loader, product workflow, or test evidence.

## Deviation

The observed pattern was:

```text
build/content checkpoint requested
old governance/recovery patterns dominate the response
control or Markdown artifact is treated as progress
implementation/source evidence is delayed or absent
```

This is an execution deviation because governance defines the boundary, but implementation proves progress.

## Root Cause

Primary cause:
ASBP execution rules allowed governance/control artifacts to be treated as progress in build/content or hybrid checkpoints unless a stronger hard stop prevented it.

Contributing cause:
The old ASBP Project workspace accumulated many long historical chats. That workspace is no longer execution-neutral and must be treated as archive/reference only.

System cause:
The active execution context was not bounded strongly enough. The system did not force a clean separation between current repo truth, current execution pack, and historical Project chat material.

## Containment

The old ASBP Project workspace is archive/reference only for live execution.

Do not use it for PLAN, GO, tracker movement, checkpoint closure, PR preparation, issue preparation, milestone closeout, or implementation claims.

Use one of these instead:

1. a clean Project for the current milestone or lane;
2. a fresh chat with a bounded execution pack;
3. a repo-driven connector session that explicitly treats old Project chat history as non-authoritative.

## Corrective Action

The repository now contains:

- `docs/governance/ACTIVE_CONTEXT_BOUNDARY_POLICY.md`
- this CAPA record
- tracker wording that records the active context reset CAPA without moving roadmap progress

## Preventive Action

Before every PLAN, GO, tracker update, checkpoint closeout, PR preparation, or issue preparation, the assistant must declare:

1. active execution context;
2. active source set;
3. active branch and relation when available;
4. current phase, milestone, and checkpoint;
5. checkpoint execution mode;
6. implementation/source minimum;
7. validation evidence required;
8. tracker movement rule;
9. explicit non-implementation claims.

## Build-First Requirement

For build/content and hybrid checkpoints:

- Markdown-only output is not milestone progress.
- Governance artifacts may support the checkpoint but may not complete it.
- PLAN must identify the implementation/source artifact that must change.
- GO must create or modify implementation/source evidence before tracker movement or closeout.

## Closure Criteria

This CAPA remains active until:

1. future execution happens from a clean bounded context;
2. active Project instructions include the context boundary rule;
3. the next build/content or hybrid checkpoint creates implementation/source evidence before tracker movement;
4. the Project Owner accepts that the control is working.

## Non-Implementation Claims

This CAPA does not implement product behavior, document generation, template selection, standards retrieval, model/provider integration, UI/API behavior, deployment, or productization.

It is a repo-side execution-control CAPA only.
