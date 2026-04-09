# POST_M5_UAT_DESIGN_PATCH_PROPOSAL

## Purpose

This document captures the design-direction patch proposed after Milestone 5 UAT closeout.

It is not intended to reopen Milestone 5.
It is also not intended to replace the broader project roadmap.

Its purpose is to make explicit a set of forward architectural and roadmap-level directions that became clear during and after Milestone 5 UAT review, so that Milestone 6 and later work proceed under the correct product model.

## Why this proposal exists

Milestone 5 closed successfully and the M5 UAT result is green.

However, the M5 closeout process surfaced several design-direction observations that should not remain implicit or buried:

- Work Package should increasingly be treated as the parent-facing canonical unit
- future workflow should become more structured than direct low-level task addition
- the planning layer should become explicit in forward roadmap/governance direction

This proposal expands those observations into a coherent forward model.

## Core design direction

The product should be treated as a deterministic CQV system with a Work Package-centered orchestration flow.

The high-level flow is:

1. create or load Work Package context
2. resolve deterministic bindings
3. stage task collection
4. commit task collection
5. generate and commit planning
6. export reports and CQV documentation

## Canonical parent unit

### Work Package is the parent-facing canonical unit

The Work Package should be treated as the main user-facing and system-facing parent object.

Tasks, collections, standards, calendars, planning artifacts, reports, and downstream documents should be understood as attached to or derived from Work Package context.

This does not invalidate current task-level surfaces.
It means that forward workflow and orchestration should increasingly center on Work Package-first behavior.

## Preset layer and entry direction

### Preset-first flow is the preferred deterministic entry path

The long-term system may support both:

- Load Preset
- Create Work Package manually

However, the preset-first path is the preferred deterministic primary flow.

Manual Work Package creation should be understood as a lower-automation variant of the same overall flow rather than a fully separate product path.

### Preset is not only a template

A preset should be treated as a deterministic binding seed.

A preset should not only instantiate Work Package context.
It should also resolve or attach downstream operational bindings needed for later flow stages.

## Deterministic selector inputs

### Selector inputs must include more than Work Package type alone

Task-pool selection should not be determined by equipment type alone.

The deterministic selector context should include at minimum:

- Work Package type
- complexity / automation profile
- scope / intent

These inputs should drive the selection of downstream bound assets.

## Scope / intent as a first-class selector dimension

### Scope / intent is a first-class selector input

In CQV, task determination depends not only on what the object is, but also on why the object is being touched.

Valid scopes / intents therefore belong inside deterministic selector logic.

Illustrative scope/intention examples include:

- end-to-end qualification lifecycle
- commissioning only
- qualification only
- periodic verification
- post-change qualification

This means that a task pool is not selected only from equipment class.
It is selected from a combined context that includes scope / intent.

## Binding layer

### Bound context should be treated as a real layer

Once Work Package context is known, the system should resolve a deterministic bound context.

The bound context should include:

- task pool
- calendar
- planning basis
- standards bundle

This should be treated as a distinct runtime layer rather than loose metadata.

## Standards layer

### Standards are part of binding, not only documentation metadata

Standards should be treated as part of runtime context binding.

The default and add-on model should be:

- CQV Core = default baseline bundle
- Cleanroom / HVAC bundle = add-on when relevant
- Automation bundle = add-on when relevant

Standards bundle selection should depend on the Work Package domain context, including type and automation profile.

This means standards influence not only final documentation, but also the deterministic operational context attached to the Work Package.

## Task collection model

### Task Collections should be interpreted broadly in Milestone 6 and beyond

Milestone 6 should not be understood as simple task grouping only.

The task collection model should support at least these conceptual states:

- source task pool
- staged task selection
- committed task selection
- iterative refinement after commitment when needed

This aligns the collection model with actual CQV workflow rather than treating collections as passive containers.

## Structured task workflow

### Low-level task addition is valid but should not be the primary forward workflow

The intended structured flow should increasingly move toward:

1. establish Work Package context
2. resolve deterministic bindings
3. stage tasks from the bound source
4. user refines task selection
5. commit task set to the Work Package
6. optionally iterate and refine again

This is a workflow/orchestration direction for future milestones.
It does not invalidate current task-add capability.

## Planning layer

### Planning must become an explicit forward layer

Planning should be treated as a first-class future layer.

It should appear after committed task selection and before export / reporting / documentation.

Planning should use:

- user-provided start date
- durations from planning basis
- dependencies from task pool / committed task set

The system should then generate a derived plan for review and later commitment.

### Planning is not optional decoration

Planning should not remain implicit or buried as a later convenience feature.
It is a major system layer in the end-to-end deterministic flow.

## Timestamp-aware system direction

### The system should be timestamp-aware by design

Because planning depends on time-based sequencing, the system should be treated as timestamp-aware by design.

This does not require full implementation immediately.
It means future roadmap/governance language should acknowledge time-aware planning as a first-class concern.

This affects future design around:

- start dates
- derived finish dates
- sequencing
- committed planning snapshots
- downstream reporting and auditability

## Export / reporting / documentation layer

### Export and CQV documentation remain downstream layers

After Work Package context, bindings, task commitment, and planning commitment are in place, the system should support downstream export/report/document generation.

This includes CQV-facing deliverables and should remain attached to Work Package-centered context.

## Relationship to the broader roadmap

### This design patch does not replace the normal roadmap

This proposal does not wipe out or replace the broader roadmap direction.

It does not cancel or reduce the project ambition toward:

- future AI layers
- future UI layers
- broader system integration layers
- production-grade SaaS direction

Instead, it clarifies foundational system direction so those later layers grow on top of a coherent deterministic base.

## Recommended roadmap-facing insertions

The following should be made explicit in forward roadmap/governance language:

1. Work Package is the canonical parent-facing unit
2. preset-first deterministic binding is a core future direction
3. selector inputs include type + complexity/automation profile + scope/intent
4. standards bundle binding is a real runtime layer
5. Task Collections cover source/staged/committed semantics
6. planning is an explicit future layer
7. the system is timestamp-aware by design
8. the broader AI/UI/SaaS roadmap remains intact

## Recommended immediate usage

This proposal should be used as input for:

- a small roadmap-direction patch
- possible guardrail wording updates
- clarification of how Milestone 6 should be interpreted before implementation advances

## Non-goal

This document is not itself an implementation plan.
It is a design-direction patch proposal intended to make the next implementation decisions more coherent.
