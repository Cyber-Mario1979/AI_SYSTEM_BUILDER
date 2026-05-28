from pathlib import Path

TARGET = Path("docs/governance/control_recovery/CONTROL_RECOVERY_001_ROADMAP_GOVERNANCE_OPERATION_PACK_REPAIR.md")

SECTION = """## 4A. Owner Decision Record — Temporary Recovery Write Authority Request

Owner decision date:

    2026-05-28

Decision summary:

    The Project Owner requested that the normal repository write-lock rule be suspended for CONTROL-RECOVERY-001 activities only, so recovery amendments can be written directly during the recovery lane and the owner may decline tool actions through the user interface when needed.

Current authority status:

    REQUESTED / TO BE IMPLEMENTED THROUGH GOVERNANCE AMENDMENT

This decision is recorded as owner intent for the recovery lane. It does not by itself complete the operation-pack amendment, build/governance policy amendment, or final recovery verification required by this plan.

Temporary recovery-write scope requested by the Project Owner:

- recovery-plan amendments;
- roadmap anti-drift amendments;
- build/governance balance policy hard-stop amendments;
- progress tracker pause/recovery-state amendments;
- M27 retrospective evidence and evidence-hygiene corrections;
- M28 restart-control evidence;
- operation-pack replacement artifacts or instructions derived from this recovery plan;
- recovery verification evidence.

Explicit exclusions:

- no normal M28.2 implementation;
- no tracker advancement to M28.3;
- no normal roadmap checkpoint closure;
- no product/runtime/code implementation outside the recovery plan;
- no PR merge;
- no branch deletion;
- no issue closure;
- no release, productization, deployment, or SaaS action;
- no operation outside CONTROL-RECOVERY-001 scope.

Expiry condition:

    This requested temporary authority expires automatically when CONTROL-RECOVERY-001 is fully implemented, verified, and owner-approved for normal roadmap resumption.

Revocation condition:

    The Project Owner may revoke this requested temporary authority at any point.

Permanent-rule requirement:

    The operation pack and repo-side governance must still be amended so future assistant behavior does not depend on memory or informal chat agreement.

"""

def main() -> None:
    if not TARGET.exists():
        raise FileNotFoundError(f"Target file not found: {TARGET}")

    text = TARGET.read_text(encoding="utf-8")

    if "## 4A. Owner Decision Record — Temporary Recovery Write Authority Request" in text:
        print("No change: owner decision section already exists.")
        return

    marker = "## 5. Objective\n"
    if marker not in text:
        raise ValueError("Could not find insertion marker: ## 5. Objective")

    updated = text.replace(marker, SECTION + "\n" + marker, 1)
    TARGET.write_text(updated, encoding="utf-8")

    print("Applied CONTROL-RECOVERY-001 owner decision record.")
    print(f"Updated file: {TARGET}")
    print("Review with:")
    print(f"git diff -- {TARGET}")

if __name__ == "__main__":
    main()
