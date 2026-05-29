---
doc_type: governance_policy
canonical_name: ACTIVE_CONTEXT_BOUNDARY_POLICY
status: ACTIVE
governs_execution: true
document_state_mode: execution_context_control
authority: active_context_boundary_control
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
created_date: 2026-05-30
---

# Active Context Boundary Policy

## Purpose

This policy prevents ASBP execution from being driven by old Project workspace history instead of the current repo truth and bounded execution pack.

The old ASBP Project workspace is archive/reference only for execution because it contains a large amount of long historical chat context.

## Authority

This policy supplements:

- `ROADMAP_CANONICAL.md`
- `PROGRESS_TRACKER.md`
- `ARCHITECTURE_GUARDRAILS.md`
- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`
- `docs/governance/BUILD_GOVERNANCE_BALANCE_POLICY.md`

It does not move roadmap state and does not replace implementation evidence.

## Active Context Rule

Before `PLAN`, `GO`, tracker movement, checkpoint closure, PR preparation, issue preparation, or milestone closeout, the assistant must confirm that it is working from a bounded active context.

Allowed active contexts are:

1. a clean Project created for the current execution lane or milestone;
2. a fresh chat supplied with a bounded execution pack;
3. a repo-driven connector session where old Project chat history is explicitly non-authoritative.

Historical chats, old recovery discussions, stale generated notes, memory, and previous Project conversations are reference only. They are not execution authority.

If the active context is not bounded, stop with:

```text
PROJECT CONTEXT VIOLATION:
Active context is not bounded.
Do not PLAN, GO, update tracker, close checkpoint, prepare PR/issue, or claim progress until a clean bounded execution context is established.
```

## Build-First Rule

For build/content and hybrid checkpoints:

- Markdown-only output is not milestone progress.
- Governance/control documents may support a checkpoint but may not complete it.
- `PLAN` must identify the implementation, source, data, code, model, contract, or test artifact that must change.
- `GO` must create or modify implementation/source evidence before tracker movement or closeout.

If the assistant proposes only governance, Markdown, policy, tracker, DDR, control-check, or closeout work for a build/content or hybrid checkpoint, stop with:

```text
BUILD-FIRST VIOLATION:
This checkpoint requires implementation/source evidence before governance-only work can continue.
```

## Session Declaration Requirement

Every ASBP execution session must declare:

1. active execution context;
2. active source set;
3. active branch and relation when available;
4. current phase, milestone, and checkpoint;
5. checkpoint execution mode;
6. implementation/source minimum;
7. validation evidence required;
8. tracker movement rule;
9. explicit non-implementation claims.

## Validation Expectation

This policy is documentation/governance-only.

No executable validation is required unless a separate change modifies code, tests, commands, imports, schemas, runtime behavior, CLI behavior, validators, loaders, or executable contracts.
