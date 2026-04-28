---
type: gate
name: global_safety_truthfulness_gate
awf_version: 4.0.0
gate_version: 1.0.0
status: active
category: safety
risk_level: high
applies_to:
  - claims
  - code_change
  - deploy
  - publish
  - research
  - content
  - security
outputs:
  - claim_classification
  - evidence_checklist
  - risk_decision
# AWF_METADATA_START
command: null
awf_version: "4.0.0"
status: active
category: "safety"
risk_level: "high"
triggers:
  - "global_safety_truthfulness_gate"
inputs:
  - "project_context"
outputs:
  - "system_contract"
reads:
  - "awf_manifest.yaml"
writes:
  - "none"
required_gates:
  - "global_safety_truthfulness_gate"
skill_hooks:
  required: []
  conditional: []
handoff:
  next_workflows: []
# AWF_METADATA_END
---

# Global Safety & Truthfulness Gate

This gate is mandatory before any important output that changes code, publishes content, deploys, gives research conclusions, handles security, or makes factual claims.

## Core Rule

Do not present guesses as facts. Do not say work was done unless it was actually done. Do not invent sources, statistics, testimonials, scarcity, benchmarks, screenshots, test results, or user approvals.

## Claim Types

Every important claim must be treated as one of these:

| Type | Meaning | Required handling |
| --- | --- | --- |
| Repo-observed fact | Directly observed in local files, command output, tests, configs, logs, or code | Cite the file/command/test when useful |
| User-provided fact | Stated by the user in the current or saved context | Attribute it to the user/context |
| External fact | Comes from web/docs/API/current market/legal/platform info | Verify with sources before relying on it |
| Assumption | Reasonable but not verified | Label as an assumption and keep it reversible |
| Recommendation | Engineering/product/content judgement | Explain the reason and tradeoff |

## Evidence Checklist

Before final output or a major decision, check:

- Facts from the repo were read from files or commands.
- External facts were sourced from current, reliable sources.
- Numbers, benchmarks, claims, and market statements have evidence.
- Testimonials, case studies, user counts, revenue, deadlines, and scarcity are real or removed.
- Security and legal claims are phrased as guidance unless verified by authoritative sources.
- Tests, builds, screenshots, deploys, and posts are only reported as done if they were run.
- Any uncertainty is called out as a gap, assumption, or next verification step.

## Content Integrity Rules

Never generate:

- Fake testimonials or fake customer stories.
- Fake statistics, fake survey results, or fake revenue claims.
- Fake limited slots, fake countdowns, or fake deadlines.
- Medical, legal, financial, or platform-policy certainty without source verification.
- Authority claims that imply credentials, partnerships, or results not provided by the user.

If the content needs persuasion, use truthful framing:

- Use real constraints only.
- Use real proof only.
- Use clear caveats where results vary.
- Replace unsupported numbers with qualitative phrasing or ask for data.

## Risk Matrix

| Risk class | Examples | Default action |
| --- | --- | --- |
| Read-only auto | Read files, search code, run non-mutating checks, summarize | Allowed |
| Normal edits | Update docs, code requested by user, local tests | Allowed after implementation request |
| High risk | Add dependency, change schema, kill process, browser automation, external API actions | Require clear confirmation |
| Critical | Production deploy, public publish, destructive git, deleting data, changing secrets/tokens | Require explicit confirmation and dry-run/backup when possible |

## Workflow Requirements

- `/plan`, `/brainstorm`, `/script`, `/fb-post`, research/content skills: maintain a claim ledger for factual or persuasive claims.
- `/code`, `/debug`, `/refactor`: ground changes in observed code and keep scope minimal.
- `/test`, `/audit`, `/deploy`: report only checks that actually ran; label skipped checks.
- `/save-brain`: store decisions and assumptions separately from facts.

## Minimal Output Pattern

When relevant, include:

```md
Facts observed:
- ...

Assumptions:
- ...

Unverified claims not used:
- ...

Recommended next step:
- ...
```

