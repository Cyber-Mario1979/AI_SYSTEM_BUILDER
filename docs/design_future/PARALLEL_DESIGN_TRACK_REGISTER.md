# PARALLEL_DESIGN_TRACK_REGISTER

## Status

Design-only register.

This file is not a source of project direction.

It is governed by:

`ROADMAP_ADDENDUM_05_PARALLEL_DESIGN_TRACK_GOVERNANCE.md`

This file must not override:

- `ROADMAP_CANONICAL.md`
- active roadmap addenda
- `ARCHITECTURE_GUARDRAILS.md`
- repo reality
- `PROGRESS_TRACKER.md`

## Purpose

Track the maturity of two parallel design tracks while normal implementation continues:

1. Library Content Expansion Track
2. Runtime / Product Layer Decomposition Track

This register exists so both tracks are reviewed deterministically and can mature into roadmap-ready material instead of remaining vague future ideas.

## How to use this register

Update this register only when one of the following occurs:

- milestone closeout review
- targeted update trigger from a completed slice
- mandatory full repo pass
- hard integration decision preparation

This register is for design maturity tracking only.

It is not implementation evidence.

## Review rhythm

### Mandatory milestone-closeout review
At every milestone closeout, review both tracks and update:

- maturity state
- new signals from repo reality
- new gaps
- new integration candidates
- whether anything is roadmap-ready

### Targeted update trigger
Update this register whenever completed work materially affects:

- source-library structure
- binding assumptions
- runtime boundaries
- output architecture
- retrieval direction
- deployment / packaging direction
- UI / service decomposition direction

### Mandatory full repo pass
Required at:

`M10.10` — Milestone 10 closeout

### Hard integration decision gate
Required before:

`M11.1` — Production structure baseline

## Maturity scale

Use the following controlled maturity values:

- `SEED` — acknowledged only
- `SHAPING` — structure is emerging but still incomplete
- `STABLE_DRAFT` — decomposition is coherent enough for serious review
- `ROADMAP_READY` — ready to become roadmap material
- `INTEGRATED` — already adopted into roadmap / addendum / approved future phase
- `DEFERRED_WITH_DECISION_GATE` — intentionally deferred with an explicit next decision point

---

# Track 1 — Library Content Expansion Track

## Track status

- maturity: `SHAPING`
- governing intent: expand the authoritative library content universe deterministically
- current implementation authority: design-only
- integration target: undecided pending hard decision before `M11.1`

## Why this track exists

The project now has an explicit source-library model, but future content expansion still needs structured decomposition.

This track exists to prevent future library growth from remaining vague.

## Current design question

What is the canonical expansion program for future library content?

The current design pressure includes:

- new pharmaceutical domain coverage
- new equipment families
- new utilities
- new process families
- new selector families
- new profile families
- new task-pool families
- new standards / guidance bundle coverage
- expansion policy for authored libraries versus compiled deployment lookup surfaces

## Proposed decomposition ladder

### LCE.1 — Library taxonomy and coverage model
Define the top-level coverage map for future library growth.

Candidate concerns:

- pharmaceutical platform families
- dosage-form families
- manufacturing context families
- utility families
- facility / cleanroom / containment families
- process-equipment families
- computerized-systems families

### LCE.2 — Selector expansion model
Define how new selector families should be introduced.

Candidate concerns:

- selector naming rules
- scope / intent families
- selector-to-binding expectations
- versioning / supersession rules

### LCE.3 — Profile expansion model
Define how new duration / profile families should be introduced.

Candidate concerns:

- profile granularity
- unit policy consistency
- calendar policy assumptions
- cross-domain profile reuse versus specialization

### LCE.4 — Task-pool expansion model
Define how new task-pool families should be introduced.

Candidate concerns:

- baseline task-pool structure
- atomic-task identity rules
- dependency wiring expectations
- optional / event-driven task policy

### LCE.5 — Standards / references expansion model
Define how standards bundles should expand.

Candidate concerns:

- core vs add-on bundles
- regional overlays
- domain-specific bundles
- bundle merge / conflict policy

### LCE.6 — Authored versus deployment library surfaces
Define the relationship between:

- authored source libraries
- bundled library sets
- compiled deployment lookup surfaces

Candidate concerns:

- what stays granular
- what gets compiled
- what gets embedded for runtime lookup
- what must remain human-maintained versus machine-compiled

### LCE.7 — Library validation and freeze rules
Define how a new library family becomes acceptable.

Candidate concerns:

- required schema checks
- required naming checks
- required dependency checks
- required coverage checks
- freeze criteria

## Current open questions

- What is the canonical top-level taxonomy for future library content growth?
- What is the unit of expansion: domain, dosage-form family, equipment family, utility family, or all of them?
- What becomes source-authored only versus deployment-compiled?
- What validation threshold makes a library family roadmap-ready?
- What belongs inside the current roadmap versus a later post-roadmap library program?

## Signals to watch during current execution

- any slice that clarifies deterministic source-of-work assumptions
- any slice that clarifies output-family expectations that depend on upstream content richness
- any repo evidence of content-shape repetition that suggests a reusable authored-library pattern
- any clear gap between current library structure and desired future domain coverage

## Candidate future outcomes

- roadmap-integrated library-expansion milestone family
- dedicated active roadmap addendum for library-expansion governance
- post-roadmap dedicated library program
- hybrid outcome: partial roadmap integration plus later standalone library roadmap

---

# Track 2 — Runtime / Product Layer Decomposition Track

## Track status

- maturity: `SHAPING`
- governing intent: decompose the future post-core system architecture into roadmap-ready executable layers
- current implementation authority: design-only
- integration target: undecided pending hard decision before `M11.1`

## Why this track exists

The roadmap provides clear deterministic and hybrid-runtime sequencing, but the broader future product architecture still needs much more granular decomposition before serious execution planning.

This track exists to prevent the later AI / UI / service / deployment direction from remaining too superficial for implementation.

## Current design question

What is the executable layer map for the future product/runtime architecture after the current core milestones?

## Proposed decomposition ladder

### RPD.1 — Resolver / registry access layer
Define the layer that resolves governed assets and deterministic references.

Candidate concerns:

- selector resolution
- profile resolution
- calendar resolution
- task-pool resolution
- standards-bundle resolution
- version-pinned lookup behavior

### RPD.2 — Orchestration / service layer
Define the layer that coordinates commands and deterministic actions without collapsing into the CLI adapter.

Candidate concerns:

- action routing
- preflight validation
- mutation ordering
- command-to-contract mapping
- stable service boundaries

### RPD.3 — AI runtime layer
Define the bounded AI runtime layer above deterministic state.

Candidate concerns:

- structured handoff points
- generation boundaries
- acceptance / retry / failure surfaces
- runtime control behavior
- future model-provider abstraction if needed

### RPD.4 — Retrieval layer
Define the bounded retrieval layer separately from generation.

Candidate concerns:

- authored-content retrieval
- compiled lookup retrieval
- future embeddings and search
- retrieval-to-generation separation
- deterministic versus probabilistic retrieval boundaries

### RPD.5 — API / external boundary layer
Define external programmatic boundaries.

Candidate concerns:

- API surface shape
- command boundary versus service boundary
- request / response contracts
- auth / tenancy / session assumptions if relevant later

### RPD.6 — UI layer
Define the front-end structure above a stable backend.

Candidate concerns:

- UI surface types
- state projection boundaries
- action invocation boundaries
- review / approval / visibility flows
- UI independence from unstable internal modules

### RPD.7 — Deployment / packaging / containerization layer
Define how the system is packaged and deployed.

Candidate concerns:

- Docker / container strategy
- local versus hosted topology
- runtime packaging boundaries
- artifact/config separation
- operational environment expectations

### RPD.8 — Production topology and maintainability layer
Define mature production structure.

Candidate concerns:

- service boundaries
- maintainability expectations
- observability / evaluation hooks
- scaling assumptions
- future SaaS or multi-user direction if adopted

## Current open questions

- Which of these future layers belong inside the canonical roadmap versus outside it?
- What is the first real post-core executable layer after the current runtime-output work?
- What should become Milestone 11+ material versus a later separate roadmap?
- Where should retrieval live relative to AI runtime and source-library resolution?
- When does Docker / deployment direction become roadmap-worthy instead of premature?

## Signals to watch during current execution

- any slice that clarifies deterministic-to-runtime boundaries
- any slice that reveals a natural resolver layer
- any slice that shows CLI should remain only an adapter
- any slice that reveals stable service-style boundaries
- any repo pressure showing that AI/UI/deployment decomposition is now blocking clarity

## Candidate future outcomes

- roadmap v4 with explicit post-core layer decomposition
- targeted roadmap addendum governing the M11 transition window
- split roadmap approach:
  - core roadmap continuation
  - separate product/runtime roadmap
- post-roadmap professionalization program with explicit layer ladder

---

# Cross-track review log

## Required review entries

Use the template below for each required review.

### Review entry template

- review point:
- trigger type:
- current milestone / checkpoint context:
- Track 1 maturity before:
- Track 1 maturity after:
- Track 2 maturity before:
- Track 2 maturity after:
- new signals:
- new gaps:
- roadmap-ready candidates:
- integration recommendation:
- notes:

## Reserved required review points

- `M10.10` full repo pass
- pre-`M11.1` hard integration decision

### Completed review entry — `M10.10` full repo pass

- review point: `M10.10` full repo pass
- trigger type: mandatory_full_repo_pass_and_milestone_closeout_review
- current milestone / checkpoint context: Milestone 10 closeout after recorded validation checkpoint and passed milestone UAT
- Track 1 maturity before: `SEED`
- Track 1 maturity after: `SHAPING`
- Track 2 maturity before: `SEED`
- Track 2 maturity after: `SHAPING`
- new signals:
  - explicit source-of-work contract enforcement now exists for persisted preset-resolved task records
  - selector-context and standards-bundle shaping pressure is now visible at the binding-context boundary
  - orchestration now provides a clearer planning/input readiness boundary
  - CLI-adapter governance is explicit while runtime/output behavior attaches through core module boundaries
  - runtime/output decomposition now exists across target, contract, mapping, acceptance, retry, family, consistency, and failure layers
- new gaps:
  - no implemented canonical library taxonomy or authored-versus-deployment library program exists yet
  - no implemented library validation/freeze program exists yet
  - broader product decomposition for retrieval, API, UI, deployment, packaging, and production topology is still incomplete
  - neither track yet has enough bounded checkpoint structure to qualify as `ROADMAP_READY`
- roadmap-ready candidates:
  - none at this closeout point
- integration recommendation:
  - Track 1: keep design-only, continue shaping, and decide before `M11.1` whether it becomes later roadmap material, a new addendum, or a post-roadmap library program
  - Track 2: keep design-only, continue shaping, and record an explicit pre-`M11.1` integration decision rather than silently carrying it forward
- notes:
  - mandatory `M10.10` full repo pass completed
  - active addendum remains in force because the hard integration decision before `M11.1` is still pending

---

# Integration readiness criteria

A track is not `ROADMAP_READY` unless all of the following are true:

- the decomposition is coherent
- the track has clear scope boundaries
- the track has candidate checkpoint structure
- the track has clear relation to existing roadmap milestones
- the track no longer depends on vague future wording alone
- there is a clear recommendation for adoption path:
  - canonical roadmap
  - active addendum
  - post-roadmap separate phase
  - explicitly deferred with new decision gate

---

# Current disposition

Both tracks are acknowledged and actively governed, but neither is yet roadmap-ready.

Current disposition:

- Track 1 — `SHAPING`
- Track 2 — `SHAPING`

Normal checkpoint execution continues unchanged while this register matures under addendum governance.
