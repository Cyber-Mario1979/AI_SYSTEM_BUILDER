---
doc_type: milestone_decision_record
canonical_name: M27_2_SELECTOR_SCOPE_INTENT_MODEL_HARDENING
status: ACTIVE_MODEL
milestone: M27
checkpoint: M27.2
phase: Phase 9 — Roadmap Reset and Local Integrated CQV Product Core
checkpoint_title: Selector and scope-intent model hardening
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
branch: feature/m27-cqv-source-content-expansion
created_date: 2026-05-27
last_updated_date: 2026-05-27
application_mode: user_applied_package
live_repo_write: NO
---

# M27.2 — Selector and Scope-Intent Model Hardening

## Purpose

This artifact defines the selector and scope-intent model for the local integrated CQV product core.

It hardens how controlled preset families, human-confirmed package context, asset/system type, scope, lifecycle event, qualification or validation intent, GMP context, risk/complexity, standards applicability, and user confirmation route a work package toward downstream candidate paths.

This checkpoint defines selector behavior and routing logic only.

It does not implement executable runtime-authoritative lookup, task-pool source records, profile records, calendar records, planning-basis records, mappings, UI/API behavior, persistent asset/equipment memory, document generation, standards retrieval, AI/runtime behavior, or productization behavior.

## Roadmap Alignment

M27 is the execution lane for CQV source content expansion.

M27.2 is limited to selector and scope-intent model hardening.

Roadmap-authorized M27.2 work:

- define selector inputs;
- include type, scope, lifecycle event, risk, standards bundle, and user intent;
- prevent work selection from Work Package type alone.

M27.2 prepares for M27.3 by defining how a selector can identify candidate downstream task-pool families without creating task-pool records.

## Source Basis from M27.1

M27.1 defined the initial controlled preset families:

- `PF-CLEANROOM` — Cleanroom
- `PF-PROCESS-EQUIPMENT` — Process Equipment
- `PF-QC-LAB-EQUIPMENT` — QC Lab Equipment
- `PF-UTILITIES` — Utilities
- `PF-COMPUTERIZED-SYSTEMS` — Computerized Systems
- `PF-MANUAL-FALLBACK` — Manual Fallback

M27.2 must use these preset families as controlled selector inputs.

M27.2 must not reopen the initial preset-family list unless the Project Owner explicitly authorizes a scope change.

## Core Selector Principle

Selector output is a controlled candidate routing decision.

Selector output is not final execution.

Selector output must preserve enough human-confirmed package context before later task-pool, profile, calendar, planning-basis, duration-reference, mapping, standards, document, UI/API, or AI layers consume it.

Work selection must not depend on Work Package type, preset family, asset type, or any single field alone.

## Work Selection Definition

Work selection means the controlled routing decision that determines which downstream work package path, candidate task-pool family, profile class, planning-basis candidate, duration-reference family, standards-bundle applicability, and document expectations may apply.

Work selection is a selector result, not a generated task list.

## Human Context Confirmation Gate

Human context input is mandatory for M27.2 routing because the same asset or system type can require different downstream work depending on scope, lifecycle event, and intent.

The selector must capture or require confirmation of the actual work package instance context before downstream routing is treated as acceptable.

At minimum, the Human Context Confirmation Gate must preserve:

| Field | Requirement | Role |
|---|---|---|
| Work Package Title | Required | Human-readable controlled title for the actual package instance. |
| Asset / System Display Name | Required where applicable | Name of the equipment, system, area, utility, laboratory instrument, or computerized system as represented in the package. |
| Asset Tag / ID | Optional / TBD allowed | Real-world identifier when available. Missing ID must not be invented. |
| Preset Family | Required | Controlled family from M27.1. |
| Asset / System Type | Required | Practical asset/system class used to refine routing beyond the preset family. |
| Scope Statement | Required | What is included in the specific package. |
| Exclusions | Required or explicit `None stated` / `TBD` | What is outside the package boundary. |
| Lifecycle Event | Required | Why this work is occurring now or what event triggered it. |
| Qualification / Validation Intent | Required | What qualification, validation, verification, calibration, assessment, or decommissioning purpose the package is intended to serve. |
| GMP Impact / Operating Context | Conditional | Required where GMP impact or operating context affects route selection. |
| Risk / Complexity | Conditional / later-refined | May guide later task-pool and planning refinement without becoming a full risk model here. |
| Standards Bundle / Applicability | Conditional | Used only where authority exists; no fabricated standards applicability. |
| Manual Confirmation | Required for ambiguity | Required when inputs are incomplete, mixed, unsupported, or ambiguous. |

## Selector Input Model

The selector model includes these controlled input dimensions.

| Selector Input | Purpose | M27.2 Rule |
|---|---|---|
| Preset family | Uses M27.1 preset families as controlled routing inputs. | Must not generate work by itself. |
| Asset / system type | Distinguishes cleanroom, manufacturing equipment, QC laboratory equipment/instrument, utility, computerized system, or mixed context. | Must refine, not replace, preset family. |
| Work Package title | Names the actual work package instance. | Must be human-provided or human-confirmed; must not be invented by selector logic. |
| Asset / system display name | Identifies the real asset/system context for the package. | Required where applicable; missing data remains `TBD` rather than guessed. |
| Scope statement | Defines what is included. | Must be separate from intent. |
| Exclusions | Defines what is outside scope. | Must be captured or explicitly marked `TBD` / `None stated`. |
| Lifecycle event | Defines the triggering event or lifecycle state. | Must be captured separately from qualification/validation intent. |
| Qualification / validation intent | Defines the purpose of the work. | Must be captured separately from lifecycle event and scope. |
| GMP impact / operating context | Captures context that affects qualification depth. | Must not be assumed from asset type alone. |
| Laboratory / QC role | Protects QC Lab Equipment routing from manufacturing-equipment assumptions. | Required when preset family is `PF-QC-LAB-EQUIPMENT` or a laboratory role is present. |
| Risk / complexity | Supports later refinement. | May be captured but does not replace later validation, risk, task-pool, or planning rules. |
| Standards bundle / applicability | Carries source-aware standards context. | Must use available authority only; no standards retrieval or fabricated clause logic. |
| User intent / manual confirmation | Confirms the intended routing. | Required for ambiguous, mixed, unsupported, or fallback cases. |

## Starter Lifecycle Event Set

M27.2 defines a starter lifecycle-event vocabulary for selector hardening.

This set is not executable code and may be refined by later approved work.

| Lifecycle Event ID | Display Name | Use |
|---|---|---|
| `LE-NEW-INSTALLATION` | New Installation | New asset, system, area, utility, instrument, or computerized system introduction. |
| `LE-MODIFICATION-POST-CHANGE` | Modification / Post-Change | Work triggered by approved change or modification. |
| `LE-RELOCATION` | Relocation | Work triggered by moving an asset, system, or instrument. |
| `LE-PERIODIC` | Periodic / Routine | Periodic qualification, verification, review, or recurring controlled activity. |
| `LE-POST-DEVIATION` | Post-Deviation | Work triggered by deviation outcome or investigation requirement. |
| `LE-POST-MALFUNCTION` | Post-Malfunction | Work triggered by malfunction, repair, breakdown, or recovery. |
| `LE-CALIBRATION-CYCLE` | Calibration Cycle | Work triggered by calibration, calibration due, or calibration-linked verification. |
| `LE-DECOMMISSIONING` | Decommissioning | Work related to retirement, removal from service, or decommissioning assessment. |
| `LE-ASSESSMENT-ONLY` | Assessment Only | Assessment, gap review, or decision-support work without immediate execution package claim. |
| `LE-MIXED-OR-OTHER` | Mixed / Other | Mixed or unsupported event requiring manual confirmation. |

## Starter Qualification / Validation Intent Set

M27.2 defines a starter qualification/validation-intent vocabulary for selector hardening.

This set is not executable code and may be refined by later approved work.

| Intent ID | Display Name | Use |
|---|---|---|
| `INT-COMMISSIONING-SUPPORT` | Commissioning Support | Commissioning-related support without claiming full qualification completion. |
| `INT-E2E-QUALIFICATION` | End-to-End Qualification | Broad qualification package path across relevant lifecycle phases. |
| `INT-IQ` | Installation Qualification | IQ-focused work. |
| `INT-OQ` | Operational Qualification | OQ-focused work. |
| `INT-PQ` | Performance Qualification | PQ-focused work. |
| `INT-REQUALIFICATION` | Requalification | Requalification package path. |
| `INT-PERIODIC-VERIFICATION` | Periodic Verification | Periodic verification or continued-state confirmation. |
| `INT-CALIBRATION-LINKAGE` | Calibration / Calibration Linkage | Calibration-related qualification or verification context. |
| `INT-CSV` | Computerized System Validation | CSV or computerized-system validation intent. |
| `INT-POST-CHANGE-QUALIFICATION` | Post-Change Qualification | Qualification or verification after change. |
| `INT-POST-DEVIATION-RECOVERY` | Post-Deviation / Malfunction Recovery | Qualification, verification, or assessment after deviation, malfunction, repair, or recovery. |
| `INT-DECOMMISSIONING` | Decommissioning | Decommissioning qualification or assessment intent. |
| `INT-ASSESSMENT-ONLY` | Assessment Only | Non-executing assessment or planning support. |
| `INT-MIXED-OR-OTHER` | Mixed / Other | Mixed or unsupported intent requiring manual confirmation. |

## Scope and Intent Separation Rules

1. Scope defines what is included in the package.
2. Intent defines why the work is being performed and what kind of CQV outcome is sought.
3. Lifecycle event defines the triggering event or lifecycle state.
4. The same asset/system type may route differently when scope, intent, or lifecycle event changes.
5. Scope, intent, and lifecycle event must not be collapsed into a single free-text field.
6. Missing scope, missing intent, or mixed context must trigger manual confirmation rather than silent routing.

## Candidate Routing Output

M27.2 selector output may define candidate downstream routing only.

A candidate routing output may include:

| Candidate Output | Meaning |
|---|---|
| Candidate work package path | Suggested route family for the package. |
| Candidate task-pool family | Candidate task-pool family to be defined in M27.3. |
| Candidate profile class | Candidate profile class to be defined in M27.4. |
| Candidate calendar / planning-basis need | Planning needs to be defined in M27.5 and M27.6. |
| Candidate standards-bundle applicability | Standards context where authority exists. |
| Candidate document expectations | Future document expectations where later M29 authority exists. |
| Manual confirmation flag | Whether the route requires human confirmation before downstream use. |
| Limitation note | Any ambiguity, missing source, missing authority, or unsupported route. |

Candidate routing output must not create tasks.

Candidate routing output must not mutate persisted project state by itself.

## Ambiguity and Manual Confirmation Rules

Manual confirmation is required when any of the following applies:

- preset family is `PF-MANUAL-FALLBACK`;
- asset/system type is missing, unclear, or mixed;
- scope statement is missing or broad enough to map to multiple downstream paths;
- qualification/validation intent is missing or mixed;
- lifecycle event is missing or mixed;
- QC laboratory equipment has both equipment and computerized-system aspects and the primary route is unclear;
- manufacturing equipment has calibration-only, load-cell-only, partial-scope, or post-event context that may not require full equipment qualification;
- standards applicability is unknown or unavailable;
- the selector detects multiple plausible candidate task-pool families;
- the selector cannot distinguish assessment-only work from execution-package work.

## QC Lab Equipment Routing Rule

QC Lab Equipment is a distinct preset family and must not be hidden under Process Equipment.

Selector behavior must preserve laboratory/instrument-specific context, including where applicable:

- analytical instrument role;
- GMP QC laboratory role;
- calibration linkage;
- qualification linkage;
- computerized-system / CSV linkage;
- data integrity or GxP software context where later standards and validation authority support it.

M27.2 does not implement detailed QC task pools, lab-equipment profiles, calibration rules, or CSV task records. Those remain downstream checkpoints.

## Manual Fallback Control Rule

Manual Fallback is a controlled temporary route.

Manual Fallback must:

- require human confirmation;
- record why a specific preset family was not used;
- preserve scope and intent explicitly;
- prevent silent creation of custom preset families;
- provide enough information for later review or future approved preset-family expansion.

Manual Fallback must not become unlimited preset sprawl.

## Future Asset / Equipment Register Compatibility Note

M27.2 remains compatible with a future asset/equipment register or event-history feature.

For now, selector context is human-provided or human-confirmed.

In a later roadmap-authorized checkpoint, some selector fields may be resolved from an approved asset/equipment register, equipment profile, or event history.

M27.2 does not implement:

- persistent equipment memory;
- asset/equipment register records;
- event logging;
- qualification history;
- calibration history;
- due-date tracking;
- periodic scheduling;
- asset lifecycle dashboards;
- database-backed equipment history.

## Downstream Boundary Rules

M27.2 does not replace later M27 checkpoints.

| Downstream Checkpoint | Boundary |
|---|---|
| M27.3 | Defines authoritative task-pool records. |
| M27.4 | Defines profile records. |
| M27.5 | Defines calendar and work-time model. |
| M27.6 | Defines planning basis and duration model. |
| M27.7 | Defines mapping records. |
| M27.8 | Implements first local product CQV library set where approved. |
| M27.9 | Validates cross-library relationships. |
| M27.10 | Checks stage/commit compatibility. |

## Not Completed / Not Claimed

M27.2 does not claim completion of:

- task-pool source records;
- actual task creation;
- persisted task mutation;
- profile records;
- equipment register / asset history;
- event logging;
- calendar records;
- calibration scheduling;
- planning-basis records;
- duration-reference records;
- mapping records;
- executable runtime-authoritative library loading;
- compiled lookup generation;
- runtime lookup behavior;
- cross-library validation;
- source-to-execution compatibility validation;
- product-ready document templates;
- document generation;
- rendering, export, or reporting behavior;
- standards embedding or retrieval;
- AI/model/provider behavior;
- UI/API behavior;
- productization, SaaS, deployment, or commercial readiness.

## DDR Impact

M27.2 touches DDR-001 and DDR-002 at selector-model scope level only.

M27.2 has DDR-009 awareness because later UI/API or external contract behavior may consume selector outputs through approved adapters.

M27.2 does not close, reopen, downgrade, or reclassify any DDR.

M27.2 does not implement runtime lookup, compiled lookup, productized placeholder-backed behavior, UI/API behavior, document generation, standards retrieval, AI/runtime behavior, persistent asset memory, or productization behavior.

## Acceptance Criteria

M27.2 is acceptable when this artifact confirms:

- selector inputs are defined and bounded;
- M27.1 preset families are used as controlled selector inputs;
- human package context is required before downstream candidate routing is accepted;
- Work Package title, asset/system display name, scope, lifecycle event, and qualification/validation intent are captured as distinct inputs;
- scope, intent, and lifecycle event are not collapsed into one field;
- work selection does not depend on Work Package type, preset family, asset/system type, or any single field alone;
- selector output is a candidate routing decision and not final execution;
- candidate task-pool family remains downstream to M27.3;
- profile records remain downstream to M27.4;
- calendars, planning basis, duration references, and mappings remain downstream to later M27 checkpoints;
- QC Lab Equipment preserves laboratory/instrument-specific routing and does not collapse into Process Equipment;
- Manual Fallback remains controlled and cannot become unlimited preset sprawl;
- future asset/equipment register compatibility is acknowledged without implementation;
- M27.3 can proceed to task-pool source model without reopening selector/scope-intent boundaries.

## Validation Expectation

This is a documentation/governance/source-scope artifact only.

No executable validation is required unless a separate change modifies code, commands, imports, schemas, tests, runtime behavior, CLI behavior, or executable contracts.

## Handoff to M27.3

M27.3 must define authoritative task-pool records separately from selector output.

M27.3 may consume the selector model defined here to identify candidate task-pool families, but persisted project tasks must not be treated as task-pool source truth.
