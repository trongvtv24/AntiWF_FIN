# AWF Core Operating Guide

Use this file as the lightweight loading path before reading long workflow or skill bodies.

## Load Order

1. Read `awf_manifest.yaml` to identify the active workflow, gates, required skills, conditional skills, risk level, and handoff path.
2. Read `global_workflows/GLOBAL_SAFETY_TRUTHFULNESS_GATE.md` before making factual, external, persuasive, legal, financial, medical, security, publishing, or deployment claims.
3. Read `global_workflows/CONTEXT_SYSTEM.md` only when memory files under `.brain/` are needed.
4. Read the selected workflow file body only after the workflow is chosen.
5. Read required skill bodies only after the workflow requires them.
6. Read conditional skill bodies only when the user's request matches their manifest trigger.

## Context Budget Rules

- Prefer manifest metadata over scanning every workflow.
- Do not load large skill bodies speculatively.
- Keep long workflow and skill files as references; use frontmatter and manifest routing first.
- If a workflow or skill contains provider limits, pricing, quotas, or current feature claims, verify them from official sources in the current session before using them as facts.
- If a skill is `suggestion_only`, it may propose improvements but must not mutate files itself. Route approved durable changes through the proper workflow.

## Artifact Rules

- Workflow `writes` must name concrete artifacts or stable artifact classes, not generic placeholders.
- Durable memory belongs in `.brain/` and should be written through `/save-brain`.
- Feature plans belong in `plans/[YYMMDD]-[HHMM]-[slug]/`.
- Feature specs belong in `docs/specs/[feature]_spec.md`.
- Architecture and API decisions belong in `docs/DESIGN.md`.
- UI decisions belong in `docs/design-specs.md`.
