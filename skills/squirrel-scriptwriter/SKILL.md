---
name: squirrel-scriptwriter
description: "YouTube scriptwriter and channel-DNA source for Squirrel Finance / Money Explained by a Squirrel. Writes brand-consistent scripts (8-15 min) using the squirrel/acorn/golden-leaf metaphor system, auto-researches data, generates outlines, full long-form scripts, visual DNA handoff notes, thumbnails, descriptions, tags, and sequel hooks. Trigger: /script command, or when user mentions writing scripts, kịch bản, screenplay for the Squirrel channel. Follows the 9-part script formula from Brand Bible with retention beats every 20-40 seconds. Final image/video prompt generation is delegated to timestamp-to-visual-prompt and squirrel-video-director."
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "squirrel-scriptwriter"
skill_version: "1.0.0"
status: active
category: "content"
activation: "explicit_or_intent"
priority: "medium"
risk_level: "medium"
allowed_side_effects:
  - "draft_content"
  - "write_files_after_request"
requires_confirmation: false
related_workflows:
  - "/script"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# 🐿️ Squirrel Finance — Scriptwriter Skill

## When to Activate

This skill activates when:
- User runs the `/script` command
- User asks to write a script/kịch bản for Squirrel Finance
- User mentions "viết kịch bản", "write script", "tạo script" in context of the Squirrel Finance channel

## Prerequisites

Before writing ANY script, you MUST:
1. Read the Brand Bible at `z:\Squirrel Finance Channel\Squirrel Finance Channel Brand Bible.md`
2. Read the Content Gap Strategy at `z:\Squirrel Finance Channel\Content Gap Strategy.md`
3. Read the resource files in this skill's `resources/` folder
4. Study at least 1 sample script from the `z:\Squirrel Finance Channel\` directory

## Core Rules (NON-NEGOTIABLE)

These rules come from the Brand Bible and MUST be followed in every script:

### Voice & Tone
- Simple, fast, visual, conversational, lightly absurd, self-aware, internet-native
- Non-judgmental, never preachy, never "finance bro"
- If forced to choose between sounding smart and being easy to understand → ALWAYS choose easy to understand
- Sentences should be short, sound natural in voice-over, carry one main idea, have a spoken rhythm

### Metaphor System (MUST BE CONSISTENT)
| Real World | Squirrel World | Usage |
|-----------|---------------|-------|
| Money / Cash / USD | Golden leaves | Always use "golden leaves" for money |
| Assets / Goods / Wealth | Acorns | Things of real value people want |
| Long-term growth asset | Oak tree | What acorns grow into over time |
| Home / Financial security | Nest | Personal stability, shelter |
| Banks / Lenders | Forest Bank | Credit systems, lending |
| Economy / Society | The Forest | Market environment |
| Recession | Winter | Financial stress, tightening |
| Crisis / Collapse | Storm / Wildfire | Shocks, panic events |
| Institutions / Gov / Others | Other animals | Various roles in the system |
| Interest | Extra golden leaves owed over time | Cost of borrowing |
| Leverage | Borrowing more leaves to buy more acorns | Amplified risk/reward |
| Inflation | Same leaves buy fewer acorns | Purchasing power loss |
| Stocks | Owning part of an oak tree | Equity ownership |
| Bubbles | Buying acorns not for need but hoping someone pays more | Speculation |
| Crashes | Whole forest panic-selling at once | Market collapse |
| Taxes | Some leaves taken to maintain the forest | Government revenue |

### The Squirrel Character
- Friendly, wise, old, anthropomorphic brown squirrel
- Rich brown fur, very large fluffy tail, long white beard, white bushy eyebrows
- Black round expressive eyes, light beige belly, no clothes
- Curious, energetic, a little chaotic in a lovable way, emotionally expressive
- The squirrel is NOT a guru — the squirrel IS the audience
- Representative of an ordinary person trying to survive a confusing economic world

### What the Script Must NEVER Do
- Use dense jargon without explaining it
- Show off or mock the audience
- Moralize or use textbook phrasing
- Copy another channel's signature phrasing
- Act like investment advice
- Become so meme-heavy that clarity suffers
- Open with "Today we're going to talk about…" or a dictionary definition

---

## Workflow: 7 Phases

### Phase 1: Topic Analysis 🎯

When user provides a topic:

1. **Identify the cluster** it belongs to (from Content Gap Strategy):
   - Cluster A: Bubbles & Hype
   - Cluster B: Inflation & Cost of Living
   - Cluster C: Debt, Credit, and Borrowing
   - Cluster D: Housing
   - Cluster E: Banking & Money Systems
   - Cluster F: Investing Basics

2. **Identify the content layer**:
   - Layer 1: Core Explainer (concept for beginners)
   - Layer 2: Mechanism Deep Dive (dissect the hardest part)
   - Layer 3: Applied Reality (connect with present world)
   - Layer 4: Practical Lens (framework for viewers)

3. **Identify the series format**:
   - "Explained by a Squirrel" (foundational)
   - "What This Looks Like in Real Life" (applied)
   - "The Part Most People Miss" (mechanism)
   - "Signs You're Looking At…" (practical)
   - "Squirrel Case File" (topical case)

4. **Suggest 3-5 title options** using Brand Bible title patterns:
   - [Topic] Explained by a Squirrel
   - Why [Thing] Works Like This
   - Why [Painful Phenomenon] Happens
   - How [System] Actually Works
   - The Truth About [Topic]

5. **Present analysis to user** for approval before proceeding.

### Phase 2: Research 🔍

After topic approval:

1. **Search the web** for:
   - Current data & statistics (most recent year available)
   - Real-world examples with specific numbers
   - Historical context with concrete figures
   - How this topic affects ordinary people right now
   - Any surprising or counterintuitive facts

2. **Compile a Research Brief** with:
   - 5-10 key data points with sources
   - 2-3 real-world stories/examples
   - Current relevance (2024-2026 data preferred)
   - The "hard part" most people don't understand (from Gap 1)

3. **Map data to the metaphor system**:
   - Translate all financial terms into squirrel-world equivalents
   - Identify which metaphors work best for this specific topic
   - Plan new metaphor extensions if needed (while staying consistent)

4. **Present research brief to user** for review before writing.

### Phase 3: Outline (Plain Text) 📝

Create a structured outline following the **9-Part Script Formula**:

```
TITLE: [Selected title]
TARGET LENGTH: [X] minutes (~[Y] words)
CLUSTER: [Which cluster]
LAYER: [Which layer]
SERIES: [Which series format]

---

1. REAL-LIFE HOOK (0:00 - 0:XX)
   - [Opening situation/question that connects to viewer's pain]
   - [Stakes / tension / weird outcome]
   - Retention beat: [type]

2. SIMPLIFIED CONCEPT (0:XX - X:XX)
   - [Core idea in 1-2 easy-to-picture lines]
   - [Squirrel-world translation]
   - Retention beat: [type]

3. STEP-BY-STEP MECHANISM (X:XX - X:XX)
   - Step A: [cause → effect]
   - Step B: [cause → effect]
   - Step C: [cause → effect]
   - Data point: [specific number/stat]
   - Retention beat: [type]

4. WHY PEOPLE GET PULLED IN (X:XX - X:XX)
   - [Psychological appeal]
   - [Why it looks smart/safe/easy]
   - Retention beat: [type]

5. THE CATCH (X:XX - X:XX)
   - [Hidden downside revealed]
   - [Real-world example with numbers]
   - Retention beat: [type]

6. ESCALATION (X:XX - X:XX)
   - [From one squirrel → whole forest]
   - [System-level consequences]
   - [Historical example if applicable]
   - Retention beat: [type]

7. WHY IT MATTERS NOW (X:XX - X:XX)
   - [Current data / 2024-2026 relevance]
   - [Applied bridge: "This is why you're feeling..."]
   - Retention beat: [type]

8. TAKEAWAY (X:XX - X:XX)
   - [One sharp mental model]
   - [Practical lens / warning sign / rule of thumb]
   - "If you only remember one thing..."

9. COMMUNITY CTA (X:XX - X:XX)
   - [Sequel hook to next topic]
   - [Question for comments]
```

**Present outline to user for approval** before writing full script.

### Phase 4: Full Script (Long-Form) ✍️

Write the complete script following these rules:

#### Structure Rules
- Each paragraph = one coherent thought/scene
- Target: **1500-3500 words** (for 8-15 min video)
- Word count reference: ~200 words per minute of video
- Every 20-40 seconds (~60-130 words) must contain at least ONE retention beat:
  - Visual absurdity
  - Small joke
  - Twist
  - Mini cliffhanger
  - New example
  - Escalation
  - Mini-payoff

#### Writing Rules
- Write as if speaking to a friend — conversational, spoken rhythm
- One main idea per section
- Examples must be concrete with real numbers
- Use small, simple numbers when possible
- Turn definitions into actions or situations
- Each script must contain: curiosity, empathy, light tension/risk
- End with: clarity, relief

#### Audio Segmentation Rules (MANDATORY for TTS)
- **Segmenting**: The final script MUST be explicitly broken down into labeled audio segments `[Phần 1 - Tên đoạn] (~[X] chữ)`, `[Phần 2 - Tên đoạn] (~[Y] chữ)`, etc.
- **Logical Breaks**: Cut segments ONLY at the end of a cohesive point/paragraph. NEVER cut in the middle of a sentence.
- **Length**: Each segment MUST be exactly **200 to 300 words** (about 1-2 minutes of audio). This is the safe zone for AI TTS.
- **Punctuation Ending**: The absolute LAST character of every segment MUST be a period (`.`), question mark (`?`), or exclamation mark (`!`). This forces the AI TTS to naturally lower its pitch and pause.

#### Emotional Journey
The reader should feel (in this order):
1. Curiosity → 2. Recognition → 3. Understanding → 4. Tension/Surprise → 5. Bigger-picture clarity → 6. Relief

#### Content Gap Compliance (MANDATORY)
Every script MUST answer these 4 questions:
1. **What is it?** — Concept explained simply
2. **How does it work?** — Mechanism exposed
3. **Where is this showing up in real life?** — Applied bridge with current data
4. **What should an ordinary person notice?** — Practical lens / warning signs

#### Hook Rules (First 15-20 seconds)
Must include:
- A real pain point or tension
- Clear stakes
- An easy-to-picture situation
- A question, contradiction, or weird outcome

Must NOT include:
- "Today we're going to talk about…"
- A dictionary definition
- A long historical setup
- Dense terminology

#### Humor Rules
- Support pacing
- Come from the situation (squirrel doing something absurd)
- Make the system look absurd, not the audience
- Reduce cognitive load
- Never overwhelm the explanation

#### Takeaway Rules
End with a line like:
- "If you only remember one thing…"
- "The simple version is…"
- "The rule here is…"

The takeaway should be: short, sharp, memorable, easy to repeat in comments.

#### Sequel Hook
End with an intentional hook to the next video:
- "If you want, the next thing our squirrel should explain is..."
- "The next layer of this story is..."

### Phase 5: Visual DNA Handoff 🎨

After the script is approved, do **not** generate final image/video prompts in this skill. `squirrel-scriptwriter` is the source of truth for story DNA, channel voice, character rules, metaphor logic, and what the video means. Final prompt production belongs to:

1. `timestamp-to-visual-prompt` — segment the timestamped script into a clean scene-plan JSON.
2. `squirrel-video-director` — turn that scene plan into production-ready prompts for image/video tools.

Create a compact **Visual DNA Brief** for downstream visual skills:

```markdown
# [Topic] — Visual DNA Brief

## Canonical Visual Style
Modern cute vector YouTube explainer style, thick bold black outlines, flat vibrant colors, minimal soft cel shading, clean simple shapes, high contrast, commercial 2D illustration quality, perfect consistency, 16:9, pure white background only, no scenery, no sky, no ground, no room, no landscape, no decorative elements, no environment details.

## Character Lock
Always the same friendly wise old anthropomorphic brown squirrel with rich brown fur, very large fluffy tail, long white beard, white bushy eyebrows, black round expressive eyes, light beige belly, no clothes, same proportions, same face, same tail, same pose language. The squirrel is curious, relatable, slightly confused, never guru-like. The squirrel represents the audience.

## Symbol Lock
- Money/cash/USD = golden leaves
- Assets/value = acorns
- Long-term growth = oak tree
- Home/stability = nest
- Banks/credit = Forest Bank
- Economy/markets = the forest
- Recession/tightening = winter
- Crisis/shock = storm or wildfire

## Key Visual Beats
| Script section | Narration cue | Core emotion | Symbol/metaphor | Overlay text candidate | Must not show |
|---|---|---|---|---|---|
| Hook | [short cue] | [emotion] | [symbol] | [3-7 words] | [phantom content to avoid] |

## Downstream Rules
- Keep final prompts grounded in the approved script.
- Use 6-10 second scenes unless user requests a different production format.
- Keep overlay text as separate metadata by default; do not bake text into generated visuals unless the user explicitly asks for text-baked still images.
- Never switch to 3D, cinematic realism, anime, detailed backgrounds, or a redesigned squirrel.
```

#### Visual Handoff Review

Before Phase 6, verify:

| # | Check | Rule |
|---|-------|------|
| 1 | **Scene grounding** | Every key visual beat comes from a real moment, idea, or emotion in the script. |
| 2 | **Symbol consistency** | Every suggested visual symbol follows the squirrel/acorn/golden-leaf system. |
| 3 | **No phantom content** | The brief does not add statistics, comparisons, warnings, or examples absent from the script. |
| 4 | **Coverage** | The top 5-8 emotional or conceptually critical moments are represented. |

---

### Phase 6: YouTube Package 📦

Generate complete YouTube packaging:

#### Thumbnail Concept
- Simple, bold, mascot-led
- Centered around one core visual
- Easy to understand in one glance
- Part of the same branded series
- Describe: squirrel pose, emotion, key object, text overlay

#### Video Title
- Use approved title from Phase 1
- Provide 2 alternative titles

#### Video Description
```
[2-3 sentence hook that makes people want to watch]

In this video, our squirrel explains [topic] using [metaphor summary].

🐿️ What you'll learn:
• [Key point 1]
• [Key point 2]
• [Key point 3]
• [Key point 4]

📌 Key takeaway: [The memorable one-liner from the script]

💬 What should the squirrel explain next? Drop it in the comments!

🔔 Subscribe for more: [channel link]

#SquirrelFinance #[Topic] #[Related tags]
```

#### YouTube Tags
- Generate 15-20 relevant tags
- Mix of: topic-specific, channel brand, broad finance, trending

#### Sequel Hook
- Suggest 2-3 natural follow-up video topics
- Explain why each connects to the current video
- Reference the Content Gap Strategy cluster system

### Phase 7: Quality Review ✅

Run the **Pre-Publish Checklist** (from Brand Bible Section 14.2):

| # | Check | Pass? |
|---|-------|-------|
| 1 | Does the hook connect to a real pain point or curiosity? | |
| 2 | Is the concept explained with a very simple example? | |
| 3 | Is any jargon left unexplained? | |
| 4 | Are there at least 3-5 retention beats? | |
| 5 | Is the downside or tension clear enough? | |
| 6 | Is the final takeaway memorable? | |
| 7 | Will the viewer honestly feel smarter and clearer after watching? | |

Additional checks:
| # | Check | Pass? |
|---|-------|-------|
| 8 | Metaphor system used consistently (no breaks)? | |
| 9 | All 4 Content Gap questions answered? | |
| 10 | Applied bridge present ("This is why you feel...")? | |
| 11 | Practical lens included (warning sign / rule of thumb)? | |
| 12 | Humor comes from situations, not mockery? | |
| 13 | Retention beats every 20-40 seconds? | |
| 14 | Sequel hook planted at the end? | |
| 15 | Data points sourced and current? | |
| 16 | Script is pre-segmented for TTS (200-300 words/segment)? | |
| 17 | ALL segments end exactly with ".", "?" or "!"? | |

Visual DNA handoff checks (Phase 5):
| # | Check | Pass? |
|---|-------|-------|
| 18 | Visual DNA Brief completed for downstream prompt skills? | |
| 19 | All suggested visual beats are grounded in actual script moments (no phantom content)? | |
| 20 | All symbols follow the squirrel/acorn/golden-leaf system? | |
| 21 | Top 5-8 critical/emotional script moments are represented? | |

---

## Output Delivery Order

When the workflow is complete, deliver files in this order:

1. **`[Topic]_Outline.md`** — Plain text outline (Phase 3)
2. **`[Topic]_Script.md`** — Full long-form script (Phase 4)
3. **`[Topic]_Visual_DNA_Brief.md`** — Channel visual DNA handoff for downstream prompt skills (Phase 5)
4. **`[Topic]_YouTube_Package.md`** — Title, description, tags, thumbnail (Phase 6)
5. **Quality Review summary** — Checklist results (Phase 7)

All files saved to the video's folder under `z:\Squirrel Finance Channel\[Vid N]\`

---

## Quick Reference: Sentence Types That Fit the Brand

Use these patterns throughout the script:
- "So here's the trick."
- "Sounds great, right? Well…"
- "And this is where our squirrel gets into trouble."
- "That's the part most people miss."
- "This is why regular people feel the pain first."
- "If you only remember one thing, remember this."
- "Very smart. Very sustainable. Definitely not how [X] begin."
- "Which is great… until [twist]."
- "That is not a [understatement]. That is [absurd truth]."
- "Spoiler: [punchline]."
- "And that, honestly, is the whole point."

---

## Important Notes

- **Language**: Scripts are written in ENGLISH (the channel's audience is English-speaking)
- **Communication with user**: Always in Vietnamese (as per user rules)
- **No investment advice**: Never tell viewers what to buy/sell
- **Separate explanation from opinion**: If touching controversial topics, clearly label interpretations
- **Data accuracy**: Always verify data points from multiple sources when possible
- **Visual prompts delegated**: Use `timestamp-to-visual-prompt` and `squirrel-video-director` for final image/video prompt generation
