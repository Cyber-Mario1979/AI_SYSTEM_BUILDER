# UI Preliminary Boundaries

## Purpose

This document captures early UI and assistant-layer boundaries for ASBP/VALOR-style systems.

It is not a frontend implementation plan.  
It is a guardrail document to prevent backend, CLI, engine, and document-generation decisions from becoming accidentally difficult to support through a future UI.

---

## Core Principle

The system should be primarily controlled through structured UI triggers, while keeping a limited assistant/chat area for advisory discussion.

Target split:

- 85–90% structured UI triggers
- 10–15% assistant/chat advisory space

The chat/assistant layer is not the execution layer.

---

## Execution Boundary

Structured UI triggers should handle execution actions such as:

- Create task
- Update task
- Commit plan
- Validate plan
- Generate schedule
- Create document
- Export artifact
- Update status
- Run pre-flight validation

The assistant/chat layer may discuss, explain, compare, warn, and advise, but should not directly execute controlled actions.

---

## Assistant Advisory Layer

The assistant/chat layer may be used for:

- Discussing CQV approaches
- Comparing options with pros and cons
- Explaining planning risks
- Identifying possible GMP or standards concerns
- Challenging weak assumptions
- Preparing the user before execution
- Explaining validation errors
- Helping the user understand consequences before committing an action

The assistant/chat layer must not directly:

- Commit plans
- Mutate task state
- Create final controlled documents
- Approve workflows
- Change schedules
- Bypass validation
- Generate controlled artifacts without a structured trigger

---

## Standards Citation Rule

When the assistant gives CQV, GMP, qualification, validation, change control, documentation, data integrity, or standards-related advice, it must cite the applicable reference where available.

The reply should include:

- Recommendation
- Reasoning
- Applicable standard, guidance, clause, or internal reference
- Confirmation gaps if the exact reference is unavailable

The assistant must not present unsupported standards-based advice as confirmed.

If the exact reference is not available, the assistant must clearly state that the advice requires standards verification before execution.

---

## Document Creation Principle

Document creation should use the LLM where it is strongest: controlled language output generation.

Execution should remain deterministic.

Document language may be LLM-crafted only within:

- Templates
- Guardrails
- Input schemas
- Pre-flight validation
- Section rules
- Review/export controls

The LLM may improve wording, clarity, structure, and professional expression.

The LLM must not invent:

- Equipment details
- Acceptance criteria
- Standards applicability
- Dates
- Owners
- Scope
- Compliance claims
- Test requirements
- Approval requirements

---

## URS Creation Flow

URS creation should support two paths.

### Path 1: DCF Path

The user completes a Data Collection Form.

Flow:

1. User selects Create URS.
2. System offers DCF path.
3. User completes structured DCF.
4. System validates required fields.
5. System selects URS template and section rules.
6. LLM drafts controlled URS language.
7. Output is checked for missing fields, unsupported assumptions, placeholders, and schema compliance.
8. User reviews and exports.

### Path 2: Minimal Input Path

The user skips the DCF and provides minimum required acceptance data.

Flow:

1. User selects Create URS.
2. User skips DCF.
3. System requests minimum required inputs.
4. System validates minimum acceptance data.
5. System generates a simpler URS with visible TBD placeholders.
6. LLM drafts controlled language only from provided inputs.
7. Output is checked before review/export.

---

## UI-Ready Engine Rule

Every engine action should return structured data, not only printed CLI text.

The CLI can print the result.  
The UI can display the result.  
The API can return the result.  
Tests can verify the result.

A structured action result should include, where applicable:

- Action name
- Success/failure status
- Entity type
- Entity ID
- Before/after values
- Validation messages
- User-facing explanation
- Next allowed actions
- Errors
- Warnings
- References, where relevant

---

## UI Questions to Preserve

The project should keep answering these questions during backend and engine development:

- What entities will the UI need to display?
- What actions will the UI trigger?
- What states must be visible to the user?
- What errors must be understandable in the UI?
- What data should be exposed cleanly instead of buried inside CLI text?
- What should remain engine-internal and never become UI-dependent?
- Which actions require confirmation?
- Which actions can be previewed before commit?
- Which results need auditability?
- Which advisory replies require standards references?
- Which document-generation steps require pre-flight validation?

---

## Final Boundary Statement

The UI should display, trigger, and explain engine behavior.

The engine owns deterministic logic, validation, state transitions, scheduling rules, and controlled mutations.

The assistant advises.

The structured UI triggers execute.

The LLM drafts controlled language only inside validated document-generation workflows.
