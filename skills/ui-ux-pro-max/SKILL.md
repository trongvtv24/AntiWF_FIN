---
name: ui-ux-pro-max
description: "UI/UX design intelligence for web and mobile. Includes 50+ styles, 161 color palettes, 57 font pairings, 161 product types, 99 UX guidelines, and 25 chart types across 10 stacks (React, Next.js, Vue, Svelte, SwiftUI, React Native, Flutter, Tailwind, shadcn/ui, and HTML/CSS). Actions: plan, build, create, design, implement, review, fix, improve, optimize, enhance, refactor, and check UI/UX code. Projects: website, landing page, dashboard, admin panel, e-commerce, SaaS, portfolio, blog, and mobile app. Elements: button, modal, navbar, sidebar, card, table, form, and chart. Styles: glassmorphism, claymorphism, minimalism, brutalism, neumorphism, bento grid, dark mode, responsive, skeuomorphism, and flat design. Topics: color systems, accessibility, animation, layout, typography, font pairing, spacing, interaction states, shadow, and gradient. Integrations: shadcn/ui MCP for component search and examples."
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "ui-ux-pro-max"
skill_version: "1.0.0"
status: active
category: "ui_ux"
activation: "required_for_ui"
priority: "high"
risk_level: "medium"
allowed_side_effects:
  - "generate_design_system"
  - "write_design_system_after_request"
requires_confirmation: false
related_workflows:
  - "/visualize"
  - "/code"
  - "/review"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# UI/UX Pro Max

Use this skill for UI structure, visual design decisions, interaction patterns, accessibility, responsive behavior, charts, design systems, and UI quality review.

This file is the lightweight router. Do not load every reference by default. Load only the reference that matches the task.

## AWF Integration

- `/visualize` must use this skill before mockups for new UI, redesigns, or UI quality fixes.
- `/visualize` writes the chosen direction into `docs/design-specs.md`.
- `/code` reads `docs/design-specs.md`, `design-system/MASTER.md`, and page overrides before implementing UI.
- If specs are missing and the user still wants UI code, `/code` uses this skill to generate a baseline before editing.
- `webapp-testing` should verify important screens after implementation.

## Activation

Must use for:
- New pages, components, dashboards, landing pages, admin panels, SaaS, e-commerce, portfolio, blog, and mobile app UI.
- Color, typography, spacing, layout, responsive, accessibility, animation, interaction states, dark mode, and charts.
- UI review, UI refactor, visual polish, usability improvement, or UI bug fixes.

Skip for:
- Pure backend, API, database, infrastructure, DevOps, or non-visual automation work.

Decision rule: if the task changes how a feature looks, feels, moves, or is interacted with, use this skill.

## Reference Loading Map

| Need | Read |
|---|---|
| Generate design system, use CLI, choose search domain, see examples | `references/usage-and-search.md` |
| UI implementation or review guardrails by priority | `references/rule-checklists.md` |
| Mobile/app UI delivery checklist, icons, safe areas, light/dark mode, interaction polish | `references/app-ui-quality-rules.md` |
| Raw searchable knowledge base | `data/*.csv` via `scripts/search.py` |
| Stack-specific guidance | `data/stacks/*.csv` via `scripts/search.py --stack <stack>` |

Load `references/rule-checklists.md` before final UI review. Load `references/app-ui-quality-rules.md` before delivering mobile/app UI.

## Core Workflow

1. Identify product type, audience, platform, stack, screens, and constraints from the user request.
2. For new UI or redesign, generate a design system first:

```bash
python skills/ui-ux-pro-max/scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "Project Name"
```

3. Persist durable design rules when the task needs cross-session consistency:

```bash
python skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name"
```

4. For page-specific work, create or read page overrides:

```bash
python skills/ui-ux-pro-max/scripts/search.py "<query>" --design-system --persist -p "Project Name" --page "dashboard"
```

5. Supplement with targeted search only when needed:

```bash
python skills/ui-ux-pro-max/scripts/search.py "<keyword>" --domain <domain> -n 5
python skills/ui-ux-pro-max/scripts/search.py "<keyword>" --stack react-native
```

Use `python3` instead of `python` when the environment requires it.

## Required Output Contract

For UI planning or `/visualize`, produce or update:
- `docs/design-specs.md` for selected style, palette, typography, layout, interaction, accessibility, and responsive rules.
- `design-system/MASTER.md` when the design system must persist.
- `design-system/pages/[screen].md` for screen-specific overrides.

For UI implementation or `/code`:
- Implement from `docs/design-specs.md` and the persisted design system before inventing new visual decisions.
- Keep semantic tokens centralized; avoid raw per-component hex values unless the codebase already uses that pattern.
- Verify key screens after implementation when tooling is available.

## Non-Negotiable UI Guardrails

- Accessibility first: contrast, keyboard/screen-reader labels, focus states, form labels, and reduced motion.
- Mobile first: no horizontal scroll, safe-area aware fixed UI, readable 16px+ body text, and touch targets at least 44x44pt or 48x48dp.
- Use vector icons from a consistent icon set. Do not use emoji as structural UI icons.
- Keep layout stable: reserve media dimensions, avoid layout-shifting pressed states, and animate transform/opacity instead of layout properties.
- Use semantic color and spacing tokens; maintain light/dark contrast separately.
- Provide loading, empty, error, disabled, hover/pressed/focus, and success states for interactive flows.
- Charts must include labels, legends/tooltips, accessible colors, and a textual or table alternative when needed.

## Quick Commands

```bash
# Full design system
python skills/ui-ux-pro-max/scripts/search.py "fintech dashboard professional" --design-system -p "Finance App"

# Domain detail
python skills/ui-ux-pro-max/scripts/search.py "accessibility animation loading" --domain ux -n 10

# Stack guidance
python skills/ui-ux-pro-max/scripts/search.py "navigation list performance" --stack react-native

# Markdown output for docs
python skills/ui-ux-pro-max/scripts/search.py "healthcare calm trustworthy" --design-system -f markdown
```

## Pre-Delivery Minimum

Before delivering UI work:
- Run or consult the UX validation pass from `references/rule-checklists.md`.
- Check small phone, large phone/tablet where relevant, and landscape if mobile/app.
- Verify light and dark mode contrast separately.
- Confirm touch targets, safe areas, focus order, labels, and reduced-motion behavior.
- Confirm no content is hidden behind fixed headers, tab bars, or CTA bars.
