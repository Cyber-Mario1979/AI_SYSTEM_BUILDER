#!/usr/bin/env python3
"""User-applied M21.7 UAT evidence package.

This script writes the minimal Phase 7 UAT protocol/report for M21.
It does not edit code, run validation, commit, push, or create a PR.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


EXPECTED_BRANCH = "feature/m21-external-surface-governance"


FILES = {
    "docs/UAT/M21/M21_UAT_PROTOCOL.md": '# M21.7 — Phase 7 UAT Protocol\n\n## Purpose\n\nThis protocol defines the minimal UAT coverage for Phase 7 external-surface governance under Milestone 21.\n\nThe UAT confirms that the external API/UI surfaces introduced and governed across `M21.1` through `M21.6` are understandable, bounded, safe, and downstream from stable inner layers.\n\n## UAT scope\n\nThe UAT scope covers:\n\n- `M21.1` — Shared external contract discipline\n- `M21.2` — UI/API consistency rules\n- `M21.3` — Product-surface governance foundation\n- `M21.4` — External-surface boundary consolidation\n- `M21.5` — Validation and acceptance discipline for external surfaces\n- `M21.6` — Phase 7 validation checkpoint\n\nThe UAT also considers the completed upstream Phase 7 boundaries:\n\n- `M19` — API Boundary Introduction\n- `M20` — UI Layer Introduction\n\n## Evidence sources\n\nThe following evidence sources are in scope for review:\n\n- `docs/milestones/M21/M21_1_SHARED_EXTERNAL_CONTRACT_DISCIPLINE.md`\n- `docs/milestones/M21/M21_2_UI_API_CONSISTENCY_RULES.md`\n- `docs/milestones/M21/M21_3_PRODUCT_SURFACE_GOVERNANCE_FOUNDATION.md`\n- `docs/milestones/M21/M21_4_EXTERNAL_SURFACE_BOUNDARY_CONSOLIDATION.md`\n- `docs/milestones/M21/M21_5_VALIDATION_AND_ACCEPTANCE_DISCIPLINE.md`\n- `docs/milestones/M21/M21_6_PHASE_7_VALIDATION_CHECKPOINT.md`\n- `asbp/external_surface/contracts.py`\n- `asbp/external_surface/consistency.py`\n- `asbp/external_surface/governance.py`\n- `asbp/external_surface/boundary.py`\n- `asbp/external_surface/acceptance.py`\n- `tests/test_external_surface_contracts.py`\n- `tests/test_external_surface_consistency.py`\n- `tests/test_external_surface_governance.py`\n- `tests/test_external_surface_boundary.py`\n- `tests/test_external_surface_acceptance.py`\n- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`\n\n## UAT objectives\n\n| ID | Objective | Expected result |\n|---|---|---|\n| UAT-M21-001 | Confirm the external-surface role is understandable. | API/UI external surfaces are described as downstream adapter/product surfaces, not inner-layer authority. |\n| UAT-M21-002 | Confirm external contract discipline is bounded. | Shared external contract vocabulary is deterministic and does not create routes, screens, deployment, or productization behavior. |\n| UAT-M21-003 | Confirm UI/API consistency is understandable. | UI-visible state remains aligned with API response outcomes and governed engine truth. |\n| UAT-M21-004 | Confirm product-surface governance is safe. | Public/consumer-facing, visibility, command/intake, and error/status surfaces remain bounded and non-authoritative. |\n| UAT-M21-005 | Confirm command/intake discipline is bounded. | Command/intake behavior requires API/service validation before mutation and does not execute domain actions directly. |\n| UAT-M21-006 | Confirm boundary consolidation is coherent. | External-surface boundary evidence consolidates M21.1 through M21.3 without behavior expansion. |\n| UAT-M21-007 | Confirm validation and acceptance discipline is ready. | Required validation/UAT evidence expectations are explicit before Phase 7 closeout. |\n| UAT-M21-008 | Confirm no Phase 8/productization leakage. | M21 does not introduce cloud/deployment, SaaS, model/provider integration, standards embedding, or product-ready document/report/export generation. |\n| UAT-M21-009 | Confirm deferred dependencies remain visible. | Open/deferred/watch DDR items remain carried forward and are not closed by M21 UAT. |\n\n## Acceptance criteria\n\nM21 UAT may pass only if:\n\n- external API/UI surfaces are understandable as bounded downstream surfaces\n- shared external contract behavior is deterministic\n- UI/API visible state cannot diverge from governed engine truth\n- product-surface governance rejects hidden authority, hidden domain logic, uncontrolled agentic behavior, cloud/deployment, tenant/SaaS, and commercial productization behavior\n- boundary consolidation does not expand behavior\n- M21.6 validation evidence exists and records a passing validation result\n- UAT evidence records an acceptance decision and rationale\n- no deferred dependency is incorrectly closed\n- no Phase 8, cloud/deployment, SaaS, or productization assumption is introduced\n\n## Out of scope\n\nThis UAT does not cover:\n\n- live API routes\n- endpoint handlers\n- UI screens\n- UI framework behavior\n- production deployment\n- cloud/compute behavior\n- SaaS/productization behavior\n- tenant behavior\n- live model/provider integration\n- standards embedding\n- standards-backed citation output\n- document/report/export generation\n- approval or release authority\n- raw state mutation\n- direct persistence access\n\n## Execution method\n\nThe UAT is document-and-evidence based.\n\nThe operator reviews the scoped evidence and records the acceptance decision in:\n\n`docs/UAT/M21/M21_UAT_REPORT.md`\n\n## Closeout dependency\n\nM21.8 Phase 7 closeout must not proceed until the M21 UAT report exists and records an acceptance decision.\n',
    "docs/UAT/M21/M21_UAT_REPORT.md": '# M21.7 — Phase 7 UAT Report\n\n## Milestone\n\nMilestone 21 — UI/API Consolidation and Product-Surface Governance\n\n## UAT checkpoint\n\n`M21.7` — Phase 7 UAT checkpoint\n\n## UAT status\n\nCompleted\n\n## Acceptance decision\n\nPass\n\n## Scope reviewed\n\nThis UAT reviewed the Phase 7 external-surface governance work completed across:\n\n- `M21.1` — Shared external contract discipline\n- `M21.2` — UI/API consistency rules\n- `M21.3` — Product-surface governance foundation\n- `M21.4` — External-surface boundary consolidation\n- `M21.5` — Validation and acceptance discipline for external surfaces\n- `M21.6` — Phase 7 validation checkpoint\n\nThe UAT also considered the completed upstream API/UI boundaries from:\n\n- `M19` — API Boundary Introduction\n- `M20` — UI Layer Introduction\n\n## Evidence reviewed\n\nThe following evidence was reviewed:\n\n- `docs/milestones/M21/M21_1_SHARED_EXTERNAL_CONTRACT_DISCIPLINE.md`\n- `docs/milestones/M21/M21_2_UI_API_CONSISTENCY_RULES.md`\n- `docs/milestones/M21/M21_3_PRODUCT_SURFACE_GOVERNANCE_FOUNDATION.md`\n- `docs/milestones/M21/M21_4_EXTERNAL_SURFACE_BOUNDARY_CONSOLIDATION.md`\n- `docs/milestones/M21/M21_5_VALIDATION_AND_ACCEPTANCE_DISCIPLINE.md`\n- `docs/milestones/M21/M21_6_PHASE_7_VALIDATION_CHECKPOINT.md`\n- `asbp/external_surface/contracts.py`\n- `asbp/external_surface/consistency.py`\n- `asbp/external_surface/governance.py`\n- `asbp/external_surface/boundary.py`\n- `asbp/external_surface/acceptance.py`\n- `tests/test_external_surface_contracts.py`\n- `tests/test_external_surface_consistency.py`\n- `tests/test_external_surface_governance.py`\n- `tests/test_external_surface_boundary.py`\n- `tests/test_external_surface_acceptance.py`\n- `docs/governance/DEFERRED_DEPENDENCIES_REGISTER.md`\n\n## Supporting validation\n\nThe supporting validation checkpoint is:\n\n`docs/milestones/M21/M21_6_PHASE_7_VALIDATION_CHECKPOINT.md`\n\nRecorded validation result:\n\n`python -m pytest -q` — `1072 passed in 43.20s`\n\nValidation decision:\n\nPass\n\n## UAT results\n\n| ID | Objective | Result | Rationale |\n|---|---|---|---|\n| UAT-M21-001 | Confirm the external-surface role is understandable. | Pass | External surfaces are presented as downstream adapter/product surfaces and are not source truth, validation truth, execution truth, or domain logic. |\n| UAT-M21-002 | Confirm external contract discipline is bounded. | Pass | Shared contract vocabulary is deterministic and does not introduce routes, screens, deployment, SaaS, or productization behavior. |\n| UAT-M21-003 | Confirm UI/API consistency is understandable. | Pass | UI-visible state is constrained to remain aligned with API response outcomes and governed engine truth. |\n| UAT-M21-004 | Confirm product-surface governance is safe. | Pass | Product-surface governance rejects hidden authority, hidden domain logic, service-boundary bypass, cloud/deployment, tenant/SaaS, commercial productization, production endpoint/screen behavior, and uncontrolled agentic behavior. |\n| UAT-M21-005 | Confirm command/intake discipline is bounded. | Pass | Command/intake behavior requires API/service validation before mutation and does not execute domain actions directly. |\n| UAT-M21-006 | Confirm boundary consolidation is coherent. | Pass | Boundary consolidation reduces duplication and aligns external-surface failure behavior without expanding behavior. |\n| UAT-M21-007 | Confirm validation and acceptance discipline is ready. | Pass | Required validation and UAT evidence expectations are explicit before Phase 7 closeout. |\n| UAT-M21-008 | Confirm no Phase 8/productization leakage. | Pass | No cloud/deployment, SaaS, productization, model/provider integration, standards embedding, or product-ready document/report/export generation behavior is introduced. |\n| UAT-M21-009 | Confirm deferred dependencies remain visible. | Pass | Deferred dependencies remain carried forward and no dependency is incorrectly closed by this UAT. |\n\n## Operator-facing confirmation\n\nThe Phase 7 external surfaces are considered:\n\n- understandable\n- bounded\n- safe\n- downstream from stable inner layers\n- non-authoritative over source truth\n- non-authoritative over validation truth\n- non-authoritative over execution truth\n- free from hidden UI/API domain logic\n- free from productization, cloud/deployment, SaaS, standards embedding, document generation, and model/provider behavior\n\n## DDR review summary\n\nThe deferred dependency register remains active and was reviewed for this UAT checkpoint.\n\nNo deferred dependency is closed by `M21.7`.\n\nDDR-001 through DDR-006 remain deferred/open as applicable for future governed-library, template, standards, document-generation, and product-ready output concerns.\n\nDDR-007 remains watch status for future actual model/provider integration and pre-go-live operational testing.\n\nDDR-008 remains a future Phase 8 / Phase 9 productization-readiness gate. M21.7 does not begin Phase 8 or Phase 9.\n\nDDR-009 remains planning-awareness only for M21 external contracts. M21.7 does not close DDR-009 and does not implement libraries, templates, standards citation authority, standards embedding, or product-ready output generation.\n\n## Explicit non-goals\n\nThis UAT does not approve or introduce:\n\n- new UI/API features\n- Phase 8 work\n- Phase 9 work\n- cloud/deployment behavior\n- SaaS/productization behavior\n- API routes or endpoints\n- UI screens or UI framework behavior\n- command execution\n- document generation\n- report generation\n- export generation\n- standards embedding\n- standards-backed citation output\n- model/provider integration\n- raw state mutation\n- direct persistence access\n\n## Open UAT blockers\n\nNone.\n\n## Acceptance rationale\n\nThe M21 external-surface governance work is accepted because it establishes bounded external API/UI contract discipline, consistency rules, product-surface governance, boundary consolidation, and validation/UAT acceptance discipline while preserving stable inner-layer authority boundaries and avoiding productization leakage.\n\nThe supporting validation checkpoint passed, and the scoped UAT objectives are satisfied.\n\n## Closeout readiness\n\nM21.7 is complete.\n\nThe next roadmap-authorized checkpoint is:\n\n`M21.8` — Phase 7 closeout\n\n## Sign-off\n\n- Operator sign-off: `Amr Hassan`\n- Reviewer sign-off: `N/A`\n',
}


def repo_root() -> Path:
    return Path.cwd()


def current_branch() -> str | None:
    completed = subprocess.run(
        ["git", "branch", "--show-current"],
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content.rstrip() + "\n")


def main() -> int:
    branch = current_branch()
    if branch != EXPECTED_BRANCH:
        print(
            f"ERROR: expected branch {EXPECTED_BRANCH!r}, "
            f"but current branch is {branch!r}.",
            file=sys.stderr,
        )
        print("Switch branches first, then rerun this script.", file=sys.stderr)
        return 1

    root = repo_root()
    for relative_path, content in FILES.items():
        target = root / relative_path
        write_text(target, content)
        print(f"wrote {relative_path}")

    print("M21.7 UAT evidence files created.")
    print("Review docs/UAT/M21/M21_UAT_PROTOCOL.md and docs/UAT/M21/M21_UAT_REPORT.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
