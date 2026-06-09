# No-Missed-Items Matrix

This file maps the old pack rule families into the product rebuild operation pack.

| Rule family from legacy pack | Product rebuild coverage | Where |
|---|---|---|
| Do not rely on memory | Covered | Project instructions, OPERATING_RULES §1 |
| Branch preflight | Covered | OPERATING_RULES §2, SESSION_CHECKLIST A |
| Do not assume main | Covered | OPERATING_RULES §2 |
| Repo truth before chat truth | Covered | OPERATING_RULES §1 |
| Read active rules before work | Covered | README, SESSION_CHECKLIST B |
| Repository write lock | Covered | OPERATING_RULES §8 |
| One bounded step | Covered | OPERATING_RULES §9 |
| No test-pass claims without evidence | Covered | OPERATING_RULES §6, SESSION_CHECKLIST E |
| Governance cannot substitute for implementation | Covered and strengthened | PRODUCT_BUILD_ROADMAP.md, OPERATING_RULES §3 |
| Avoid old roadmap continuation | Covered | OPERATING_RULES §4 |
| Active Assistant Gate | Replaced for rebuild | CURRENT_STATE + roadmap + git state |
| PR/merge strategy | Simplified | GitHub write rule + local command flow |
| DDR/readiness gates | Deferred unless touched | Do not revive old productization path |
| AI boundary | Covered | OPERATING_RULES §7 |
| Session handoff | Covered | HANDOFF_TEMPLATE.md |
| ChatGPT Project bootstrap | Covered | CHATGPT_PROJECT_INSTRUCTIONS.txt + ACTIVATION_PROMPT.md |

## Important intentional change

The old pack was optimized for a milestone/tracker-heavy repo.

The rebuild pack is optimized for:

- local branch truth
- product roadmap truth
- executable code
- tests
- UI/product behavior
- AI as candidate-support only

Do not mix both active packs.
