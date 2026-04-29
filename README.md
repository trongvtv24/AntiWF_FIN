# AntiWF_FIN - Antigravity Workflow Framework v4.0

AntiWF_FIN is the AWF v4 system bundle for Antigravity: global slash-command workflows, reusable skills, schemas, templates, and a central manifest that routes user intent into the right workflow and skill set.

## Source Of Truth

| File | Role |
| --- | --- |
| `awf_manifest.yaml` | Central router for workflows, skills, gates, risk levels, and handoff paths |
| `global_workflows/references/CORE_OPERATING_GUIDE.md` | Lightweight load order and context-budget rules before reading long workflow or skill bodies |
| `global_workflows/GLOBAL_SAFETY_TRUTHFULNESS_GATE.md` | Mandatory truthfulness and safety gate for claims, edits, deployment, publishing, research, and content |
| `global_workflows/CONTEXT_SYSTEM.md` | Canonical memory contract for `.brain/` files |
| `schemas/*.schema.json` | Machine-readable contracts for AWF memory files |
| `templates/*.example.json` | Example files that match the schemas and context contract |

## Workflow Groups

Core software flow:

```text
/init -> /brainstorm -> /plan -> /design -> /visualize -> /code -> /run -> /test -> /audit -> /deploy
```

Maintenance and recovery:

```text
/recap -> /next -> /debug -> /refactor -> /rollback -> /save-brain
```

Content and publishing:

```text
/script -> /fb-post
```

## AWF v4 Guarantees

- All important workflows route through `awf_manifest.yaml`.
- Important factual or persuasive claims go through the global truthfulness gate.
- Durable memory is written only through `/save-brain`.
- Lightweight checkpoints are append-only through `session_log.txt`.
- Facts, decisions, and unverified claims are separated.
- High-risk and critical workflows declare confirmation requirements in the manifest.

## Context Files

AWF v4 uses `.brain/` as the local project memory folder:

```text
.brain/
  brain.json          Stable repo/user-confirmed facts
  session.json        Current work state
  session_log.txt     Append-only lightweight checkpoints
  handover.md         Session handover when context is long or risky work starts
  decisions.md        Append-only decision log
  claims.md           Claim ledger for assumptions and verification gaps
  preferences.json    Local communication and working-style preferences
```

Use the files in `templates/` as starting points and validate against `schemas/`.

## Install

Copy the core folders and files into the Antigravity data directory:

```text
global_workflows/
skills/
schemas/
templates/
plugins/
awf_manifest.yaml
mcp_config.json
```

Typical Windows location:

```text
%USERPROFILE%\.gemini\antigravity\
```

## Validation

Run the AWF-aware validator after changing workflows, skills, schemas, templates, or `awf_manifest.yaml`:

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_awf.py --strict
```

This validator accepts AWF extended frontmatter such as `risk_level`, `required_gates`, `allowed_side_effects`, and `related_workflows`.

## Notes

- `fb-publisher` is intentionally left as a private/local publishing skill.
- Runtime data, cache folders, local session data, logs, and secrets should stay out of new commits unless deliberately versioned.
- After changing workflow or skill metadata, validate that every path in `awf_manifest.yaml` exists.
