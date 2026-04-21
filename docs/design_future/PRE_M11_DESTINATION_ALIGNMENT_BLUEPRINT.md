# PRE_M11_DESTINATION_ALIGNMENT_BLUEPRINT

## Status

Active working design artifact under:

`ROADMAP_ADDENDUM_06_PRE_M11_DESTINATION_ALIGNMENT_AND_DESIGN_READINESS.md`

## Purpose

Finish the design-readiness state for the two governed future tracks before implementation resumes.

This file is not implementation evidence.

This file exists to make the destination explicit enough that the milestones between now and those later future tracks do not accidentally create avoidable refactor pressure.

## Gate outputs required

This file must produce all of the following before the gate may close:

1. Track 1 readiness decomposition
2. Track 2 readiness decomposition
3. cross-track dependency and foundation map
4. milestone-forward alignment map
5. roadmap-facing adoption package input
6. exact implementation re-entry recommendation

---

# A06.1 — Track 1 readiness decomposition

## Track

Library Content Expansion Track

## Checkpoint decision status

Decision baseline recorded.

This checkpoint now resolves the major design-shape questions that were still too vague for safe forward alignment.

## Repo-reality anchor

The current repo already makes the following ideas explicit and therefore they must be treated as protected foundations for future library design:

- selector context is real and currently includes:
  - `system_type`
  - `preset_id`
  - `scope_intent`
  - `standards_bundles`
- standards bundles already have a bounded baseline-plus-add-on pattern:
  - `cqv-core`
  - `cleanroom-hvac`
  - `automation`
- source-of-work distinction is already explicit on tasks:
  - `instantiation_mode = manual`
  - `instantiation_mode = preset_resolved`
  - current source-definition kind is `task_pool`
- orchestration already assumes that binding context must become complete before deterministic planning/execution flow can proceed

These are not yet full library surfaces, but they are already real contracts in the deterministic model and must not be treated as disposable wording.

## Readiness target

Track 1 is design-ready only when all of the following are explicit and bounded:

- canonical library taxonomy
- unit-of-expansion model
- authored-source versus deployment-compiled policy
- validation / freeze policy
- future adoption checkpoint ladder
- protected foundations that intermediate milestones must not violate

## A06.1 final design decisions

### Decision 1 — Canonical top-level taxonomy

The canonical top-level taxonomy for future library growth is:

1. **library artifact kind**
2. **coverage family**
3. **variant / scope layer**

This means the primary axis is **not** domain-only and **not** equipment-only.

The first split must be by library artifact kind because the future system already implies different responsibilities and different compile behavior for:

- selector definitions
- profile definitions
- task-pool definitions
- standards-bundle definitions
- supporting taxonomy / mapping metadata

The second split is coverage family, which may include:

- dosage-form family
- process-equipment family
- utility family
- facility / cleanroom / containment family
- computerized-systems family
- broader manufacturing/domain family where needed

The third split is variant / scope layer, which captures bounded variations such as:

- scope-intent differences
- regional/reference-bundle differences
- family-specific specialization
- deployment-target specialization when needed later

### Decision 2 — Unit of expansion

The correct future unit of expansion is a **coverage pack**.

A coverage pack is a bounded authored unit that may contain coordinated entries across several library artifact kinds for one coherent target coverage family.

A coverage pack may include, when relevant:

- selector entries
- profile entries
- task-pool entries
- standards-bundle references or overlays
- mapping metadata needed for deterministic resolution

This is preferred over expanding one isolated artifact type at a time because the current system direction already couples selector context, standards bundles, task instantiation, and later orchestration/planning readiness.

Therefore:

- the project should not treat task-pool expansion as fully independent from selector expansion
- the project should not treat standards-bundle shaping as fully independent from coverage-family shaping
- the project should not force every future pack to contain every artifact kind, but the coverage-pack model is the canonical coordination unit

### Decision 3 — Authored-source versus deployment-compiled policy

The future library model must explicitly separate:

#### Authored-source surfaces

Human-maintained, granular, reviewable, canonical sources of truth.

These should include:

- selector definitions
- profile definitions
- task-pool definitions
- standards-bundle definitions
- taxonomy and mapping metadata
- cross-link declarations between authored artifacts

#### Deployment-compiled surfaces

Generated, optimized lookup surfaces for later resolver/runtime use.

These should include only what is needed for deterministic lookup and runtime efficiency, for example:

- normalized lookup indexes
- version-pinned manifests
- resolved mapping tables
- compiled bundle manifests
- deployment-facing lookup projections

Rules:

- deployment-compiled surfaces must never become the source of truth
- authored-source content must remain the canonical editable layer
- compilation must happen only after validation/freeze acceptance
- future runtime retrieval must target compiled lookup surfaces where appropriate, but design authority remains with authored sources

### Decision 4 — Validation and freeze policy

A future library family is not acceptable until it passes all applicable checks in four groups:

#### Group A — Structural validity

- schema validity
- required-field validity
- artifact-kind-specific contract validity
- duplicate identity rejection

#### Group B — Identity and taxonomy validity

- naming/id rules
- taxonomy placement validity
- coverage-family placement validity
- variant/scope-layer validity

#### Group C — Cross-library contract validity

- selector-to-task-pool linkage validity
- selector-to-profile linkage validity
- standards-bundle reference validity
- source-definition reference validity
- no dangling cross-library references

#### Group D — Deployment-compile validity

- authored-source versus compiled-output consistency
- deterministic compile result
- no hidden data loss in compiled lookup surfaces
- version/freeze manifest coherence

Freeze rule:

A library family becomes freeze-eligible only when:

- authored artifacts are valid
- cross-library links are valid
- compiled deployment outputs are reproducible
- the pack passes identity/taxonomy checks
- the pack is accepted as a bounded release unit

### Decision 5 — Protected current foundations

The following current repo-real concepts are now treated as protected future foundations:

- selector context remains a first-class binding seed
- `preset_id` remains a real binding concept, not decorative metadata
- `scope_intent` remains a first-class selector input
- `standards_bundles` remain explicit bound context, not hidden assumptions
- `preset_resolved` task instantiation remains a real deterministic path
- `task_pool` remains the first authoritative source-definition kind
- `source_definition_id` remains the explicit bridge from instantiated execution task back to source definition

Intermediate milestones must not erode these foundations through shortcut design decisions.

## Candidate future artifact-kind taxonomy

The canonical future authored library families should be shaped as:

- `selector_library`
- `profile_library`
- `task_pool_library`
- `standards_bundle_library`
- `library_mapping_metadata`

This is a taxonomy of **artifact kinds**, not yet a commitment to final file names or repo directories.

## Candidate future checkpoint ladder for Track 1 adoption

The future adoption ladder for Track 1 should be shaped as:

- `T1.A` Library taxonomy and identity foundation
- `T1.B` Authored-source artifact contracts by library kind
- `T1.C` Cross-library binding and source-resolution contracts
- `T1.D` Validation and freeze pipeline foundation
- `T1.E` Deployment-compiled lookup generation foundation
- `T1.F` Coverage-pack expansion program
- `T1.G` Standards/reference expansion program
- `T1.H` Library governance and release discipline

This ladder is now specific enough to guide later roadmap adoption work.

## Intermediate-milestone anti-drift rules created by A06.1

From this point forward, no intermediate milestone should:

- blur authored-source and deployment-compiled responsibilities
- introduce lookup assumptions that bypass explicit source-definition identity
- reduce selector context to decorative metadata
- treat standards bundles as a loose optional note instead of governed bound context
- create future library-facing behavior directly in CLI adapters
- make local assumptions that only work for one hard-coded coverage family while pretending the design is general

## A06.1 resolved answers to the original open questions

### What is the canonical top-level taxonomy?

Library artifact kind first, coverage family second, variant/scope layer third.

### What is the correct unit of expansion?

A bounded coverage pack.

### What must stay source-authored only?

Selectors, profiles, task pools, standards bundles, taxonomy metadata, and cross-link declarations.

### What must become compiled deployment lookup later?

Normalized runtime lookup indexes, manifests, mapping tables, and deployment-facing projections.

### What validation threshold makes a library family acceptable?

Structural validity, identity/taxonomy validity, cross-library contract validity, and deployment-compile validity must all pass.

### Which parts belong inside the canonical roadmap later versus a separate library-expansion program?

Foundation and governance layers are roadmap-ready candidates later.
Large-scale coverage growth belongs in a dedicated library-expansion program once the foundation layers are adopted.

## A06.1 checkpoint output

A06.1 now establishes that the Library Content Expansion Track is no longer just a vague future note.

It has a concrete design shape, a protected foundation set, a future ladder shape, and explicit anti-drift rules for the milestones that happen before its later implementation.

---

# A06.2 — Track 2 readiness decomposition

## Track

Runtime / Product Layer Decomposition Track

## Checkpoint decision status

Decision baseline recorded.

This checkpoint now resolves the major design-shape questions for the future runtime/product stack so later milestones do not grow on top of vague architecture language.

## Repo-reality anchor

The current repo already establishes a real seed boundary for Track 2, and that accepted seed must govern future decomposition:

- deterministic orchestration already exists as a real layer that builds an orchestration payload from Work Package, collection, task, and plan state
- a runtime boundary layer already exists above orchestration and exposes:
  - `runtime_boundary_state`
  - `eligible_for_prompt_contract`
  - `selected_plan_id`
  - bounded `deterministic_facts`
  - explicit `model_may`
  - explicit `model_may_not`
- helper-defined runtime contract surfaces already exist for:
  - prompt contract shape
  - handoff shape
  - controlled generation instructions
  - candidate response template
  - output contract
- UAT already confirms deterministic blocked-state and execution-ready runtime behavior, bounded prompt-contract behavior, bounded handoff behavior, controlled generation behavior, deterministic candidate acceptance/rejection, and deterministic retry/fail-closed behavior

Therefore the future Track 2 design must grow from this real accepted runtime seed.

It must not pretend the system is still only CLI-level, and it must not pretend a full product stack already exists.

## Readiness target

Track 2 is design-ready only when all of the following are explicit and bounded:

- canonical executable layer map
- current accepted seed boundary
- future layer boundaries
- dependency ordering
- anti-drift rules for intermediate milestones
- candidate future checkpoint ladder
- clear distinction between roadmap-ready foundation layers and broader later productization layers

## A06.2 final design decisions

### Decision 1 — Canonical executable layer map

The canonical future executable layer map is:

#### L0 — Delivery adapters

Examples:

- CLI adapter
- future API adapter
- future UI adapter

Rule:
All delivery surfaces are adapters only.
They are not the home of domain logic, orchestration logic, retrieval logic, or runtime acceptance logic.

#### L1 — Deterministic domain/state core

Examples:

- state models
- persistence boundaries
- entity rules
- cross-entity validation
- planning/state invariants

Rule:
This remains the deterministic truth layer.

#### L2 — Resolver / registry access layer

Examples:

- selector resolution
- profile resolution
- calendar resolution
- task-pool resolution
- standards-bundle resolution
- version-pinned governed lookup

Rule:
This is the first true future layer that is still missing as a distinct mature boundary.

#### L3 — Orchestration / service layer

Examples:

- action routing
- preflight validation
- mutation ordering
- state-to-action coordination
- bounded service-style composition

Rule:
The current orchestration layer is a real seed of this future layer and should evolve into a clearer service boundary rather than being bypassed.

#### L4 — Runtime boundary and contract layer

Examples:

- runtime boundary payloads
- prompt-contract readiness
- structured handoff payloads
- controlled generation request shape
- model permissions and prohibitions

Rule:
The current runtime boundary logic and helper-defined contract surfaces are the accepted seed of this layer.

#### L5 — Controlled generation and decision layer

Examples:

- bounded prose generation
- output validation
- retry control
- fail-closed decision behavior
- accepted-output promotion

Rule:
Generation is downstream from L4 and remains bounded by explicit contracts.

#### L6 — Retrieval layer

This layer must be split conceptually into two bounded categories:

1. **governed deterministic retrieval**
   - version-pinned lookup over compiled/governed library surfaces
   - tightly coupled to resolver/registry rules

2. **probabilistic or search-oriented retrieval**
   - future optional retrieval over broader authored or indexed content
   - must remain explicitly separate from deterministic source resolution

Rule:
Track 2 must never blur deterministic governed resolution with broader probabilistic retrieval.

#### L7 — External product surfaces

Examples:

- API contracts
- UI interaction boundaries
- external request/response shapes
- approval/review flows

Rule:
These surfaces consume stable service/runtime boundaries.
They must not couple directly to CLI command shapes or raw state storage.

#### L8 — Deployment / packaging / production topology layer

Examples:

- packaging strategy
- containerization strategy
- environment separation
- artifact/config separation
- production topology
- observability/evaluation hooks
- maintainability/operational hardening

Rule:
This layer comes last because it should target stable internal boundaries, not unstable intermediate structure.

### Decision 2 — Current accepted seed boundary

The current accepted implementation seed for Track 2 is:

- L0 seed: CLI adapter
- L1 seed: deterministic domain/state core
- L3 seed: orchestration logic
- L4 seed: runtime boundary payload + prompt/handoff/generation contract helpers
- L5 seed: output validation / retry / fail-closed runtime behavior

The current repo does **not** yet provide a mature distinct L2 resolver/registry layer, L6 retrieval layer, L7 API/UI layer, or L8 deployment/topology layer.

That absence is acceptable.
It is now a design fact, not a gap to be filled ad hoc during unrelated milestones.

### Decision 3 — First real future executable layer

The first true future executable layer after the current accepted seed is:

**L2 — Resolver / registry access layer**

Rationale:

- the system already has source-of-work distinction
- the system already has selector context and standards bundles
- the system already has preset-resolved task instantiation semantics
- future runtime/product growth should not jump directly to retrieval, API, UI, or deployment before governed asset resolution has its own explicit boundary

This means the project should not let broader productization outrun governed resolution.

### Decision 4 — Retrieval placement rule

Retrieval must live **after** resolver/registry foundations are explicit and **before** broader runtime/product expansion depends on it.

More precisely:

- governed deterministic retrieval is a downstream consumer of resolver/registry rules
- probabilistic retrieval is a later optional layer that must not redefine deterministic source resolution
- future AI/runtime behavior may consume retrieval outputs, but retrieval must remain structurally separate from generation

Therefore retrieval is not the first future layer.
Resolver/registry comes first.

### Decision 5 — Orchestration / service boundary rule

The future orchestration/service layer must evolve from the current orchestration seed and become the stable coordination boundary above the deterministic core and below delivery surfaces.

Rules:

- CLI must not absorb orchestration responsibilities
- future API/UI must not bypass orchestration/service boundaries
- mutation ordering, preflight checks, and action coordination belong here
- this layer should become the main non-adapter coordination surface for future product growth

### Decision 6 — Runtime boundary rule

The current runtime boundary layer is an accepted architectural seed and must be preserved.

Protected properties:

- structured deterministic-facts payload
- explicit eligibility state
- explicit model permissions
- explicit model prohibitions
- explicit prompt/handoff/generation contract boundaries

Future work may harden and expand this layer, but intermediate milestones must not collapse it into free-form generation or ad hoc adapter logic.

### Decision 7 — API / UI boundary rule

Future API and UI layers are real product goals, but they are **not** foundation layers.

They are downstream adapter/product surfaces that depend on:

- stable resolver rules
- stable orchestration/service rules
- stable runtime boundary contracts
- stable output acceptance rules

Therefore the project must not design API or UI as if they define the internal architecture.
They must sit on top of stable internal layers.

### Decision 8 — Deployment / packaging rule

Deployment, packaging, and production-topology direction become roadmap-worthy only after the project has:

- a stable resolver/registry boundary
- a stable orchestration/service boundary
- a stable runtime boundary
- a stable decision/acceptance layer
- a sufficiently explicit external product boundary if API/UI entry is adopted

Deployment direction must not be used as an excuse to lock early architecture around today’s CLI-centered shape.

## Candidate future checkpoint ladder for Track 2 adoption

The future adoption ladder for Track 2 should be shaped as:

- `T2.A` Executable layer map freeze
- `T2.B` Resolver / registry foundation
- `T2.C` Orchestration / service boundary hardening
- `T2.D` Runtime boundary and contract hardening
- `T2.E` Retrieval separation foundation
- `T2.F` Controlled generation and decision hardening
- `T2.G` API boundary introduction
- `T2.H` UI boundary introduction
- `T2.I` Deployment / packaging / topology foundation
- `T2.J` Production maintainability and observability hardening

This ladder is now explicit enough to guide later roadmap adoption work.

## Track-2 classification of later work

### Roadmap-ready foundation candidates later

The following are credible future canonical-roadmap candidates:

- resolver / registry foundation
- orchestration / service hardening
- runtime boundary / contract hardening
- retrieval separation foundation
- controlled generation / decision hardening

### Broader later productization candidates

The following are credible later productization-program candidates unless the roadmap is intentionally expanded:

- broad API program
- broad UI program
- broad deployment/containerization/topology program
- broader product-operational hardening beyond the bounded foundation layers

This is not yet the final adoption-path decision.
It is the design classification needed for safe forward alignment.

## Intermediate-milestone anti-drift rules created by A06.2

From this point forward, no intermediate milestone should:

- put domain or orchestration logic directly into delivery adapters
- treat CLI command surfaces as if they are the future service boundary
- add AI/runtime behavior that bypasses the runtime boundary layer
- mix deterministic governed resolution with probabilistic retrieval
- let API/UI assumptions drive internal architecture before service/runtime boundaries are stable
- make deployment assumptions against today’s adapter-centric execution shape
- create future-facing behavior that reads like a product layer but actually hard-codes itself to current CLI plumbing

## A06.2 resolved answers to the original open questions

### Which future layers belong inside the canonical roadmap later?

Resolver/registry foundation, orchestration/service hardening, runtime boundary hardening, retrieval separation, and controlled generation/decision hardening are the strongest roadmap candidates.

### Which should remain outside the main roadmap unless intentionally expanded?

Broader API, UI, deployment, packaging, and production-topology programs are the strongest candidates for later dedicated productization treatment.

### What is the first real post-core executable layer?

Resolver / registry access layer.

### Where should retrieval live relative to runtime and source resolution?

After resolver/registry foundations, before broader runtime/product expansion, and always separate from generation.

### When does deployment direction become roadmap-worthy instead of premature?

Only after stable internal boundaries exist for resolver, orchestration/service, runtime boundary, and decision behavior.

## A06.2 checkpoint output

A06.2 now establishes that the Runtime / Product Layer Decomposition Track is no longer a vague future idea.

It has:

- a canonical executable layer map
- an explicit accepted current seed boundary
- a protected future ordering rule
- a later adoption ladder
- clear anti-drift constraints for milestones that occur before later Track 2 implementation

---

# A06.3 — Cross-track dependency and foundation map

## Purpose

Turn the Track 1 and Track 2 decisions into one explicit dependency map so future milestones do not optimize locally in ways that later force structural rework.

This checkpoint is the bridge between:

- Track 1 library-shape readiness
- Track 2 runtime/product layer readiness
- milestone-forward anti-drift execution

## Checkpoint decision status

Decision baseline recorded.

A06.3 now defines:

- the dependency order between the two tracks
- the shared protected foundations
- the anti-drift rules intermediate milestones must obey
- the kinds of shortcut decisions that would create avoidable future refactor pressure

## Cross-track relationship summary

Track 1 and Track 2 are not independent future programs.

They are coupled in one directional way:

- Track 1 defines the shape of governed source artifacts and the authored-source versus deployment-compiled split
- Track 2 defines how future executable layers will resolve, orchestrate, retrieve, expose, and deliver those governed sources

Therefore:

- Track 2 cannot be shaped correctly if Track 1 remains vague
- Track 1 cannot be operationalized later unless Track 2 preserves the right future boundaries for resolver, retrieval, orchestration, and deployment-compiled lookup

This means the project must protect both:

- source-shape correctness
- executable-boundary correctness

at the same time.

## A06.3 final dependency decisions

### Decision 1 — Primary dependency order

The canonical dependency order across the two tracks is:

1. **Track 1 library taxonomy and artifact-kind clarity**
2. **Track 1 authored-source versus deployment-compiled split**
3. **Track 1 cross-library contract discipline**
4. **Track 2 resolver / registry access boundary**
5. **Track 2 orchestration / service boundary**
6. **Track 2 runtime boundary and controlled-generation contract hardening**
7. **Track 2 retrieval separation**
8. **Track 2 external product surfaces**
9. **Track 2 deployment / packaging / production topology**

This order is now authoritative for future alignment reasoning.

### Decision 2 — Why Track 1 comes first

Track 1 comes first because Track 2 needs a stable answer to all of the following before its later layers can mature safely:

- what artifact kinds exist
- what identities and mappings are canonical
- what is source-authored truth
- what may be deployment-compiled
- what cross-library references are governed and valid
- what the runtime is actually resolving when it resolves a preset, task pool, profile, or standards bundle

Without that, future resolver, retrieval, and deployment layers would be built against unstable assumptions.

### Decision 3 — Resolver depends on Track 1, not vice versa

The future resolver / registry layer is the first real executable consumer of Track 1 design.

Therefore:

- Track 1 does **not** wait on retrieval
- Track 1 does **not** wait on UI
- Track 1 does **not** wait on deployment topology

Instead:

- resolver/registry is the first layer that must faithfully operationalize Track 1 contracts
- retrieval later depends on resolver/registry and must not redefine source authority
- deployment-compiled lookup later depends on both Track 1 compile policy and Track 2 resolver/retrieval boundaries

### Decision 4 — Orchestration depends on resolver clarity

The orchestration / service layer must not become the place where unresolved source-library ambiguity is “handled informally.”

It should orchestrate actions over already-governed source and state boundaries, not invent missing source semantics.

Therefore future orchestration hardening depends on:

- enough Track 1 clarity for governed sources
- enough resolver/registry clarity for stable asset access

### Decision 5 — Retrieval is downstream from governed resolution

The future retrieval layer depends on two prior conditions:

- Track 1 must already define authored-source and deployment-compiled distinctions
- Track 2 must already define resolver/registry as the governed deterministic access boundary

Therefore retrieval must remain downstream from governed resolution.

It must never silently replace resolver/registry or become the hidden source-of-truth path.

### Decision 6 — External product surfaces are downstream consumers

Future API and UI layers are downstream consumers of all of the following:

- Track 1 source/library clarity
- resolver/registry rules
- orchestration/service boundaries
- runtime boundary contracts
- accepted decision/validation behavior

Therefore API/UI work should not shape those inner layers prematurely.

### Decision 7 — Deployment depends on both tracks being mature enough

Future deployment, packaging, and production topology depend on:

- the authored-source versus deployment-compiled split from Track 1
- the stable executable layer map from Track 2
- clear internal service/runtime boundaries
- no accidental dependence on CLI-specific execution shape

Therefore deployment direction is one of the last dependencies, not one of the first.

## Shared protected foundations

The following foundations are now shared protections across both tracks.

Intermediate milestones must preserve them.

### Foundation F1 — CLI remains an adapter only

No future-facing design may recenter the architecture on CLI behavior.

This remains protected by permanent guardrails and now also by this cross-track map.

### Foundation F2 — Deterministic core remains the truth boundary

The state/model/validation layer remains the deterministic truth boundary.

Future resolver, orchestration, runtime, retrieval, API, UI, and deployment layers must consume this truth through approved boundaries rather than bypass it.

### Foundation F3 — Source-of-work distinction remains explicit

The current distinction between:

- manual task instantiation
- preset-resolved task instantiation
- source definition identity
- instantiated execution state

must remain explicit.

No future milestone may collapse those meanings back into one vague task model.

### Foundation F4 — Selector context remains real binding context

The following remain first-class binding concepts:

- `system_type`
- `preset_id`
- `scope_intent`
- `standards_bundles`

They are not decorative metadata.

They are protected future inputs to resolver, orchestration, and runtime behavior.

### Foundation F5 — Authored-source and deployment-compiled surfaces must remain separable

Future milestones must not create structures that blur:

- authored canonical source artifacts
- deployment-facing compiled lookup artifacts

The split must remain available even before the full compiled pipeline is implemented.

### Foundation F6 — Runtime boundary remains bounded

The existing runtime seed already defines:

- deterministic facts
- eligibility state
- model permissions
- model prohibitions
- bounded contract behavior

No future milestone may bypass this into free-form generation logic.

### Foundation F7 — Deterministic governed resolution must remain distinct from broader retrieval

Future design must preserve a structural difference between:

- governed deterministic asset resolution
- broader retrieval/search behavior

This distinction must survive all intermediate milestone choices.

### Foundation F8 — External product surfaces must depend on stable inner layers

Future API/UI/product surfaces must be downstream of stable internal boundaries.

They must not become the reason those inner boundaries are improvised.

## Cross-track anti-drift rules for intermediate milestones

From this point forward, any intermediate milestone choice is invalid if it does one or more of the following:

### Anti-drift rule 1

Introduces future source-library behavior without preserving the authored-source versus deployment-compiled distinction.

### Anti-drift rule 2

Introduces future runtime/product behavior without respecting the layer order:
resolver first, then orchestration, then runtime boundary hardening, then retrieval, then external product surfaces.

### Anti-drift rule 3

Uses CLI shape as a substitute for future service/API/product boundaries.

### Anti-drift rule 4

Introduces retrieval-like behavior before governed resolver/registry assumptions are explicit.

### Anti-drift rule 5

Adds milestone-local shortcuts that only work because current source coverage is small or hard-coded.

### Anti-drift rule 6

Places future-facing domain behavior directly inside adapters instead of approved core/service-style boundaries.

### Anti-drift rule 7

Lets deployment or packaging assumptions shape internal architecture before inner layer boundaries stabilize.

### Anti-drift rule 8

Treats selector context, standards bundles, or source-definition identity as convenience metadata rather than protected contract inputs.

## Types of future refactor pressure this checkpoint is meant to prevent

A06.3 exists specifically to prevent these classes of later pain:

### Refactor pressure class A — Source-shape correction refactor

Where future library work would force widespread rewriting because the project treated source artifacts, mappings, and compiled lookup as one blurred concept.

### Refactor pressure class B — Resolver bypass refactor

Where future retrieval/runtime work would need major surgery because governed source resolution never got its own explicit boundary.

### Refactor pressure class C — Adapter extraction refactor

Where API/UI/product growth would require pulling real logic back out of CLI adapters.

### Refactor pressure class D — Runtime-boundary repair refactor

Where free-form generation or loose contract behavior would need to be pulled back into bounded runtime surfaces later.

### Refactor pressure class E — Deployment-topology correction refactor

Where packaging/deployment assumptions would have been built against unstable internal shapes rather than mature boundaries.

## Cross-track dependency table

| Order | Dependency                         | Why it comes here                                                               | What must not happen earlier                                                |
| ----- | ---------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 1     | Track 1 taxonomy clarity           | Future resolution needs artifact-kind and coverage-family clarity               | No resolver/retrieval/deployment assumptions against vague source structure |
| 2     | Track 1 authored vs compiled split | Runtime/product layers need to know what is source truth versus compiled lookup | No future lookup layer that blurs canonical sources and compiled artifacts  |
| 3     | Track 1 cross-library contracts    | Stable links are needed before executable layers consume them                   | No orchestration/runtime logic that “fills gaps” in source semantics ad hoc |
| 4     | Track 2 resolver/registry          | First executable consumer of governed source contracts                          | No retrieval/API/UI leapfrogging resolver foundations                       |
| 5     | Track 2 orchestration/service      | Stable coordination layer must sit above resolved/governed assets               | No direct adapter-led coordination as long-term architecture                |
| 6     | Track 2 runtime boundary hardening | Bounded AI/runtime behavior depends on stable orchestration facts               | No free-form generation path bypassing runtime boundary contracts           |
| 7     | Track 2 retrieval separation       | Retrieval must consume governed resolution, not replace it                      | No mixed deterministic/probabilistic access boundary                        |
| 8     | Track 2 external product surfaces  | API/UI should consume stable inner layers                                       | No API/UI-first shaping of internal architecture                            |
| 9     | Track 2 deployment/topology        | Delivery topology must target stable internals                                  | No deployment-driven locking of premature structure                         |

## A06.3 milestone-facing rule

Any future milestone-local choice that materially affects one of the following must be treated as a cross-track decision, not a local-only one:

- library artifact taxonomy
- authored-source versus compiled-output split
- source-definition identity rules
- resolver boundaries
- orchestration/service boundaries
- runtime boundary contracts
- retrieval boundaries
- API boundaries
- UI boundaries
- deployment boundaries

If it materially affects one of these, it must be checked against this map before implementation proceeds.

## A06.3 checkpoint output

A06.3 now establishes one explicit dependency spine across the two future tracks.

That spine says:

- source/library clarity must stabilize before future executable consumption layers mature
- governed resolution must stabilize before retrieval and broader product surfaces
- stable inner layers must exist before external product surfaces and deployment direction

This checkpoint therefore converts the two separate readiness tracks into one shared anti-drift foundation map for all intermediate milestones that happen before their later implementation.

---

# A06.4 — Milestone-forward alignment map

## Purpose

Convert the Track 1 and Track 2 design decisions into forward execution rules for the milestones that happen before those future tracks are implemented.

This checkpoint exists so the project does not resume implementation under a false assumption that upcoming milestones are “local only.”

A06.4 defines what upcoming milestones may safely do, what they must avoid, and what kinds of local choices now count as destination-shaping choices.

## Checkpoint decision status

Decision baseline recorded.

A06.4 now establishes:

- milestone-facing alignment rules
- allowed and not-allowed kinds of intermediate foundations
- pressure areas inside the next milestone family
- mandatory design-check triggers for future milestone-local decisions

## A06.4 alignment principle

From this point forward, the project may resume implementation only if each future milestone decision is checked against this question:

**Does this local choice preserve the future source-library model and future executable layer map, or does it quietly push the system toward a contradictory topology?**

If the answer is uncertain, the choice is not local-only and must be checked against this blueprint before implementation proceeds.

## Canonical forward-alignment stance

The future destination now implies the following implementation stance:

- upcoming milestones may build enabling foundations
- upcoming milestones may harden internal structure
- upcoming milestones may improve maintainability and professional readiness
- upcoming milestones may not silently commit the project to a source model, service model, retrieval model, API model, UI model, or deployment model that conflicts with A06.1 through A06.3

This means forward implementation is allowed again only when it remains destination-compatible.

## A06.4 final alignment decisions

### Decision 1 — M11 is allowed, but only as destination-compatible professionalization

Milestone 11 is not cancelled.

But Milestone 11 must now be interpreted through this design gate.

That means:

- `M11.1` through `M11.9` remain valid roadmap checkpoints
- none of them may be executed in a way that undermines the future library model or future runtime/product layer map
- professionalization work is allowed only if it strengthens boundaries that the future tracks will later depend on

### Decision 2 — What M11.1 may and may not do

`M11.1` — Production structure baseline may now proceed later only if it does all of the following:

#### Allowed direction

- strengthen module boundaries
- improve internal structure around approved core/service/runtime seeds
- improve repository structure in a way that supports later resolver, orchestration, runtime, and product growth
- make source/library-facing and runtime-facing future boundaries easier to adopt later
- preserve CLI-as-adapter governance

#### Not allowed

- freeze the repo around today’s CLI-centric command layout as if that is the future product shape
- create structure that assumes source libraries will remain informal or directly embedded forever
- create structure that hard-wires future delivery layers to current adapters
- make packaging or product-facing structure decisions that leap ahead of resolver/service/runtime boundary maturity

### Decision 3 — What M11.2 may and may not do

`M11.2` — Evaluation and regression baseline may proceed later only if it evaluates the right future-facing contracts.

#### Allowed direction

- strengthen regression discipline around deterministic core behavior
- strengthen regression discipline around orchestration and runtime-boundary contracts
- create evaluation hooks that later resolver/runtime/product layers can inherit
- make future library validation/freeze and future runtime acceptance easier to verify later

#### Not allowed

- define evaluation only around current CLI behavior while ignoring future boundary contracts
- create regression assumptions that would block later authored-source versus compiled-surface separation
- define evaluation in a way that assumes future retrieval or generation can bypass explicit contracts

### Decision 4 — What M11.3 may and may not do

`M11.3` — Versioning discipline may proceed later only if versioning remains compatible with future library and runtime decomposition.

#### Allowed direction

- strengthen version signaling for deterministic system surfaces
- prepare for later version-pinned governed source lookup
- prepare for later compiled deployment artifact versioning
- prepare for later runtime contract versioning

#### Not allowed

- define versioning only at the package/CLI level as if future governed libraries and contracts do not need their own version discipline
- make version rules that erase the distinction between source-authored content and deployment-compiled artifacts

### Decision 5 — What M11.4 must now be interpreted to mean

`M11.4` — Retrieval architecture basics is now one of the highest-pressure checkpoints under this blueprint.

It may proceed later only if interpreted with the A06 rules.

#### Allowed direction

- define retrieval basics that preserve the distinction between:
  - governed deterministic asset resolution
  - broader retrieval/search behavior
- shape retrieval so it is downstream from future resolver/registry foundations
- prepare future retrieval interfaces without letting retrieval become hidden source-of-truth logic

#### Not allowed

- treat retrieval as the first future executable layer
- blur deterministic governed resolution with probabilistic retrieval
- let retrieval redefine source authority
- build retrieval directly against unstable adapter surfaces
- let `M11.4` quietly absorb unresolved resolver/registry concerns

### Decision 6 — What M11.5A through M11.5C may and may not do

`M11.5A` Runtime control hardening, `M11.5B` Failure-discipline hardening, and `M11.5C` Maintainability hardening are allowed later only if they harden the current accepted seeds in the right direction.

#### Allowed direction

- harden the existing runtime boundary seed
- harden bounded contract enforcement
- harden fail-closed behavior
- harden maintainability in core/service/runtime helper boundaries
- make future API/UI/deployment adoption easier by improving internal clarity now

#### Not allowed

- introduce ad hoc generation behavior outside the runtime boundary layer
- hide maintainability problems by pushing more logic into adapters
- create “temporary” shortcuts that would later block resolver/service/runtime decomposition
- optimize only for local convenience at the expense of future layer separation

### Decision 7 — What M11.6 may and may not do

`M11.6` — Architecture cleanup and consolidation is allowed later only if it consolidates toward the approved destination.

#### Allowed direction

- reduce duplication inside approved boundaries
- consolidate helper logic in ways that reinforce future resolver/service/runtime separation
- simplify internal surfaces without erasing future-track distinctions

#### Not allowed

- broad cleanup that collapses meaningful future boundaries into one convenience layer
- consolidation that pulls service/runtime logic back into adapters
- cleanup that makes later Track 1 or Track 2 adoption harder to introduce cleanly

### Decision 8 — Validation, UAT, and closeout checkpoints now have an added burden

Future validation, UAT, and closeout checkpoints are no longer allowed to ask only:

- “did the code pass?”
- “did the milestone finish?”

They must also ask:

- “did this milestone preserve destination compatibility with A06.1 through A06.3?”

This does not mean every milestone gets new implementation scope.
It means each milestone now has a destination-compatibility check as part of safe continuation.

## Milestone-pressure map

The following roadmap checkpoints now carry the highest destination-shaping pressure.

### High pressure

- `M11.1` Production structure baseline
- `M11.3` Versioning discipline
- `M11.4` Retrieval architecture basics
- `M11.5A` Runtime control hardening
- `M11.5B` Failure-discipline hardening
- `M11.5C` Maintainability hardening
- `M11.6` Architecture cleanup and consolidation

### Moderate pressure

- `M11.2` Evaluation and regression baseline
- future roadmap checkpoints that touch richer source libraries or future product boundaries

### Lower pressure but still governed

- milestone validation/UAT/closeout steps, because they now need to confirm compatibility rather than only completion

## Mandatory design-check triggers for future milestone-local decisions

From this point forward, a local milestone choice must be checked against this blueprint before implementation whenever it materially affects one or more of the following:

- source-library taxonomy
- source-authored versus deployment-compiled separation
- version-pinned governed lookup assumptions
- resolver/registry attachment points
- orchestration/service attachment points
- runtime boundary payloads or contract shapes
- retrieval boundaries
- API boundaries
- UI boundaries
- deployment/packaging boundaries
- product topology assumptions

If it affects one of these, it is not just a local implementation detail.

## Safe kinds of intermediate foundations

The following kinds of work are now considered safe future-compatible foundations when done inside the canonical roadmap:

- strengthening adapter/core separation
- improving internal module clarity
- strengthening deterministic contract validation
- strengthening runtime boundary enforcement
- improving regression discipline around explicit contracts
- preparing versioning rules that can later extend to governed libraries and runtime contracts
- reducing duplication in ways that preserve future boundary separation
- making future resolver/service/runtime insertion easier without implementing them yet

## Unsafe kinds of intermediate foundations

The following kinds of work are now considered unsafe while this blueprint governs alignment:

- turning current CLI command structure into the assumed long-term product topology
- embedding future governed source logic directly into adapters or ad hoc helpers
- creating retrieval-like access paths that bypass future resolver rules
- treating compiled deployment lookup as if it is already the source of truth
- making versioning rules that cannot later distinguish source artifacts, compiled artifacts, and runtime contracts
- making packaging/deployment decisions against unstable internal shapes
- using “cleanup” to collapse distinctions that future tracks depend on

## Alignment rules by future-track concern

### Concern A — Future library model

Any intermediate milestone that touches source definitions, presets, profiles, task pools, standards bundles, or versioned lookup assumptions must preserve:

- artifact-kind-first taxonomy logic
- coverage-pack expansion logic
- authored-source truth
- deployment-compiled separability

### Concern B — Future resolver/service/runtime stack

Any intermediate milestone that touches coordination, command routing, runtime facts, prompt/handoff/generation boundaries, or future external access must preserve:

- resolver-before-retrieval ordering
- service boundary growth from orchestration seed
- bounded runtime boundary contracts
- fail-closed control behavior

### Concern C — Future external product surfaces

Any intermediate milestone that touches external-facing structure must preserve:

- API/UI as downstream consumers
- no direct coupling to CLI plumbing
- no topology assumptions before internal boundaries stabilize

### Concern D — Future deployment/product topology

Any intermediate milestone that touches packaging, environment assumptions, artifact location, or maintainability structure must preserve:

- source-authored versus compiled artifact distinction
- stable internal boundaries first
- deployment as downstream of mature internals, not as the driver of them

## A06.4 implementation-resume rule

Implementation may safely resume later only if the resumed checkpoint is executed under all of the following conditions:

- the checkpoint stays inside canonical roadmap scope
- the checkpoint is checked against A06.1 through A06.3
- no local choice contradicts the future destination
- no local choice silently commits the project to a conflicting source or product topology

This is the operational meaning of destination-compatible forward motion.

## A06.4 checkpoint output

A06.4 now turns the future destination into milestone-facing execution discipline.

It establishes that:

- M11 may proceed later, but not naïvely
- `M11.4` retrieval work is especially sensitive and must stay downstream from future resolver logic
- production structure, versioning, runtime hardening, maintainability, and cleanup work must now be judged by destination compatibility as well as local correctness
- any milestone-local decision that materially affects future library or product architecture is no longer “just local”

---

# A06.5 — Roadmap-facing adoption package

## Purpose

Convert A06.1 through A06.4 into a concrete authority package that can guide forward execution without leaving the two future tracks vague again.

This checkpoint does not implement those tracks.

It defines how their now-ready design state must enter future execution authority.

## Checkpoint decision status

Decision baseline recorded.

A06.5 now establishes:

- the adoption recommendation for Track 1
- the adoption recommendation for Track 2
- the exact future authority path for each track
- the named later programs that remain outside immediate canonical execution
- the condition under which implementation may safely resume on the current roadmap

## A06.5 final adoption decision

The adoption decision for both tracks is:

**Option D — Hybrid path**

Meaning:

- bounded foundation layers become future canonical roadmap material
- broader expansion/productization programs remain explicitly named and governed as later programs
- no track is allowed to fall back into vague “future maybe” status
- no track is allowed to distort immediate execution by being shoved into the current checkpoint ladder prematurely

This is the canonical adoption recommendation produced by the gate.

## Track 1 adoption recommendation

### Track

Library Content Expansion Track

### Adoption path

**Hybrid**

### What should become future canonical roadmap material

The following Track 1 layers are now strong candidates for future canonical roadmap authority:

- library taxonomy and identity foundation
- authored-source artifact contract foundation
- cross-library binding and source-resolution contract foundation
- library validation and freeze foundation
- deployment-compiled lookup generation foundation
- library governance and release discipline

These are foundation/governance layers, not bulk expansion layers.

### What should remain a separate named later program

The following Track 1 work should remain a named later program rather than immediate canonical ladder material:

- large coverage-pack expansion across domains/families
- broad selector/profile/task-pool family expansion at scale
- broad standards/reference expansion at scale

### Named later program

`POST_ROADMAP_LIBRARY_COVERAGE_EXPANSION_PROGRAM`

### Why this is the correct adoption path

Track 1 is now design-ready enough to define future foundational authority, but not to justify dropping a large content-expansion program directly into the current roadmap window.

That means:

- foundations should become roadmap material later
- large-scale coverage growth should remain an explicit later program
- neither part should be left vague

## Track 2 adoption recommendation

### Track

Runtime / Product Layer Decomposition Track

### Adoption path

**Hybrid**

### What should become future canonical roadmap material

The following Track 2 layers are now strong candidates for future canonical roadmap authority:

- executable layer map freeze
- resolver / registry foundation
- orchestration / service boundary hardening
- runtime boundary and contract hardening
- retrieval separation foundation
- controlled generation / decision hardening

These are architecture/foundation layers that directly shape the safe future system.

### What should remain a separate named later program

The following Track 2 work should remain a named later program rather than immediate canonical ladder material:

- broad API program
- broad UI program
- broad deployment / packaging / topology program
- broader product-operational hardening beyond bounded foundation layers

### Named later program

`POST_ROADMAP_PRODUCTIZATION_AND_DELIVERY_PROGRAM`

### Why this is the correct adoption path

Track 2 is now design-ready enough to define future foundational architecture authority, but not to justify forcing the whole productization stack into the current roadmap window.

That means:

- architecture foundations should become roadmap material later
- broader productization should remain an explicit later program
- neither part should be left vague

## Exact future authority path

The future authority path is now defined as follows.

### Authority path A — Current execution authority

Until this gate closes, current execution remains paused under:

`ROADMAP_ADDENDUM_06_PRE_M11_DESTINATION_ALIGNMENT_AND_DESIGN_READINESS.md`

### Authority path B — Immediate post-gate implementation authority

After gate closeout, implementation resumes on the current canonical roadmap at the recorded re-entry checkpoint.

However, that resumed implementation must remain destination-compatible with A06.1 through A06.5.

### Authority path C — Future canonical roadmap authority

After current-roadmap execution reaches the appropriate roadmap-extension point, the following should be adopted into future canonical roadmap authority:

#### Future Track 1 foundation family

- taxonomy and identity foundation
- authored-source artifact contracts
- cross-library binding/source-resolution contracts
- validation/freeze foundation
- deployment-compiled lookup generation foundation
- governance/release discipline

#### Future Track 2 foundation family

- executable layer freeze
- resolver/registry foundation
- orchestration/service hardening
- runtime boundary hardening
- retrieval separation foundation
- controlled generation/decision hardening

### Authority path D — Named later program authority

The following must remain explicit named later programs unless a later roadmap amendment intentionally absorbs them:

- `POST_ROADMAP_LIBRARY_COVERAGE_EXPANSION_PROGRAM`
- `POST_ROADMAP_PRODUCTIZATION_AND_DELIVERY_PROGRAM`

These names now replace vague future wording.

## Recommended future checkpoint-family shapes

### Future Track 1 foundation family

Recommended ladder shape:

- taxonomy and identity foundation
- authored-source artifact contracts
- cross-library binding/source-resolution contracts
- validation/freeze foundation
- deployment-compiled lookup generation foundation
- governance/release discipline

### Future Track 2 foundation family

Recommended ladder shape:

- executable layer map freeze
- resolver/registry foundation
- orchestration/service boundary hardening
- runtime boundary/contract hardening
- retrieval separation foundation
- controlled generation/decision hardening

These are not yet inserted into the canonical roadmap text here.
They are now the approved adoption package inputs for the later roadmap-facing step.

## Rules for later absorption into canonical roadmap authority

The following rules now apply:

### Rule 1

Foundation layers may enter the canonical roadmap only as bounded checkpoint families, not as vague umbrella prose.

### Rule 2

Large coverage expansion and broad productization programs must not be silently smuggled into foundation checkpoints.

### Rule 3

If later execution pressure requires one of the named programs earlier than expected, it must enter through an explicit roadmap amendment or later active addendum.

### Rule 4

No future milestone may pretend these two programs do not exist.

### Rule 5

No future milestone may absorb these two programs implicitly through wording drift.

## Recommended roadmap-facing packaging artifacts

The design gate should now treat the following as the expected later packaging outputs:

1. a future canonical roadmap extension package for:
   - Track 1 foundation family
   - Track 2 foundation family

2. continued explicit named-program records for:
   - `POST_ROADMAP_LIBRARY_COVERAGE_EXPANSION_PROGRAM`
   - `POST_ROADMAP_PRODUCTIZATION_AND_DELIVERY_PROGRAM`

3. if later needed, a bounded addendum only when current-roadmap execution encounters genuine pressure that requires earlier incorporation of one of those future families

## Re-entry recommendation produced by A06.5

Implementation should not resume by pretending the future tracks are solved forever.

Implementation should resume only under this rule:

- return to the current canonical roadmap
- resume at the exact recorded re-entry checkpoint
- keep A06.1 through A06.5 as binding destination-alignment authority for milestone-local decisions
- postpone actual insertion of future foundation families into the canonical roadmap text until the gate closeout step records the final re-entry and authority statement

## A06.5 checkpoint output

A06.5 now converts the two future tracks into explicit future authority paths.

It establishes that:

- both tracks are adopted through a hybrid path
- future foundation layers are roadmap-bound candidates
- broader expansion/productization remains explicit named later-program authority
- the project no longer depends on vague future language for either track
- implementation may later resume without losing the destination

---

# A06.6 — Gate closeout and implementation re-entry decision

## Purpose

Close the pre-`M11.1` design-readiness gate only after the project can resume implementation without relying on vague future-target language for either Track 1 or Track 2.

This checkpoint records:

- whether the gate outputs are complete
- whether implementation may safely resume
- the exact re-entry checkpoint
- where the future-track destination authority lives until later canonical roadmap absorption occurs

## Checkpoint decision status

Gate closeout decision recorded.

## Gate-closeout assessment

The gate is considered complete once the finalized A06.1 through A06.5 content is applied in this blueprint.

At that point, the gate outputs are satisfied because the project has:

- Track 1 readiness decomposition
- Track 2 readiness decomposition
- cross-track dependency and foundation map
- milestone-forward alignment map
- roadmap-facing adoption package
- exact implementation re-entry recommendation

## Gate-closeout interpretation

This gate does **not** mean the two future tracks are now implemented.

It means the project no longer needs to guess about them while continuing forward implementation.

The future destination is now explicit enough that:

- intermediate milestones can move again
- local design choices can be checked against a concrete future model
- the project does not need to defer the two tracks back into vague shaping status
- the project does not need to force immediate implementation of those tracks before the roadmap is ready for them

## Re-entry conditions satisfied

Implementation may safely resume because all of the following are now true:

- the future library model has an explicit design shape
- the future runtime/product layer map has an explicit design shape
- the dependency order between source-shape and executable-boundary work is explicit
- the milestone-forward anti-drift rules are explicit
- the adoption path is explicit and no longer vague
- the current roadmap can continue without silently contradicting the intended end-product destination

## Re-entry rule

Forward implementation now resumes on the current canonical roadmap, but under the following permanent operational rule for the remainder of the current roadmap window:

Any milestone-local choice that materially affects future library shape, resolver boundaries, service boundaries, runtime boundaries, retrieval boundaries, API boundaries, UI boundaries, or deployment boundaries must be checked against this completed blueprint before implementation proceeds.

This is now the required meaning of destination-compatible execution.

## Addendum-closeout recommendation

After this section and the finalized A06.1 through A06.5 sections are in place, the design gate is ready to close.

At that point:

- `ROADMAP_ADDENDUM_06_PRE_M11_DESTINATION_ALIGNMENT_AND_DESIGN_READINESS.md` may become `COMPLETED_HISTORICAL`
- the progress tracker should be normalized to the resumed checkpoint
- normal checkpoint execution may continue

## Final re-entry statement

- exact implementation re-entry checkpoint: `M11.1 — Production structure baseline`
- reason implementation may safely resume: the project now has an explicit destination-alignment blueprint, explicit future-track adoption path, and explicit anti-drift rules, so `M11.1` can proceed without relying on vague future shaping language
- future-track destination authority now lives in: `docs/design_future/PRE_M11_DESTINATION_ALIGNMENT_BLUEPRINT.md` as the approved destination-alignment reference for milestone-local compatibility checks until the designated future foundation families are later absorbed into canonical roadmap authority
