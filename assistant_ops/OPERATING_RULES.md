# ASBP Product Rebuild Operating Rules

## 1. Source of truth

Use sources in this order:

1. Current local git output supplied by the user
2. `PRODUCT_BUILD_ROADMAP.md`
3. `assistant_ops/CURRENT_STATE.md`
4. `assistant_ops/OPERATING_RULES.md`
5. Repository files on the current branch
6. Current user instruction

Do not use old chat memory, old project memories, old uploaded packs, stale README wording, or old roadmap milestones as current truth.

## 2. Startup protocol

Before product code, planning, or roadmap interpretation, ask for:

```powershell
git branch --show-current
git log -1 --oneline
git status --short
```

Expected branch:

`product-rebuild-from-pre-pr23`

If the branch is different, stop and resolve branch state first.

## 3. Product work rule

After P0, no product milestone may close unless it ships at least one of:

- executable code
- tests
- runnable local behavior
- generated artifact
- product UI behavior
- validated scenario evidence

Documents may guide work, but documents alone cannot close product work.

## 4. No old drift continuation

Do not continue:

- PR #134
- M35.2 license strategy
- M32/M33/M34 as the product path
- old Phase 9 SaaS/Productization ladder
- governance-only milestone chains

## 5. P1 target

Current next product step:

`P1 — Product Application Service Layer`

Expected files:

- `asbp/product_app/__init__.py`
- `asbp/product_app/models.py`
- `asbp/product_app/service.py`
- `tests/test_product_app_service.py`

Required service functions:

- `list_work_packages`
- `get_work_package`
- `create_work_package`
- `select_work_package`
- `configure_work_package`
- `get_planning_view`
- `create_plan_amendment_candidate`
- `build_ai_context_packet`

## 6. Code and test rule

For code work, provide:

- exact files to create/update
- one paste block per terminal action
- exact tests to run
- expected behavior
- no claim that tests passed until user provides output

## 7. AI role

AI is part of the product value.

AI may:

- review governed context
- suggest tasks
- suggest document text
- identify gaps
- prepare candidate outputs

AI must not:

- mutate state directly
- own truth
- approve outputs
- silently change plans
- bypass deterministic service functions

## 8. GitHub write rule

Default: no live GitHub writes.

The assistant may prepare local commands or file contents.

The assistant must not create, update, close, delete, merge, or push via GitHub connector unless the user explicitly says:

`LIVE REPO WRITE: YES`

and the action is bounded.

## 9. Session rule

Work one step at a time.

End every session with a handoff containing:

- branch
- latest commit
- status
- done
- blocked
- next exact action
