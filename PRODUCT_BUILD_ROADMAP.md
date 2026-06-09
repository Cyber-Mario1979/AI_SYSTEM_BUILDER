# ASBP Product Build Roadmap v1

Status: ACTIVE
Branch: product-rebuild-from-pre-pr23
Baseline: c17b7893c6e58b8bf3b3651a0232214eb2584956
Purpose: rebuild the project as a usable AI-applied product path after removing the productization/SaaS drift path.

## 1. Operating Rule

This roadmap controls execution.

This file is allowed as the one required roadmap-control artifact.

After this file is committed, no product milestone may close unless it ships at least one of:

- executable code
- tests
- runnable local behavior
- generated artifact
- user-facing product surface
- validated product scenario evidence

A document-only checkpoint cannot close a product milestone.

## 2. Product Target

Build a local AI-applied CQV product that lets the user:

1. create or select a Work Package
2. configure scope, system type, preset, and standards bundle
3. stage or generate task sets
4. create a plan with durations, dependencies, owners, and dates
5. amend the plan with before/after evidence
6. generate controlled document drafts and exports
7. discuss the Work Package with AI inside governed context
8. review, accept, reject, or revise candidate outputs
9. export usable artifacts
10. repeat the workflow without relying on long chat memory

## 3. Product Architecture Rule

The product must use three layers:

1. Deterministic service layer
   - owns state changes
   - owns IDs
   - owns validation
   - owns planning calculations
   - owns artifact records

2. AI assistance layer
   - reads governed context
   - suggests tasks, risks, document text, and review comments
   - never mutates state directly
   - every AI output is candidate-only until accepted

3. Local product surface
   - local app or browser UI
   - no raw internal CLI required for normal use
   - shows Work Packages, Planning, Outputs, and AI Review

## 4. Non-Negotiables

- No governance-only product milestone.
- No SaaS, license, commercial, or deployment work before local product use exists.
- No AI-owned state mutation.
- No hidden state writes.
- No broad readiness claims.
- No document generation claim unless a real artifact is generated.
- No UI claim unless a user can launch and use it locally.
- Every PR must say exactly what executable behavior changed.
- Every code PR must include tests.

## 5. Build Sequence

### P0 — Product Build Roadmap Lock

Goal:
Create this roadmap file.

Deliverable:
PRODUCT_BUILD_ROADMAP.md

Exit condition:
Roadmap committed on product-rebuild-from-pre-pr23.

Next step:
P1 must be executable code.

### P1 — Product Application Service Layer

Goal:
Create callable product operations independent of CLI parsing.

Files expected:
- asbp/product_app/__init__.py
- asbp/product_app/models.py
- asbp/product_app/service.py
- tests/test_product_app_service.py

Required service functions:
- list_work_packages
- get_work_package
- create_work_package
- select_work_package
- configure_work_package
- get_planning_view
- create_plan_amendment_candidate
- build_ai_context_packet

Exit condition:
Tests prove the service layer can create/configure/read product workflow state without CLI parsing.

No UI claim yet.

### P2 — Local Product App Shell

Goal:
Create a launchable local product surface.

Required screens:
- Dashboard
- Work Packages
- Planning
- Outputs
- AI Review

Exit condition:
User can launch the app locally and see product state.

### P3 — Work Package Workflow

Goal:
Create and configure Work Packages from the product surface.

Required behavior:
- create WP
- edit title/status
- set system type
- set preset
- set scope
- set standards bundle
- persist through approved service layer

Exit condition:
User can create and configure a WP without terminal commands.

### P4 — Planning Workflow

Goal:
Make planning usable from the product surface.

Required behavior:
- show tasks
- show durations
- show dependencies
- show owners
- generate baseline plan
- display planning result

Exit condition:
User can create or view a plan from the product surface.

### P5 — Plan Amendment Workflow

Goal:
Make plan changes controlled and visible.

Required behavior:
- amend duration
- amend owner
- amend dependency
- amend status
- show before/after
- preserve amendment record

Exit condition:
User can amend a plan and see impact before acceptance.

### P6 — Document Draft and Export

Goal:
Generate real controlled artifacts.

Required behavior:
- generate at least one document draft from WP state
- save artifact metadata
- mark human review required
- export/open artifact locally

Exit condition:
User can generate and open at least one real artifact.

### P7 — AI Review Panel

Goal:
Use AI inside product context without giving AI direct state control.

Required behavior:
- assemble AI context packet from selected WP
- ask AI for review or candidate suggestions
- show candidate output
- accept/reject candidate manually
- accepted changes must go through deterministic service layer

Exit condition:
User can discuss a WP with AI inside the product.

### P8 — End-to-End Product Trial

Goal:
Run the full local product loop.

Required flow:
- create WP
- configure WP
- stage/generate tasks
- plan
- amend plan
- generate artifact
- AI review
- human review
- export

Exit condition:
One full local product scenario runs successfully with evidence.

## 6. PR Rules

Every PR after P0 must include:

- code changed
- tests added or updated
- exact command to run tests
- exact behavior added
- what is still not claimed

A PR is rejected if it only adds governance, evidence, readiness language, or milestone closure without product behavior.

## 7. Current Next Step

Current step:
P0 — commit this roadmap.

Next executable step:
P1 — Product Application Service Layer.
