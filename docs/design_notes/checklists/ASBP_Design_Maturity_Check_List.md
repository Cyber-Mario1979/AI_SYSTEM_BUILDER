# ASBP Design Maturity Checklist

## A. Core Domain Clarity

- [ ] Task lifecycle fully defined (Open → Planned → In Progress → Completed)
- [ ] Each state has a clear meaning (not just labels)
- [ ] Derived states identified (e.g., Overdue)
- [ ] Status impact on scheduling clarified

## B. Scheduling Semantics

- [ ] Planned Duration defined
- [ ] Start Date defined
- [ ] Finish Date defined (derived vs stored)
- [ ] Due Date concept defined (if applicable)
- [ ] Overdue logic defined
- [ ] Rescheduling behavior defined

## C. Dependency Model

- [ ] Dependencies supported
- [ ] Task-to-task dependencies defined
- [ ] Work-package dependencies defined
- [ ] Lag handling defined
- [ ] Milestone/anchor-based dependencies supported
- [ ] Dependencies enforced vs advisory clarified

## D. Cross-Entity Relationships

- [ ] Work packages independence vs linkage defined
- [ ] Cross-WP dependencies supported (if required)
- [ ] Change propagation rules defined

## E. Calendar Model

- [ ] Single vs multiple calendars defined
- [ ] Calendar assignment model defined (global / user / WP)
- [ ] Work week configurable
- [ ] Non-working days affect scheduling

## F. Data vs Logic Separation

- [ ] Presets treated as data only
- [ ] Task pools treated as data
- [ ] No hidden logic inside data structures
- [ ] System tolerates large libraries

## G. Source of Truth

- [ ] Source of truth clearly defined
- [ ] No conflicting duplicated data
- [ ] Derived vs stored values clarified

## H. Automation Boundaries

- [ ] User responsibilities defined
- [ ] System responsibilities defined
- [ ] Automatic transitions defined
- [ ] Rule triggers clearly defined

## I. Export / Reporting Semantics

- [ ] Export = snapshot or dynamic clarified
- [ ] Overdue indicators included
- [ ] Dependencies visible in output
- [ ] Output consistent with internal logic

## J. Future-Proofing

- [ ] No hidden assumptions (single calendar, small data, etc.)
- [ ] Feature additions won't break core model
