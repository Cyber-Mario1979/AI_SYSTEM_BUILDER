---
doc_type: canonical_roadmap
canonical_name: ROADMAP_CANONICAL
status: ACTIVE_AFTER_MERGE
governs_execution: true
document_state_mode: state_agnostic
authority: canonical_strategic_source_of_truth
version: v7
supersedes: ROADMAP_CANONICAL v6 Draft
source_change_control: ROADMAP_CANONICAL.md Section 2 — V7 change record
change_control_id: RCC-ROADMAP-003
repository: Cyber-Mario1979/AI_SYSTEM_BUILDER
source_branch: roadmap-v7-required-deliverable-control
approval_state: PROJECT_OWNER_REQUESTED_REPO_AMENDMENT
created_date: 2026-06-03
application_mode: branch_pr_review
live_repo_write: YES_BRANCH_PR
---

# AI Systems Builder Program (ASBP) — Canonical Roadmap v7

## 1. Purpose

Roadmap v7 is the forward execution roadmap for ASBP after the M31 closeout and M32.1 planning entry point.

The final ASBP goal is to finish a real local integrated CQV product before any deployment or hosted-path decision. The product must be usable locally, evidence-based, validated, accepted by the owner, and explicit about limitations.

Roadmap v7 is not a commercialization plan. Commercial launch work remains outside ASBP unless separately approved after completion.

Roadmap v7 does not reopen closed milestones by itself and does not implement code, UI, AI runtime behavior, retrieval, output generation, cleanup, tracker movement, release, or deployment by itself.

---

## 2. V7 change record

Roadmap v7 applies the current Project Owner agreement that remaining checkpoint deliverables must be explicit inside the roadmap.

The checkpoint table column is therefore:

```text
Required deliverable / completion minimum
```

This wording replaces the older `Completion minimum` wording for remaining active and future checkpoints.

### V7 anti-drift rule

For M32 onward:

- `Build/content` checkpoints require real implementation, source/content artifacts, adapters, workflow behavior, scenario packs, correction packages, packaging artifacts, or product documentation as stated in the checkpoint.
- `Hybrid` checkpoints require both the governance boundary and the implementation/source/contract/evidence part stated in the checkpoint.
- `Validation` checkpoints require truthful validation evidence.
- `UAT` checkpoints require real trial, observation, UAT, or owner acceptance evidence.
- `Closeout` checkpoints may close only after required prior evidence exists.
- Documentation alone cannot complete a `Build/content` or `Hybrid` checkpoint unless the roadmap explicitly records an approved deferral and the tracker states that the product/runtime behavior was not implemented.

Governance defines the boundary. Implementation proves progress. Validation proves truth. UAT proves acceptance.

---

## 3. Source-of-truth contract

`ROADMAP_CANONICAL.md` governs forward phase, milestone, and checkpoint order after merge into `main`.

Repo reality governs what actually exists: code, tests, package structure, commands, runtime behavior, source data, validation evidence, UAT evidence, and closeout evidence.

`PROGRESS_TRACKER.md` is the current-position pointer only. It does not override roadmap direction or repo truth.

`ARCHITECTURE_GUARDRAILS.md` and `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md` remain active governance sources.

If roadmap, tracker, DDR, architecture guardrails, or repo reality conflict, execution stops before PLAN or GO until the conflict is resolved.

---

## 4. Execution modes

| Execution mode | Meaning |
|---|---|
| `Governance-only` | Decision, scope lock, review, acceptance preparation, or planning artifact only. |
| `Build/content` | Code, source data, source library, validator, loader, output, retrieval, AI, UI, workflow, packaging, or product documentation content. |
| `Hybrid` | Governance boundary plus implementation/source/runtime/content evidence. |
| `Validation` | Validation evidence checkpoint. |
| `UAT` | User acceptance testing, owner acceptance, human observation, or trial acceptance. |
| `Closeout` | Milestone boundary freeze after required prior evidence exists. |

For Phase 9 and Phase 10 product-path work, wording such as define, scope, model, review, decide, assess, gate, framework, authority, or behavior must not be treated as governance-only by inference.

---

## 5. Validation policy

Code-affecting work requires:

```text
python -m pytest -q
```

Do not claim tests passed unless they were actually run and passed in the current environment.

Docs-only governance work does not require pytest unless it changes executable commands, imports, package behavior claims, runtime contracts, schemas, CLI behavior, validators, loaders, or executable behavior.

Milestone transition requires UAT or owner acceptance evidence appropriate to the milestone.

---

## 6. Phase summary

| Phase | Milestones | V7 treatment |
|---|---|---|
| Phase 1 — Foundations | M1-M2 | Historical foundation. |
| Phase 2 — Deterministic System Modeling | M3-M7 | Historical deterministic model. |
| Phase 3 — AI Runtime Architecture | M8-M10 | Historical runtime/output boundary foundation; not proof of live/product AI. |
| Phase 4 — Professionalization | M11 | Historical professionalization boundary. |
| Phase 5 — Core Engine Completion | M12-M15 | Historical core-engine/document/export/resolver/library framework. |
| Phase 6 — AI Layer | M16-M18 | Historical AI boundary/evaluation/advisory governance. |
| Phase 7 — UI and API Layer | M19-M21 | Historical external-surface governance; not full local usable UI. |
| Phase 8 — Cloud / Compute Layer | M22-M24 | Historical deployment/operation boundary planning; not deployment readiness. |
| Phase 9 — Full Local Integrated CQV Product Core | M25-M34 | Active product build path through local AI/UI/document/output convergence, trial, and product-core closeout. |
| Phase 10 — Engineering Product Readiness and Deployment-Readiness Evaluation | M35-M38 | Post-local-product engineering readiness path; not commercial launch. |

M1 through M24 remain closed for their original scope unless separately reopened by approved change control.

M25 through M31 remain interpreted by repo reality and closeout evidence. Governance/model/scaffold closure does not prove current executable product capability unless implementation and validation evidence prove it.

---

## 7. Phase 9 — Full Local Integrated CQV Product Core

### Phase goal

Build, validate, trial, and accept a complete real local integrated CQV product core with governed source libraries, standards authority, document/output behavior, retrieval where justified, bounded AI where accepted, and local workflow/UI surfaces sufficient for real local use.

---

### Milestones 25-31 status summary

| Milestone | Status | Required interpretation |
|---|---|---|
| M25 — Roadmap Reset and Control Recovery | Historical/completed | Redirected project toward local integrated CQV product path; does not prove product completion. |
| M26 — Product Source Authority Boundary | Historical/completed | Established source-authority boundaries; product behavior still depends on implementation and validation. |
| M27 — Runtime-Authoritative CQV Libraries and Mappings | Historical/completed | Established library/mapping evidence; downstream workflow must prove consumption and user-facing value. |
| M28 — Standards Applicability, Citation, and Runtime Consumption Authority | Historical/completed | Standards/citation authority is limited by verified evidence and source status. |
| M29 — Product-Ready Document Factory, Document Engine Workflow, and Output Rendering | Historical/completed | Product-ready output depends on repo implementation, validation, and UAT evidence. |
| M30 — Governed Retrieval and Indexing | Historical/completed | Retrieval is support-only and source-traceable; not source authority. |
| M31 — Governed AI Assistance, Runtime Shakedown, and Human Observation | Closed | Conditional local/offline AI draft-support baseline carried into M32 only if scoped, with human review required. |

M31 carry-forward limit: AI may be included in M32 only as bounded local/offline draft support unless later evidence expands it. Generated AI output remains human-review-required. Normal pytest must not require Ollama or a live model.

---

### Milestone 32 — Full Local Usable Product Workflow/UI

**Goal:** Build a real local workflow/UI path that lets a user operate ASBP locally without relying on raw internal CLI mechanics for normal product use.

Entry gate: M26-M31 product-core sources, output boundaries, retrieval boundaries, and AI limits must be available for the intended workflow. M31 AI is included only where M32.1 scopes it.

DDR focus: DDR-001, DDR-002, DDR-005, DDR-006, DDR-007, DDR-009 as applicable.

| Checkpoint | Execution mode | Purpose | Required deliverable / completion minimum | Validation / review requirement | Tracker movement rule | Not allowed |
|---|---|---|---|---|---|---|
| `M32.1` Full local workflow scope lock | `Governance-only` | Define local user journey and product functions. | Scope record defining local user journey, included/excluded functions, project creation/selection, preset/profile binding, task staging, planning, document/output flow, review gates, source selection, AI inclusion decision, limitations, and acceptance criteria. | Document consistency review. | May advance only after accepted M32.1 scope record exists. | Treating scope record as implemented UI/workflow; SaaS/admin/tenant scope. |
| `M32.2` Local UI/runtime surface decision | `Hybrid` | Select local operating surface. | Decision plus adapter boundary for selected surface: CLI-enhanced, local web, desktop-like, or controlled forms; include implementation/adapter impact where applicable. | Tests required if executable surface changes. | May advance only after selected surface and boundary are explicit. | Cloud-first bypass; treating decision as implemented UI. |
| `M32.3` UI-to-core adapter implementation | `Build/content` | Implement adapter layer without domain logic in UI. | Actual UI adapter contracts, routes, forms, or calls as applicable, using approved core/service boundaries. | `python -m pytest -q` if code changed. | May advance only after adapter behavior exists and validates where applicable. | UI writes raw state/files directly; document-only closure. |
| `M32.4` Controlled input surfaces | `Build/content` | Build controlled local input forms/surfaces. | Controlled DCF path, minimal input path, project/preset/profile/source selection, and standards/profile choices where in scope. | `python -m pytest -q` if code changed. | May advance only after controlled input behavior exists. | Unvalidated free-form input as truth; document-only closure. |
| `M32.5` Workflow visibility surfaces | `Build/content` | Show workflow state and limitations. | Visible WP/task/schedule/document lifecycle/source/citation/AI limitation state where in scope. | `python -m pytest -q` if code changed. | May advance only after visibility behavior is implemented or explicitly deferred. | Misleading readiness indicators; hidden limitations. |
| `M32.6` Output review/download surfaces | `Build/content` | Provide controlled output review and artifact access. | Document/export view, artifact metadata, validation limitations, review/acceptance status, and safe artifact access. | `python -m pytest -q` if code changed. | May advance only after output review/download behavior exists. | Silent output acceptance; document-only closure. |
| `M32.7` Local workflow error/failure handling | `Build/content` | Make failures visible and safe. | Visible and safe handling for missing input, invalid references, source limitations, validation errors, and provider/AI failures where in scope. | `python -m pytest -q` if code changed. | May advance only after failure behavior exists. | UI masks failures; false success state. |
| `M32.8` End-to-end local scenario implementation | `Build/content` | Run one approved local CQV workflow scenario through the local UI/workflow. | One approved local CQV workflow scenario that can actually be exercised through the local UI/workflow, with executable/local-use instructions and evidence. | `python -m pytest -q` if code changed; scenario evidence required. | May advance only after a local scenario can be exercised. | Calling it product-ready before trial; document-only closure. |
| `M32.9` Validation checkpoint | `Validation` | Validate local workflow/UI behavior. | Full tests plus scenario validation evidence for the local workflow/UI. | Validation evidence required. | May advance only after validation evidence exists. | Skip workflow testing; claim validation by memory. |
| `M32.10` Milestone UAT / owner acceptance | `UAT` | Accept local workflow as trial-ready. | Owner acceptance that the local workflow is trial-ready, with limitations recorded. | UAT/owner acceptance required. | May advance only after owner acceptance exists. | Treat as commercial readiness; treat conditional acceptance as full readiness. |
| `M32.11` Milestone closeout | `Closeout` | Freeze local workflow/UI MVP baseline. | Closeout record freezing local workflow/UI MVP baseline and identifying remaining trial blockers. | Document consistency review. | May advance only after closeout exists and evidence references are complete. | Proceed to trial with hidden gaps. |

M32 exit criteria: local product workflow is usable enough for real trial; UI/workflow remains a downstream adapter; source, standards, output, AI, and validation limitations are visible.

---

### Milestone 33 — Full Local Product Trial, Defect Loop, and UAT

**Goal:** Prove the local integrated CQV product works in realistic local use before engineering readiness or deployment-readiness work proceeds.

Entry gate: M32 local workflow/UI accepted as trial-ready; known DDR blockers are closed, carried with explicit limitations, or excluded from trial scope.

| Checkpoint | Execution mode | Purpose | Required deliverable / completion minimum | Validation / review requirement | Tracker movement rule | Not allowed |
|---|---|---|---|---|---|---|
| `M33.1` Trial scope and protocol | `Governance-only` | Define local trial boundaries. | Trial protocol with scenario(s), system type, user role, acceptance criteria, data sensitivity, limitations, and trial boundaries. | Document consistency review. | May advance only after protocol exists. | Trial without scope; treating protocol as trial execution. |
| `M33.2` Test dataset / scenario pack | `Build/content` | Prepare realistic local CQV scenario pack. | Realistic cleanroom/HVAC/equipment/computerized-system scenario data as approved, with confidentiality controls. | Source/data consistency review; tests if executable validators change. | May advance only after scenario pack exists. | Real confidential data without control; document-only closure. |
| `M33.3` Integrated validation suite | `Build/content` | Validate the integrated path. | Integrated validation covering source selection, staging, planning, standards, document factory, UI, retrieval, and AI/local model where included. | `python -m pytest -q` if code changed; integrated validation evidence. | May advance only after integrated validation exists. | Unit-only confidence for product trial. |
| `M33.4` Trial execution round 1 | `UAT` / `Hybrid` | Run realistic local workflow. | Real trial record capturing issues, errors, friction, wrong outputs, AI behavior where in scope, and user observations. | Real trial evidence required. | May advance only after trial evidence exists. | Ignore observed failures; use synthetic tests as trial. |
| `M33.5` Issue triage and correction plan | `Governance-only` | Classify findings. | Classified issue list with severity and disposition: bug, fix, refactor, doc, library, standards, UI, AI, or no action. | Review evidence required. | May advance only after triage exists. | Patch randomly outside roadmap. |
| `M33.6` Corrective implementation package | `Build/content` | Apply approved corrections. | Approved corrections applied to code, docs, source data, UI, AI, libraries, standards, or workflow as triaged. | `python -m pytest -q` if code changed. | May advance only after corrections and validation exist. | Scope creep beyond trial findings; document-only closure. |
| `M33.7` Regression and re-trial | `Validation` / `UAT` | Re-run affected paths. | Regression evidence and re-trial notes for corrected paths. | Validation and re-trial evidence required. | May advance only after affected paths are rechecked. | Close without re-check. |
| `M33.8` Local product UAT report | `UAT` | Produce UAT evidence. | UAT report with scope, results, limitations, acceptance decision, and owner/reviewer field. | UAT report required. | May advance only after UAT report exists. | Productization claim without UAT. |
| `M33.9` Final validation checkpoint | `Validation` | Final local product validation. | Full tests plus integrated scenario validation. | Validation evidence required. | May advance only after validation evidence exists. | Claim validation by memory. |
| `M33.10` Owner acceptance gate | `UAT` | Accept/reject local product core. | Pass, conditional pass, or fail decision with rationale and limitations. | Owner decision required. | May advance only after owner decision exists. | Treat conditional pass as full readiness. |
| `M33.11` Milestone closeout | `Closeout` | Freeze trial evidence. | Closeout record defining remaining gaps and next gate. | Document consistency review. | May advance only after closeout exists. | Re-enter readiness automatically. |

M33 exit criteria: integrated trial evidence, defect loop evidence, validation results, UAT/owner decision, and explicit limitations.

---

### Milestone 34 — Local Product-Core Closeout and Local Release-Candidate Gate

**Goal:** Decide whether the local integrated CQV product core is real, usable, validated, and acceptable as an enterprise-grade local product baseline.

Entry gate: M33 validation and UAT complete; full DDR register reviewed; product-core gaps resolved, accepted, or explicitly carried.

| Checkpoint | Execution mode | Purpose | Required deliverable / completion minimum | Validation / review requirement | Tracker movement rule | Not allowed |
|---|---|---|---|---|---|---|
| `M34.1` Product-core completeness assessment | `Governance-only` | Assess all local product categories. | Evidence-based assessment covering libraries, standards, document/output, retrieval, AI, UI, validation, UAT, install/run needs, and limitations. | Document consistency review. | May advance only after assessment exists. | Assume readiness from one scenario only. |
| `M34.2` DDR closure/reclassification review | `Governance-only` | Review all DDR statuses. | Close, reclassify, or carry-forward decisions for DDRs, with evidence. | DDR consistency review. | May advance only after DDR review exists. | Close dependencies without evidence. |
| `M34.3` Product-core limitation register | `Governance-only` | Record known limits. | Register of supported scopes, unsupported scopes, source limits, standards limits, AI limits, UI limits, and output limits. | Document consistency review. | May advance only after limitation register exists. | Hide limitations. |
| `M34.4` Local release-candidate boundary decision | `Governance-only` | Decide local RC boundary. | In/out boundary for the first local enterprise-grade product baseline. | Owner review required. | May advance only after local RC boundary is explicit. | Expand to deployment/SaaS prematurely. |
| `M34.5` Engineering readiness entry decision | `Governance-only` | Decide if Phase 10 may begin. | Evidence-based pass, conditional pass, or fail decision for entering Phase 10. | Owner decision required. | May advance only after decision exists. | Resume readiness automatically. |
| `M34.6` Validation checkpoint | `Validation` | Validate any final changes. | Validation evidence for any final changes; pytest if code changed. | Validation evidence required where applicable. | May advance only after validation evidence exists. | Claim closure without validation. |
| `M34.7` Product-core UAT/owner acceptance | `UAT` | Accept product-core closeout. | Owner decision with rationale. | Owner acceptance required. | May advance only after acceptance exists. | Treat as launch approval. |
| `M34.8` Phase 9 closeout | `Closeout` | Freeze local product-core path. | Phase 9 closeout record pointing to Phase 10 only if approved. | Document consistency review. | May advance only after closeout exists. | Skip re-entry gate. |

M34 exit criteria: product-core completeness decision, DDR alignment, limitation register, owner acceptance/rejection, and explicit Phase 10 entry decision.

---

## 8. Phase 10 — Engineering Product Readiness and Deployment-Readiness Evaluation

### Phase goal

Prepare the accepted local product for engineering product-readiness decisions, packaging, release governance, deployment-readiness evaluation, and optional future cloud/web/SaaS technical boundary decisions.

Phase 10 begins only if M34 approves entry.

---

### Milestone 35 — Product Boundary, License, Repository, and Engineering Release Direction

**Goal:** Decide what ASBP is as an engineering product artifact and what release/distribution boundary is allowed.

| Checkpoint | Execution mode | Purpose | Required deliverable / completion minimum | Validation / review requirement | Tracker movement rule | Not allowed |
|---|---|---|---|---|---|---|
| `M35.1` Product identity and boundary assessment | `Governance-only` | Define product vs build project. | Product name, audience/use context, supported scope, excluded scope, and enterprise-grade quality target. | Owner review required. | May advance only after boundary assessment exists. | Commercial launch claim. |
| `M35.2` License strategy assessment | `Governance-only` | Decide license path or legal-review need. | GPLv3 continuation, dual license, proprietary future repo, open-core, or legal review need. | Owner/legal review decision where applicable. | May advance only after license path is explicit. | Legal/license change without approval. |
| `M35.3` Repository visibility / split decision | `Governance-only` | Decide repo structure. | Public/private split, future product repo, archive/public docs, or no split. | Owner decision required. | May advance only after repo decision exists. | Make repo private silently. |
| `M35.4` Distribution and deployment posture decision | `Governance-only` | Decide allowed technical posture. | Local-only package, private/internal deployment option, hosted website technical path, cloud-hosted technical path, or SaaS technical feasibility path. | Owner decision required. | May advance only after posture decision exists. | Pricing, sales, or marketing planning. |
| `M35.5` Supportability boundary | `Governance-only` | Define support obligations. | Bug/security/support channels, no-SLA/SLA decision boundary, and lifecycle policy. | Owner review required. | May advance only after supportability boundary exists. | Promise unsupported obligations. |
| `M35.6` Validation checkpoint | `Validation` | Validate docs/code consistency. | Docs/code consistency evidence; pytest only if executable claims or code changed. | Validation or consistency evidence required. | May advance only after validation/review evidence exists. | Claim code validation if not run. |
| `M35.7` Owner acceptance | `UAT` | Approve engineering product boundary. | Owner decision approving the engineering product boundary. | Owner acceptance required. | May advance only after acceptance exists. | Begin packaging without boundary. |
| `M35.8` Milestone closeout | `Closeout` | Freeze product boundary. | Closeout record pointing to M36 if approved. | Document consistency review. | May advance only after closeout exists. | Skip license/support/security decisions. |

---

### Milestone 36 — Packaging, Installability, Release Governance, Security, and Supportability

**Goal:** Make the accepted local product governable as an enterprise-grade release-candidate artifact.

| Checkpoint | Execution mode | Purpose | Required deliverable / completion minimum | Validation / review requirement | Tracker movement rule | Not allowed |
|---|---|---|---|---|---|---|
| `M36.1` Packaging strategy | `Hybrid` | Define and implement package/build path where approved. | Packaging/install plan plus implementation where in scope. | `python -m pytest -q` if code changed; install test if package behavior changed. | May advance only after packaging path exists or is explicitly deferred. | Production package without tests. |
| `M36.2` Local install/run guide | `Build/content` | Document and verify local use. | Verified local install/run guide for the supported local mode. | Command verification evidence required. | May advance only after guide and verification exist. | Undocumented local operation. |
| `M36.3` Release artifact policy | `Governance-only` | Define release artifacts. | Version tags, artifact metadata, release notes, and checksums if needed. | Document consistency review. | May advance only after policy exists. | Ad hoc release files. |
| `M36.4` Security policy | `Governance-only` | Define vulnerability/security reporting and scope. | `SECURITY.md` or equivalent vulnerability/security reporting policy where approved. | Owner review required. | May advance only after policy exists. | Claim enterprise security posture without evidence. |
| `M36.5` Supportability policy | `Governance-only` | Define support/maintenance boundary. | Issue templates, support boundary, and lifecycle policy. | Owner review required. | May advance only after policy exists. | SLA without approval. |
| `M36.6` Product documentation package | `Build/content` | Build user-facing docs. | User-facing docs: install/use guide, limitations, supported scopes, and troubleshooting. | Documentation review and command validation where applicable. | May advance only after docs package exists. | Replace governance docs with marketing. |
| `M36.7` Release validation package | `Validation` | Validate packaged product. | Install test, command test, artifact checks, and pytest where code changed. | Validation evidence required. | May advance only after validation evidence exists. | Release without validation. |
| `M36.8` UAT / owner acceptance | `UAT` | Accept packaging/release governance. | Owner signoff with limitations. | Owner acceptance required. | May advance only after acceptance exists. | Commercial launch. |
| `M36.9` Milestone closeout | `Closeout` | Freeze release-candidate governance. | Record remaining release blockers. | Document consistency review. | May advance only after closeout exists. | Skip operational shakedown. |

---

### Milestone 37 — Operational Shakedown and Deployment-Path Technical Gate

**Goal:** Decide whether any local/private/cloud/website/SaaS technical deployment path is safe to pursue after packaging and release governance evidence exists.

| Checkpoint | Execution mode | Purpose | Required deliverable / completion minimum | Validation / review requirement | Tracker movement rule | Not allowed |
|---|---|---|---|---|---|---|
| `M37.1` Operational scope lock | `Governance-only` | Decide technical operational scope. | Scope, environment, users, data sensitivity, and deployment assumptions. | Owner review required. | May advance only after operational scope exists. | Production deployment by default. |
| `M37.2` Provider integration gate | `Hybrid` | Revisit DDR-007 if provider/runtime path is included. | Provider boundary, smoke tests, cost/privacy/risk controls, and validation evidence if provider/runtime path is included. | `python -m pytest -q` if code changed; smoke evidence where applicable. | May advance only after approved adapter/test plan and evidence exist. | Live calls without approved adapter/test plan. |
| `M37.3` Deployment environment gate | `Governance-only` / `Hybrid` | Decide environment path. | Environment decision: local package, internal server, owned website, cloud staging, or SaaS later as technical options; include tests if deployment code/config changes. | Review required; tests if deployment code/config changes. | May advance only after environment decision exists. | Tenant behavior without SaaS gate. |
| `M37.4` Monitoring and failure handling | `Hybrid` | Define operational controls. | Logs, health checks, failure escalation, rollback, and issue capture. | Tests if executable behavior changes. | May advance only after operational controls exist. | Silent failure. |
| `M37.5` Operational shakedown | `UAT` / `Hybrid` | Execute repeated realistic use. | Repeated realistic use, issue capture, performance/friction notes, and AI/provider behavior where in scope. | Shakedown evidence required. | May advance only after shakedown evidence exists. | Go-live after single happy path. |
| `M37.6` Corrective action loop | `Build/content` | Fix shakedown issues. | Prioritized fixes from shakedown, with validation. | `python -m pytest -q` if code changed. | May advance only after corrections and validation exist. | Hide unresolved issues. |
| `M37.7` Go/no-go evidence pack | `Governance-only` | Produce readiness evidence. | Evidence pack with validation, UAT, issue status, limitations, and decision options. | Owner review required. | May advance only after evidence pack exists. | Launch without go/no-go. |
| `M37.8` UAT / owner acceptance | `UAT` | Accept operational readiness result. | Pass, conditional, or fail operational readiness decision with rationale. | Owner acceptance required. | May advance only after acceptance exists. | Treat conditional pass as SaaS-ready. |
| `M37.9` Milestone closeout | `Closeout` | Freeze operational gate. | Closeout decision on whether M38 may begin. | Document consistency review. | May advance only after closeout exists. | Skip unresolved DDR-007. |

---

### Milestone 38 — Cloud/Web/SaaS Technical Boundary Consolidation

**Goal:** Consolidate cloud, hosted website, or SaaS technical boundaries only after local product, packaging, release governance, and operational readiness gates are satisfied.

M38 is still not commercial launch planning.

| Checkpoint | Execution mode | Purpose | Required deliverable / completion minimum | Validation / review requirement | Tracker movement rule | Not allowed |
|---|---|---|---|---|---|---|
| `M38.1` Cloud/web/SaaS suitability reassessment | `Governance-only` | Decide if any hosted path remains valid. | Product fit, data/privacy, tenant need, cost/risk, and support assumptions. | Owner review required. | May advance only after reassessment exists. | SaaS because it sounds commercial. |
| `M38.2` Tenant/customer boundary plan if SaaS is approved | `Governance-only` | Define tenant/customer assumptions. | Tenant model, data separation, access assumptions, and unsupported states. | Owner review required. | May advance only after boundary exists if SaaS remains in scope. | Tenant implementation without approval. |
| `M38.3` Compliance and audit boundary | `Governance-only` | Define compliance limits. | Validation package, audit trail needs, and standards limitations. | Review required. | May advance only after compliance limits exist. | Regulated claims without evidence. |
| `M38.4` Deployment/release posture gate | `Governance-only` | Decide release posture. | Release candidate, pilot, private beta, public technical release, pause, or no-go decision. | Owner decision required. | May advance only after posture decision exists. | Full launch by default. |
| `M38.5` Final validation and regression | `Validation` | Validate release boundary. | Full tests, scenario checks, and documentation checks. | Validation evidence required. | May advance only after validation evidence exists. | Release without regression. |
| `M38.6` Final UAT / owner acceptance | `UAT` | Owner acceptance. | Final pass, conditional, or fail owner acceptance. | Owner acceptance required. | May advance only after acceptance exists. | Skip owner signoff. |
| `M38.7` Phase 10 closeout | `Closeout` | Close or pause engineering readiness path. | Record next strategic path and separate post-ASBP business/commercial decision. | Document consistency review. | May advance only after closeout exists. | Hide remaining gaps. |

---

## 9. DDR placement matrix

| DDR | V7 placement | Required interpretation |
|---|---|---|
| DDR-001 Governed-library runtime promotion / deployment-compiled lookup | M26, M27, M32-M34 | Governance/model evidence does not equal executable runtime-authoritative product library behavior in the local workflow. |
| DDR-002 Consolidated runtime-authoritative libraries | M26, M27, M32-M34 | Product library package/layout must be implemented, consumed, validated, and trialed before local product acceptance. |
| DDR-003 Product-ready document templates library | M29, M32-M34 | Product-ready output requires document factory workflow, rendering/generation behavior, validation, and local trial evidence. |
| DDR-004 Standards source registry and citation authority | M28, M32-M34 | Standards authority remains limited by verified source status and citation/applicability evidence. |
| DDR-005 Standards embedding / retrieval index | M30, M31, M33-M34 | Retrieval remains support-only unless future evidence explicitly closes remaining scope. |
| DDR-006 Product-ready document/export/report generation/rendering | M29, M31, M32-M34 | Generated output readiness requires review/acceptance controls, validation, UAT, and limitation visibility. |
| DDR-007 Model/provider integration and pre-go-live operational testing | M31, M33, M37 | Live provider/product AI and local app-coupled AI runtime require strategy, boundary, smoke, shakedown, validation, human observation, and acceptance evidence. |
| DDR-008 Phase 8/9 readiness gate | M25, M34 | Historical gate-control closure only; not product readiness. |
| DDR-009 External contract placeholders | M27, M32, M37-M38 | API/external placeholders do not authorize productized placeholder-backed behavior. |

---

## 10. Parallel support lane — non-code repository cleanup

The cleanup lane remains:

```text
Comprehensive non-code repository document cleanup
```

Cleanup is a parallel support lane only. It is not code cleanup, not tests cleanup, not implementation refactor, not roadmap rewriting by stealth, and not M32 checkpoint progress.

Cleanup may support M32 and later work by reducing ambiguity, but it must not replace product workflow/UI implementation, validation, UAT, or trial evidence.

Cleanup requires fresh repo inventory, protected active-file list, archive/keep/promote/move decisions, reference-impact scan before moves, owner approval before destructive or large-scale moves, and repo-index regeneration after approved cleanup.

No cleanup is performed by Roadmap v7 itself.

---

## 11. First active checkpoint after v7 application

After Roadmap v7 is merged/applied, the expected active checkpoint remains:

```text
PLAN M32.1 — Full local workflow scope lock
```

This is PLAN only, not GO.

M32.1 must produce the accepted scope record described in its `Required deliverable / completion minimum` cell before tracker movement from M32.1.

Roadmap v7 approval does not start M32.1 GO and does not implement M32 workflow/UI.

---

## 12. Final v7 direction statement

The next strategic path is:

1. complete `PLAN M32.1` as a real local workflow scope lock;
2. build the full local usable product workflow/UI through M32 build/content checkpoints;
3. run a realistic full local product trial with defect capture, correction, regression, re-trial, and owner acceptance in M33;
4. close the local product core only after evidence proves it is real, usable, validated, and accepted as an enterprise-grade local product baseline in M34;
5. proceed to engineering product-readiness only after local product-core closeout approves entry;
6. prepare packaging, installability, security/supportability, release governance, and deployment-readiness evaluation in M35-M37;
7. evaluate cloud, owned-website, or SaaS technical boundaries only after local product and engineering readiness evidence exist;
8. keep business/commercial launch work outside ASBP unless a separate post-completion decision approves a separate project or track.

Roadmap v7 exists to make the remaining ASBP path build-forward, evidence-based, and resistant to governance-only drift.
