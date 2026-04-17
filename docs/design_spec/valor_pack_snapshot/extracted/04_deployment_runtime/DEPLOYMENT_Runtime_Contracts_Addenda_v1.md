---
id: VALOR-deployment-runtime-contracts-addenda
version: v1
date: '2026-02-26'
ownership: Deployment Pack
scope: Consolidated runtime-facing addenda for reduced retrieval surface.
---

# Runtime Contracts Addenda (Consolidated)

This file consolidates runtime-relevant addenda into a single retrieval surface.

## A) Planning Invariants & UX Contract (source: ARCH_Addendum_Planning_Invariants_UX_Contract_v1.md)

# Planning Invariants & UX Contract (Single-Table Scheduling)

## 1) Definitions
- **Schedule Tasks**: Computes schedule dates (and optional owner defaults) and writes them **directly** into the Tasks table. This is a *proposal-in-place* represented by `Status = Planned` for eligible rows.
- **Commit Schedule**: Authorizes execution by changing statuses only (`WP: Open -> In Progress`; first eligible task `Planned -> In Progress`). Dates/owners are not changed by Commit Schedule.

## 2) Binding prerequisites

Before `Schedule Tasks <WP###> <dd-mm-yyyy>` may run, the Work Package MUST have the required scheduling bindings in WP **Bound Context**:
- `CAL=<calendar_id>@<ver>` (Calendar)
- `PROF=<profile_id>@<ver>` (Profile)

`TP=<TP-ID>@<ver>` (Task Pool) is not a standalone hard gate for scheduling, but it becomes required when the scheduler needs Task Pool lookups (for example, repairing a missing `Duration Ref` from `Atomic Task ID`).

## 3) Hard invariants (non-negotiable)

1. `Schedule Tasks <WP###> <dd-mm-yyyy>` MUST:
   - update Start/Finish dates in the existing Tasks table for planned tasks,
   - change eligible task Status from `Open` (or blank if unset) -> `Planned`,
   - use working-day arithmetic from the bound Calendar,
   - refuse planning if required scheduling bindings are missing (see §4).

2. `Schedule Tasks <WP###> <dd-mm-yyyy>` MUST NOT:
   - create any separate planning/proposal section or secondary planning table,
   - render any section titled `PLAN PROPOSAL`,
   - change WP Status,
   - change task IDs, WP IDs, or document IDs.

3. `Commit Schedule <WP###>` MUST:
   - stop and ask for explicit confirmation (`Yes/No`) before committing,
   - on **Yes**: change WP Status `Open` -> `In Progress` and change the **first eligible** task only from `Planned` -> `In Progress`,
   - on **No**: commit no changes.

4. `Commit Schedule <WP###>` MUST NOT:
   - change `Start Date`, `Finish Date`, `Owner`, `Dependencies`, or `Planned Duration (d)`.

## 4) Binding gate (critical)

Scheduling depends on the WP bound context. If any of the below are missing/unbound, ORCH must refuse scheduling:
- `CAL` (calendar_id + version)
- `PROF` (profile_id + version)

If `PROF` is missing/`UNBOUND`:
- refuse scheduling and instruct the user to use a WP preset (`Load Preset <code> Scope=<SCOPE>` / `Bind Planning Basis <WP###> Scope=<SCOPE>`) or explicitly set the Profile/Type on the WP header and run `Update WP###`.

If a task has a `Duration Ref` but the referenced `profile_key` is not found in the bound Profile record (including composite keys):
- refuse scheduling with the message:
`Planning failed: Duration Ref <key> not found in Profile <PROF-ID>. Check Bound Context or provide explicit Planned Duration (d).`

## 5) Deterministic duration resolution

### 5.1 Duration source precedence (strict)
For each task, resolve **Planned Duration (d)** in this strict order:

1) If task has **Planned Duration (d)** -> use it (must be integer >= 0).

2) Else if task has **Duration Ref**:
   - If it is `COMPOSITE(k1+k2+...)` -> resolve each key from the bound Profile Library and sum (after any required unit conversion to WORKING_DAYS).
   - Else resolve the single `duration_ref.profile_key` from the bound Profile Library.

3) Else if task has **Atomic Task ID**:
   - Resolve `Duration Ref` from the bound Task Pool (`atomic_task_id -> duration_ref.profile_key`), write it into the row, then resolve exactly as in step (2).

4) Else try Profile Library defaults (phase + task_type fallback, if implemented in the profile record).

5) Else fallback to `7` (WORKING_DAYS). Never default to `1`.

### 5.2 Authoritative lookup source
- **Authoritative:** WP **Bound Context** is the single source of truth for scheduling invariants:
  - Calendar: resolve `CAL=<calendar_id>@<version>` against `Libraries set (calendar_library)` across `ARCH_BUNDLE_Libraries_*`.
  - Profile: resolve `PROF=<profile_id>@<version>` against `Libraries set (profile_library)` across domain bundles.
  - Task Pool (when needed): resolve `TP=<task_pool_id>@<version>` against `ARCH_BUNDLE_Libraries_*`.
- `WP-HEADERS` (from `wp_header_library`) is user-facing header documentation only; it is non-authoritative if it conflicts with bound Calendar/Profile/Task Pool records.

### 5.3 Failure-mode diagnostic
If a planned WP shows most/all tasks with the fallback duration (`7`):
- treat as a binding or `Duration Ref` failure,
- verify:
  - WP Bound Context contains `PROF=<profile_id>@<version>`,
  - tasks were created from a Task Pool (they should carry `duration_ref.profile_key` / `Duration Ref` and often `Atomic Task ID`),
  - the profile record contains the referenced `profile_key` values.

## 6) Working-day date math

Definitions:
- `WD_ADD(date, n)` = add `n` working days to `date` per bound Calendar (skipping non-working days).
- `WD_NEXT(date)` = the next working day after `date`.

Rules:
- If `Planned Duration (d) = 0` -> Finish Date = Start Date.
- If `Planned Duration (d) = 1` -> Finish Date = Start Date.
- If `Planned Duration (d) > 1` -> Finish Date = `WD_ADD(Start Date, Planned Duration (d) - 1)`
- Next task Start Date = `WD_NEXT(previous Finish Date)`, unless dependencies push it later.

## 7) Dependency-aware forward pass
- Initialize the planning anchor to the first working day on/after the user-provided start date.
- Plan tasks in ascending Task ID order unless explicit dependencies require otherwise.
- Each task start date is the next working day after the maximum of:
  - the current sequential anchor, and
  - the latest predecessor finish date (+ lag days if defined).

## 8) Renderer validity requirement (Scheduling)

Any scheduling operation (`Schedule Tasks`, `Commit Schedule`) that mutates task statuses/dates must:
- re-render the Tasks table using the canonical renderer, and
- preserve a valid markdown Tasks table at all times.

If a safe Tasks table render cannot be produced, the system must refuse the mutation and keep the last valid Tasks table unchanged.

## B) Canvas Rendering & Record Layout (source: ARCH_Addendum_Canvas_Rendering_Record_Layout_v1.md; Deployment overrides applied)

# ARCH Addendum — Canvas Rendering & Record Layout Contract — v1

## 1) Global rules


- **After any Tasks mutation** (`Commit Tasks`, `Schedule Tasks`, bulk update), the Tasks section must be either:
  - a valid canonical markdown Tasks table, or
  - `- No tasks created yet.` (only if zero tasks).
- If rendering cannot be guaranteed, the mutation must be refused and the last valid Tasks render must be preserved.
- WP Canvas is the **truth view** for WP/task/plan records (Deployment mode).
- In M2, do not paste full WP Canvas truth blocks into chat (confirmations + snapshot + State Echo only).
- **Deployment exception:** document bodies and report bodies are rendered in chat; WP Canvas stores references only.
- Never render Canvas truth in fenced code blocks (document-like markdown only).
- Missing values render as **blank after the arrow** (e.g., `**Title** -> `). Do not print `No Entry`.
- Never leak internal renderer/template tokens into chat or Canvas (examples: `md_table`, `+md_table}]}`, raw JSON fragments, unexpanded `{...}` braces). If a table cannot be rendered safely, refuse the mutation and render a safe fallback (`- No tasks created yet.`).

## 2) Work Package (WP) Canvas layout

### 2.0 Isolation (one WP per canvas)

- Each Work Package MUST be rendered in its **own separate Canvas object** (titled `Work Package WP###`).
- It is **FORBIDDEN** for a single Canvas object to contain more than one `Work Package WP###` title line.
- If a canvas already contains a different WP title anywhere in its body, the system MUST refuse to append and MUST create/open the correct WP canvas instead.


### 2.1 Title (first line)
`Work Package WP###`

### 2.2 Header fields (exact order; one bullet per field)
 - **Work Package ID** -> WP###
 - **Title** ->
 - **Area** ->
 - **Scope** ->
 - **Objective** ->
 - **Governance** ->
 - **Type** -> ProcessEquipment | Utilities | CleanRoom | ComputerizedSystems
 - **Status** -> Open

### 2.3 Stamps (keep order; blank if unknown)
 - **Bound Context** -> CS=...; TP=...; PROF=...; CAL=...
 - **Planning Basis** -> Duration Source=...
 - **Plan Applied** -> <dd-mm-yyyy>
 - **Standards Bundle** -> SB-...@v1 OR SB-...@v1, SB-...@v1

### 2.4 Documents section

Header line (canonical): `**Documents**`

Pack-aligned rule (non-negotiable):
- The WP **Documents** register is **manual** in this pack.
- VALOR MUST NOT auto-edit the WP Documents list.
- Default placeholder when empty:
  - `- No documents created yet.`

Optional anchors:
- `<!-- VALOR:WP:WP###:DOC_INDEX:START -->`
- `<!-- VALOR:WP:WP###:DOC_INDEX:END -->`

These anchors may exist for future deterministic indexing, but in this pack they are **optional** and must not be relied on for automatic mutation.

## 3) Tasks section

### 3.1 Tasks header
`**Tasks**`

**Anchor block (recommended; deterministic updates):**
Immediately under the Tasks header, the canvas SHOULD contain the following two sentinel lines (exact; include the WP ID):
- `<!-- VALOR:WP:WP###:TASKS:START -->`
- `<!-- VALOR:WP:WP###:TASKS:END -->`

Rules:
- The Tasks content (either placeholder or table) is everything between START and END.
- If none: render the placeholder line inside the anchor block:
  - `- No tasks created yet.`

**Canvas patch safety (prevents regex escape failures):**
- Treat Canvas "match"/"replace" primitives as regex-sensitive. Avoid backslash-based regex tokens (examples: `\s`, `\S`, `\d`, `\b`, capture backrefs like `\1`).
- Safe full-block replacement pattern (no backslashes):
  - Match: `(?s)<!-- VALOR:WP:WP###:TASKS:START -->.*?<!-- VALOR:WP:WP###:TASKS:END -->`
  - Replace with: START sentinel + newline + placeholder/table + newline + END sentinel.


### 3.2 Planning table (canonical task representation)

When tasks exist, render them in a **Markdown table** with **exactly** the columns below (canonical):

| Task ID | Description | Owner | Status | Planned Duration (d) | Start Date | Finish Date | Dependencies | Atomic Task ID | Duration Ref |
| ------- | ----------- | ----- | ------ | -------------------: | ---------- | ----------- | ------------ | -------------- | ------------ |

**Column rules (strict; pack-canonical order):**
- **Task ID**: Required (WP###-T### format)
- **Description**: Required (single line; sanitize tabs/newlines to spaces)
- **Owner**: Optional (blank if not assigned)
- **Status**: Required (default: Open)
- **Planned Duration (d)**: Optional until planned; written by planning/commit (or fallback rules per planning addendum)
- **Start Date**: Optional (blank until planned/applied); display format `dd-mm-yyyy`
- **Finish Date**: Optional (blank until planned/applied); display format `dd-mm-yyyy`
- **Dependencies**: Optional (blank or comma-separated Task IDs)
- **Atomic Task ID**: Optional task-pool linkage (use `—` if not applicable)
- **Duration Ref**: Optional until planned/committed; required for deterministic duration resolution unless `Planned Duration (d)` is present

**Rendering guards (non-negotiable):**
- Always render **exactly 10 columns** (no extra empty columns).
- Every row must have the same column count as the header.
- If content contains `\t`, `\n`, or `\r`, replace with spaces before rendering.
- Never output dangling lines outside the table.




## 4) Preset / staging visibility (pack-aligned)

- After `Load Preset <Code> Scope=<SCOPE>`:
  - ORCH creates a **new** WP canvas (`Work Package WP###`) and writes the WP header/context.
  - WP Canvas `Tasks` must remain empty (`- No tasks created yet.` inside the TASKS anchor block).
  - ORCH must **not** preload structured tasks into the Tasks table.

- Task staging occurs only after:
  - `Stage Tasks WP###`

- `Stage Tasks WP###` is **chat-only** and uses the strict deterministic preview format:
  - `staged_task_set_id: <STS-ID>`
  - `idx | task_id | title`
  - one row per staged task in canonical Task Pool order

- Structured tasks (IDs + fields) are created only after:
  - `Commit Tasks WP### [<indices>]`

## 5) Planning Status Indicators

Tasks show planning state via the **Status** column in the Tasks table:

**Status Values:**
- **Open**: Task created, no planning applied yet
- **Planned**: Dates (and allowed owner defaults) assigned by `Schedule Tasks <WP###> <dd-mm-yyyy>`; awaiting `Commit Schedule <WP###>`
- **In Progress**: Execution authorized after `Commit Schedule <WP###>` (status-only apply)
- **Completed**: Task finished and approved

**Key principle:** The Tasks table is the single source of truth. There is NO separate "PLAN PROPOSAL" section.

## C) Reporting & Export Projection Contract (source: ARCH_Addendum_Reporting_Export_Projection_Contract_v1.md)

# ARCH Addendum — Reporting & Export Projection Contract — v1

**Applies to:** M1/M2 projection features (`Build Report`, `Export`, `Consolidated Export`, `Create Gantt Chart`)
**Related:** `02_Orchestration_Core.md`, `03_KS_Core.md`, `09_Valor_Export_Template.csv`

## 1) Overview
This addendum defines the **single authoritative CSV export format** for Valor work packages (single and consolidated multi-WP).

**Key rules**
- Export is **projection-only** (never mutates WP/task truth).
- Export must generate a **downloadable CSV file** (preferred). Fallback: if file generation fails, inline CSV in chat as a single code block.
- Export must always include the **full strict column set** (16 columns, exact names, exact order).
- If the strict format cannot be guaranteed, the assistant must refuse the export.

## 2) Command
- `Export` → exports the **Active WP**
- `Export WP###` → exports the specified WP
- `Consolidated Export [WP IDs]` → exports multiple WPs into single CSV
- `Consolidated Export all` → exports all session WPs into single CSV

## 3) File naming

**Single WP:**
- `VALOR_Export_<WPID>_<PLANID or NOPLAN>_<dd-mm-yyyy>.csv`

**Consolidated:**
- `VALOR_Consolidated_Export_<count>WPs_<dd-mm-yyyy>.csv`

Examples:
- `VALOR_Export_WP002_PLAN001_04-01-2026.csv`
- `VALOR_Consolidated_Export_3WPs_07-01-2026.csv`

## 4) CSV strict schema (columns)
The CSV must contain **exactly** these columns (names & order must match):

1. WP ID  
2. Title  
3. Scope  
4. Objective  
5. Governance  
6. Task ID  
7. Task Description  
8. Task Status  
9. Task Owner  
10. Start Date  
11. Finish Date  
12. Planned Duration (d)  
13. Elapsed (d)  
14. Remaining (d)  
15. Lateness (d)  
16. % Time Elapsed

**Canonical CSV header row (exact):**  
`WP ID,Title,Scope,Objective,Governance,Task ID,Task Description,Task Status,Task Owner,Start Date,Finish Date,Planned Duration (d),Elapsed (d),Remaining (d),Lateness (d),% Time Elapsed`

- If `09_Valor_Export_Template.csv` is unavailable at runtime, use the canonical header row above (do not refuse solely due to template access).

### 4.1 Data formatting rules
- Dates must be `dd-mm-yyyy`.
- `% Time Elapsed` must be an integer percent string like `0%`, `25%`, `100%`.
- Empty/unknown values are allowed **as blank cells**, but columns must never be omitted.

## 5) Projection calculations (strict)
All calculations are computed as-of **Export Date**, which is the session stamp `DateTime <dd-mm-yyyy hh:mm AM/PM Cairo-Egypt>` (use the date component as Export Date).

Let:
- `S` = Start Date
- `F` = Finish Date
- `D` = Export Date

### 5.1 Planned Duration (d)
If S and F exist:
  - Planned Duration (d) = the number of **working days** between `S` and `F` inclusive, using the bound Calendar defined in the planning invariants. In other words, count only working days and include both the start and finish dates.
If missing S or F:
  - Planned Duration (d) = blank

### 5.2 Elapsed (d)
If S and F exist:
  - If `D < S` → Elapsed (d) = `0`
  - If `S <= D <= F` → Elapsed (d) = the number of **working days** between `S` and `D` inclusive, using the same bound Calendar as in Planned Duration.
  - If `D > F` → Elapsed (d) = Planned Duration (d)
If missing S or F:
  - Elapsed (d) = blank

### 5.3 Remaining (d)
If Planned Duration exists:
- Remaining (d) = `max(0, Planned Duration - Elapsed)`
Else:
- Remaining (d) = blank

### 5.4 Lateness (d)
If F exists:
  - If `D <= F` → Lateness (d) = `0`
  - If `D > F` → Lateness (d) = the number of **working days** between `F` and `D`, excluding `F` and including `D`, computed per the bound Calendar.
Else:
  - Lateness (d) = blank

### 5.5 % Time Elapsed
If Planned Duration exists and > 0:
- % Time Elapsed = `round((Elapsed / Planned Duration) * 100)` as integer + `%`
Else:
- % Time Elapsed = blank

## 6) Owner fallback rules
- If a task owner is missing:
  - Use WP Governance as the owner fallback
  - If Governance is also missing → leave blank

## 7) Compliance self-check before confirming
Before saying "export completed successfully" the assistant must verify:
- Column names and order match section&nbsp;4 exactly
- All computed columns exist (12—16)
- All rows conform to the CSV schema (correct field count, valid date formats, etc.)
If validation fails:
- Respond with a detailed refusal message indicating the specific column(s) or row(s) that failed (e.g., "Export failed: invalid date format in row&nbsp;3, column&nbsp;10" or "Export failed: missing column 'Finish&nbsp;Date'").
- Do not generate a file.

## 8) Template file
The canonical header template is stored as:
- `09_Valor_Export_Template.csv`

The exporter must follow it exactly.

---

## 9) Multi-WP Consolidation (v7.1.1 extension)

### Build Consolidated Report
**Command:** `Build Consolidated Report [WP IDs]` or `Build Consolidated Report all`

**Input:** `wp_snapshots: array` (1 or more WP projections)

**Output:** Single markdown document (Canvas) with:
- **Executive Summary:** Aggregate stats across all WPs (total tasks, completion %, critical path summary)
- **Per-WP Sections:** Same structure as single-WP report (one section per WP)
- **Cross-WP Dependency Visualization:** If task dependencies exist across WPs, include a dependency graph or list
- **Consolidated Completeness Assessment:** Overall project/program health score

**Mode:** M1/M2, projection-only (no Canvas mutations)

**Performance limit:** Max 10 WPs per operation

**Chat output:**
- `Confirmed.`
- `Consolidated report generated for N WPs: [WP IDs].`
- `Moved to Canvas. Continue.`

---

### Consolidated Export
**Command:** `Consolidated Export [WP IDs]` or `Consolidated Export all`

**Input:** `wp_snapshots: array` (1 or more WP projections)

**Output:** Single CSV file with:
- Same 16-column schema as single-WP export
- All WPs' tasks in one file (WP ID column differentiates)
- File naming: `VALOR_Consolidated_Export_<count>WPs_<dd-mm-yyyy>.csv`

**Strict refusal gate applies** (same as single-WP export):
- Template compliance must be guaranteed
- All 16 columns present in correct order
- Computed fields (12—16) must be calculated for each task

**Performance limit:** Max 10 WPs per operation

**Chat output:**
- `Confirmed.`
- `Consolidated export generated for N WPs: [WP IDs].`
- `Download: VALOR_Consolidated_Export_NWPs_dd-mm-yyyy.csv`
- Attach the file

---

### Gantt Chart Projection
**Command:** `Create Gantt Chart [WP IDs]` or `Create Gantt Chart all`

**Input:** `wp_snapshots: array` (requires plan data for each WP)

**Output format:** Rendered visual (SVG/PNG) - PRIMARY output with no extra user steps required

**Rendering method:**
- Generate Mermaid gantt diagram code internally
- Render using the available runtime renderer (e.g., Code Interpreter). If no renderer is available, output the Mermaid source only (no images).
- Return rendered image as primary deliverable
- Mermaid source code is OPTIONAL/SECONDARY (only if user explicitly requests it)

**Output structure:**
- Horizontal timeline (start date to latest finish date across all WPs)
- Task bars grouped by WP (section per WP)
- Dependency arrows (intra-WP dependencies shown; cross-WP if schema supports)
- Milestone markers (plan applied dates, phase boundaries)
- Color coding by task status:
  - Open: blue
  - Planned: light blue
  - In Progress: yellow
  - Drafted: orange
  - Completed: green
  - Overdue: red
 - Cross-WP dependencies: show arrows between tasks in different WPs when defined in `external_dependencies`.

**File naming:**
- `VALOR_Gantt_<count>WPs_<dd-mm-yyyy>.png` (rendered visual - primary)
- `VALOR_Gantt_<count>WPs_<dd-mm-yyyy>.mmd` (Mermaid source - optional, only if requested)

**Refusal conditions:**
1. **Missing plan data:** If any WP lacks applied plan data → refuse with message:
   - `All WPs must have applied plans. Missing: [WP IDs].`
   - `Run 'Plan tasks <date>' and 'Apply Plan' for each WP first.`

2. **Date range > 2 years:** Warn user about readability:
   - `Timeline spans N years. Chart may be difficult to read. Proceed? (Yes/No)`

**Performance limit:** Max 10 WPs per operation

**Cross-WP dependency handling (v7.1.1):**
- Supported via optional task field `external_dependencies` (array of `WP###-T###`).
- When present, render cross-WP arrows; otherwise render intra-WP dependencies only.

**Chat output:**
- `Confirmed.`
- `Gantt chart generated for N WPs: [WP IDs].`
- `Timeline: <earliest start> to <latest finish>.`
- Display the rendered Gantt chart image inline (primary deliverable)
- `Download: VALOR_Gantt_NWPs_dd-mm-yyyy.png`
- If user requested Mermaid source: also attach `.mmd` file

**Example visual output:**
The rendered Gantt chart displays as an inline image showing the timeline with color-coded task bars grouped by Work Package.

---

## 10) Multi-WP Command Parsing Rules

**Explicit WP ID list:**
- `Build Consolidated Report WP001 WP002 WP003`
- `Consolidated Export WP001 WP002`
- `Create Gantt Chart WP001 WP002 WP003 WP004`

**"all" keyword:**
- `Build Consolidated Report all` → include all WPs in current session
- `Consolidated Export all` → include all WPs in current session
- `Create Gantt Chart all` → include all WPs in current session

**Max WP count:** 10 WPs per operation
- If user requests >10 WPs → refuse with message:
  - `Maximum 10 WPs per consolidated operation. You requested N. Please reduce the selection.`

**Min WP count:** 1 WP required
- If no WPs exist or user provides empty list → refuse with message:
  - `No WPs available for consolidated operation. Create at least one WP first.`

---

## 11) Backwards Compatibility

**Single-WP commands unchanged:**
- `Build Report` → single WP report (chat)
- `Export` or `Export WP###` → single WP CSV export (file)

**No breaking changes:**
- Existing single-WP workflows continue to work exactly as before
- Consolidated commands are purely additive

---

## D) Document Generation Compliance (source: ARCH_Addendum_Document_Generation_Compliance_v1.md)

# Document Generation Compliance Addendum

## 1) Separate objects
- Documents are rendered in chat by default (Deployment mode); WP Canvas stores a Documents index (references only).
- WP Canvas may include a **Documents** index list (references only).

## 2) Token-clean rule (strict)
Final document output MUST NOT contain:
- `{{ ... }}` tokens
- `{}` or `{ }` placeholders
- `<...>` placeholders

If required content is missing:
- leave the value blank, or write `TBD` (plain text), not braces.

## 3) No operational/footer text inside documents
Document bodies must not include runtime/UI lines such as:
- `Mode: ...`, `State: ...`, `Canvas ready`, `Next -> ...`, `To commit: ...`, etc.

Operational guidance must remain in chat only.

## 4) Timestamps
- Timestamp format (date + time): `dd-mm-yyyy hh:mm AM/PM Cairo Time - Egypt`
- 12-hour clock with `AM/PM` exactly.
- Never label a timestamp as UTC unless it is actually UTC.
- If the user provides the current Cairo time during testing, treat it as the session NOW for stamping until updated.
