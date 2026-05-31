# Docs Index Generation Notes

## Method

Generated from the local repository working tree using:

    git ls-files docs

The index excludes generated `docs/repo_index/` output to avoid self-index recursion.

## Branch / Commit

- Branch: `feature/m28-3-citation-model-contract`
- Commit: `7b0af0b0b05b7be30c23ee6978848f5f73b8fbe3`
- Generated local timestamp: `2026-05-31T05:47:12`

## Scope

This pass indexes tracked files and derived folders under `docs/` only.

It does not index the rest of the repository yet. It does not delete, rename, promote, or archive any file.

## Counts

- Indexed tracked files under docs: 312
- Indexed derived folders under docs: 89

## Exclusions

The index excludes runtime/cache/local artifacts such as `.git`, `.venv`, `__pycache__`, `.pytest_cache`, local `apply.py`, and generated `docs/repo_index/` output.

## Classification Limitations

Cleanup and promotion classifications are heuristic review aids only. They are not instructions to delete, rename, move, or promote files.

All cleanup/promotion actions require Project Owner review and explicit follow-up authorization.
