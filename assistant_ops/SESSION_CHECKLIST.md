# Session Checklist

Use this checklist at the start of every session.

## A. Confirm local state

Required user output:

- `git branch --show-current`
- `git log -1 --oneline`
- `git status --short`

Do not proceed if branch is not confirmed.

## B. Confirm active files

Read or confirm:

- `PRODUCT_BUILD_ROADMAP.md`
- `assistant_ops/CURRENT_STATE.md`
- `assistant_ops/OPERATING_RULES.md`

## C. Confirm next step

Current expected next product step:

`P1 — Product Application Service Layer`

## D. Before giving code

Check:

- branch is `product-rebuild-from-pre-pr23`
- roadmap exists
- assistant ops exists
- working tree is understandable
- requested action matches next step
- code will include tests

## E. Before claiming completion

Required evidence:

- user ran commands
- user pasted output
- tests passed or failure was analyzed
- latest commit is known
- next action is stated

## F. Stop conditions

Stop and clarify if:

- branch mismatch
- uncommitted unrelated changes
- missing roadmap
- missing ops files
- request attempts old M35/M32/M33/M34 continuation
- request asks for governance-only product milestone closure
- tests fail
- source of truth conflict appears
