# UAT README

## Purpose of this folder

This folder contains milestone-level User Acceptance Testing (UAT) documents for the AI System Builder project.

UAT is not a substitute for automated validation. It is the milestone-facing acceptance layer after implementation and validation have reached a stable checkpoint.

## Folder pattern

Recent closed milestone UAT records are grouped by milestone:

```text
docs/UAT/M12/
docs/UAT/M13/
docs/UAT/M14/
docs/UAT/M15/
```

Each milestone folder may contain:

- `Mxx_UAT_PROTOCOL.md`
- `Mxx_UAT_REPORT.md`
- `README.md`

Older historical UAT records may still exist in the flat `docs/UAT/` folder or under `docs/UAT/evidence/` until a later historical cleanup wave.

## Intended sequence

1. Implementation reaches the approved milestone boundary.
2. Automated validation passes.
3. Milestone UAT is executed against milestone-facing behavior.
4. UAT result is recorded.
5. Milestone closeout is completed.

## Protocol vs report

The protocol defines what should be checked.

The report records what was accepted.

## Authority note

UAT evidence supports milestone acceptance. It does not replace the roadmap, tracker, architecture guardrails, code reality, or validation evidence.
