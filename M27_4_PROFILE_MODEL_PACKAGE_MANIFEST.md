# M27.4 Profile Model Package Manifest

## Scope

User-applied implementation package for:

M27.4 — Profile model

## Files written by apply script

- `asbp/profile_source_model.py`
- `asbp/profile_source_store.py`
- `data/source/profiles/starter_profiles.json`
- `tests/test_profile_source_model.py`
- `docs/milestones/M27/M27_4_PROFILE_MODEL.md`

## Not included

- No tracker advancement
- No commit
- No push
- No pull request
- No GitHub write
- No DDR closure or reclassification

## Required validation after applying

Run from repository root:

    python -m pytest -q

Then run:

    git status --short

## Expected next workflow

If validation passes, request `UPT` to prepare the tracker update for M27.4 completion and M27.5 handoff.
