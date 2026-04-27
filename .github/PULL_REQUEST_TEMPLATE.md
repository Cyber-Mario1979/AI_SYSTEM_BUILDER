# Pull Request

## Summary

Describe what this pull request changes.

## Change type

Choose one:

- [ ] Code behavior
- [ ] Tests only
- [ ] Documentation/public surface only
- [ ] Roadmap/tracker/governance
- [ ] Architecture/guardrail
- [ ] Refactor with no intended behavior change

## Scope boundary

Explain why this PR belongs in the selected scope.

For public-surface-only changes, confirm that this PR does not change runtime behavior, roadmap order, validation policy, architecture boundaries, or source-of-truth rules.

## Roadmap / tracker alignment

State the related checkpoint, milestone, or public-surface package.

If not applicable, write `N/A`.

## Behavior impact

Does this change runtime or CLI behavior?

- [ ] No
- [ ] Yes

If yes, describe the behavior change.

## Validation

Paste the validation run or explain why it is not required.

```powershell
python -m pytest -q
```

## Documentation impact

List updated documentation files.

## Checklist

- [ ] The change is narrow and reviewable.
- [ ] The change does not mix unrelated work.
- [ ] Source-of-truth roles remain clear.
- [ ] Public-surface wording does not replace tracker, roadmap, guardrails, code, or tests as authority.
- [ ] Validation evidence is included or clearly not required.
