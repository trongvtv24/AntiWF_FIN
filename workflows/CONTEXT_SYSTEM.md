---
type: system_contract
name: context_system
awf_version: 4.0.0
contract_version: 1.0.0
status: active
category: context
risk_level: medium
applies_to:
  - save-brain
  - recap
  - auto-save
  - session-restore
  - note-taking
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

# AWF Context System

This is the single source of truth for project memory. It replaces overlapping memory behavior across `/save-brain`, `/recap`, `awf-auto-save`, `awf-session-restore`, `awf-note-taking`, and `context-engineering`.

## File Roles

| File | Role | Writer | Read by |
| --- | --- | --- | --- |
| `.brain/brain.json` | Stable project knowledge | `/save-brain` | `/recap`, `/plan`, `/design`, `/code`, `/audit` |
| `.brain/session.json` | Current session state | `/save-brain`, bounded workflow checkpoints | `/recap`, `/next`, `/code`, `/debug`, `/run` |
| `.brain/session_log.txt` | Lightweight append-only task checkpoints | `awf-auto-save`, `/code`, `/visualize` | `/recap`, `/next` |
| `.brain/handover.md` | Context-window handover | `/save-brain`, proactive handover | `/recap` |
| `.brain/decisions.md` | Important decisions and rationale | `/save-brain`, confirmed workflow decisions | `/plan`, `/design`, `/code`, `/audit` |
| `.brain/claims.md` | Claims, assumptions, and verification gaps | `/save-brain`, research/content workflows | `/brainstorm`, `/script`, `/fb-post`, `/audit` |
| `.brain/preferences.json` | Local user/project preferences | `/customize` | all workflows |

## Write Policy

- `/save-brain` is the canonical writer for durable memory.
- `/recap` is read-only. It may suggest repairs if files are missing or corrupted, but it must not silently rewrite durable memory.
- `awf-auto-save` may append lightweight checkpoints to `session_log.txt` and update narrow session progress fields only.
- `awf-session-restore` reads context and summarizes; it does not decide new facts.
- `awf-note-taking` writes notes only after explicit user confirmation.
- `context-engineering` guides what context to include; it does not create competing memory stores.

## brain.json

Stable facts that should survive sessions:

```json
{
  "project": {},
  "tech_stack": {},
  "architecture": {},
  "database_schema": {},
  "api_endpoints": [],
  "business_rules": [],
  "features": [],
  "conventions": [],
  "knowledge_items": []
}
```

Rules:

- Store facts observed from repo or confirmed by user.
- Do not store temporary task status.
- Do not store unverified claims as facts.
- When a fact comes from a user decision, mirror the decision in `decisions.md`.

## session.json

Current dynamic state:

```json
{
  "working_on": {},
  "current_plan_path": null,
  "current_phase": null,
  "pending_tasks": [],
  "recent_changes": [],
  "errors_encountered": [],
  "skipped_tests": [],
  "last_run": null,
  "handover_required": false
}
```

Rules:

- Keep this small.
- Update only fields related to the current workflow.
- Move durable learnings into `brain.json` through `/save-brain`.

## decisions.md

Append-only decision log:

```md
## YYYY-MM-DD - Decision title

Context:
- ...

Decision:
- ...

Rationale:
- ...

Alternatives considered:
- ...

Consequences:
- ...
```

## claims.md

Use this to prevent hallucinated facts:

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
4. Do not silently discard a conflict that affects implementation or publishing.

