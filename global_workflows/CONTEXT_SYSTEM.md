---
type: system_contract
name: context_system
awf_version: 4.0.0
contract_version: 4.0.0
status: active
category: context
risk_level: medium
applies_to:
  - save-brain
  - recap
  - auto-save
  - session-restore
  - note-taking
  - context-engineering
outputs:
  - brain_json_contract
  - session_json_contract
  - memory_write_policy
# AWF_METADATA_START
command: null
awf_version: "4.0.0"
status: active
category: "context"
risk_level: "medium"
triggers:
  - "context_system"
inputs:
  - "project_context"
outputs:
  - "system_contract"
reads:
  - "awf_manifest.yaml"
writes:
  - "none"
required_gates:
  - "context_system"
  - "global_safety_truthfulness_gate"
skill_hooks:
  required: []
  conditional: []
handoff:
  next_workflows: []
# AWF_METADATA_END
---

# AWF Context System v4.0

This is the single source of truth for AWF project memory. It replaces overlapping memory behavior across `/save-brain`, `/recap`, `awf-auto-save`, `awf-session-restore`, `awf-note-taking`, and `context-engineering`.

## Core Rule

Do not mix stable facts, temporary state, decisions, and unverified claims.

| Data type | Canonical home |
| --- | --- |
| Stable repo-observed or user-confirmed facts | `.brain/brain.json` |
| Current task/session progress | `.brain/session.json` |
| Lightweight checkpoints | `.brain/session_log.txt` |
| Session handoff | `.brain/handover.md` |
| Important decisions and rationale | `.brain/decisions.md` |
| Claims, assumptions, and verification gaps | `.brain/claims.md` |
| Local communication and working style | `.brain/preferences.json` |

## File Roles

| File | Role | Writer | Read by |
| --- | --- | --- | --- |
| `.brain/brain.json` | Stable project knowledge only | `/save-brain` | `/recap`, `/plan`, `/design`, `/code`, `/audit` |
| `.brain/session.json` | Current session state | `/save-brain`, bounded workflow checkpoints | `/recap`, `/next`, `/code`, `/debug`, `/run` |
| `.brain/session_log.txt` | Append-only task checkpoints | `awf-auto-save`, `/code`, `/visualize`, `/plan` | `/recap`, `/next` |
| `.brain/handover.md` | Context-window handover | `/save-brain`, proactive handover | `/recap` |
| `.brain/decisions.md` | Append-only decision log | `/save-brain`, confirmed workflow decisions | `/plan`, `/design`, `/code`, `/audit` |
| `.brain/claims.md` | Claim ledger | `/save-brain`, research/content workflows | `/brainstorm`, `/script`, `/fb-post`, `/audit` |
| `.brain/preferences.json` | Local preferences | `/customize` | all workflows |

## Write Policy

- `/save-brain` is the canonical writer for durable memory.
- `/recap` is read-only. It may suggest repairs if files are missing or corrupted, but it must not silently rewrite durable memory.
- `awf-auto-save` may append to `.brain/session_log.txt` and update only narrow session progress fields in `.brain/session.json`.
- `awf-session-restore` reads context and summarizes. It does not create new facts.
- `awf-note-taking` writes notes only after explicit user confirmation.
- `context-engineering` decides what context to include in the prompt. It does not create competing memory stores.
- Unverified claims must never be promoted into `brain.json`.

## brain.json Contract

`brain.json` stores facts that should survive sessions. It must validate against `schemas/brain.schema.json`.

Required top-level shape:

```json
{
  "meta": {
    "schema_version": "4.0.0",
    "awf_version": "4.0.0",
    "created_at": "2026-04-29T00:00:00+07:00",
    "updated_at": "2026-04-29T00:00:00+07:00"
  },
  "project": {
    "name": "project-name",
    "type": "fullstack",
    "status": "development",
    "source": "repo_observed"
  },
  "tech_stack": {},
  "architecture": {},
  "database_schema": {},
  "api_endpoints": [],
  "business_rules": [],
  "features": [],
  "knowledge_items": {},
  "environment": {},
  "updated_at": "2026-04-29T00:00:00+07:00"
}
```

Rules:

- Store only repo-observed facts or facts explicitly confirmed by the user.
- Store required environment variable names, never secret values.
- Use `source` fields when useful to make facts auditable.
- Do not store temporary progress, failed attempts, open assumptions, or unverified claims.
- When a stable fact comes from a decision, mirror the decision in `decisions.md`.

## session.json Contract

`session.json` stores short-lived state. It must validate against `schemas/session.schema.json`.

Required top-level shape:

```json
{
  "meta": {
    "schema_version": "4.0.0",
    "awf_version": "4.0.0",
    "created_at": "2026-04-29T00:00:00+07:00",
    "updated_at": "2026-04-29T00:00:00+07:00"
  },
  "updated_at": "2026-04-29T00:00:00+07:00",
  "message_count": 0,
  "summary": {
    "project": "project-name",
    "status": "coding",
    "current_feature": "feature-name",
    "current_task": "current task",
    "progress_percent": 50,
    "last_action": "last completed action",
    "next_step": "recommended next step",
    "blockers_count": 0
  },
  "working_on": {
    "feature": "feature-name",
    "task": "current task",
    "status": "coding",
    "files": [],
    "blockers": [],
    "notes": null
  },
  "current_plan_path": null,
  "current_phase": null,
  "pending_tasks": [],
  "recent_changes": [],
  "errors_encountered": [],
  "skipped_tests": [],
  "decision_refs": [],
  "claim_refs": [],
  "last_run": null,
  "handover_required": false
}
```

Rules:

- Keep this file small and focused on current workflow state.
- Use `decision_refs` and `claim_refs` as pointers only. The durable logs live in `decisions.md` and `claims.md`.
- Move stable learnings into `brain.json` only through `/save-brain`.
- Tests, builds, screenshots, deploys, and publishes may be recorded only if they actually ran.

## session_log.txt Contract

`session_log.txt` is append-only. Each checkpoint should be compact:

```text
[2026-04-29T10:00:00+07:00] trigger=workflow_end workflow=/code
summary=Implemented auth validation; tests not run; next=/test
files=src/features/auth/validate-user.ts
```

Rules:

- Do not rewrite old entries.
- Prefer one compact checkpoint per meaningful workflow event.
- Use it for recovery, not as a durable project knowledge store.

## decisions.md Contract

Append-only decision log:

```md
## 2026-04-29 - Use Recharts for revenue chart

Context:
- Revenue dashboard needs a simple time-series chart.

Decision:
- Use Recharts.

Rationale:
- It already fits the React stack and is enough for the current chart.

Alternatives considered:
- Chart.js

Consequences:
- Add chart-specific test coverage before release.
```

## claims.md Contract

Claim ledger:

```md
## Claim Ledger

| Claim | Type | Evidence | Status | Used in output? |
| --- | --- | --- | --- | --- |
| ... | repo/user/external/assumption | file/source/user | verified/unverified | yes/no |
```

Unverified claims must stay out of production content, deploy decisions, audit conclusions, and final reports unless explicitly labeled.

## Handover Rules

Create `.brain/handover.md` when:

- Context is getting long.
- A phase is done.
- A risky action is about to start.
- User pauses work.

Handover must include:

- Current goal.
- Files touched or important files.
- Completed work.
- Pending work.
- Decisions.
- Assumptions and unverified claims.
- Tests/checks run and skipped.

## Conflict Resolution

If memory conflicts:

1. Prefer repo-observed facts over saved memory.
2. Prefer newer explicit user decisions over older notes.
3. Keep conflicting claims in `claims.md` until resolved.
4. Do not silently discard a conflict that affects implementation, publishing, or deployment.

## Validation

Before finishing `/save-brain`:

- Validate `brain.json` against `schemas/brain.schema.json` when it was changed.
- Validate `session.json` against `schemas/session.schema.json` when it was changed.
- Validate `preferences.json` against `schemas/preferences.schema.json` when it was changed.
- Report validation as run only if it actually ran.
