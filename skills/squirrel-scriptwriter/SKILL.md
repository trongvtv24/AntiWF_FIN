---
name: squirrel-scriptwriter
description: "YouTube scriptwriter for Squirrel Finance channel. Writes brand-consistent scripts (8-15 min) using the squirrel/acorn/golden-leaf metaphor system. Auto-researches data from the internet, generates outlines and full long-form scripts, AI image prompts, thumbnails, descriptions, tags, and sequel hooks. Trigger: /script command, or when user mentions writing scripts, kịch bản, screenplay for Squirrel Finance. Follows the 9-part script formula from Brand Bible with retention beats every 20-40 seconds."
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

### Phase 5: AI Visual Prompts 🎨 (For Image & Video Generators)

After the script is approved, generate Google Banana AI visual prompts for the entire video:

**🔥 CRITICAL AI RULE (PREVENT AI BIAS)**:
Even if the user asks for "Video Prompts" (instead of Image Prompts) to use in Kling, Sora, or Runway, you **MUST** strictly use the EXACT SAME 2D Vector Base Prompt below. NEVER switch to "3D", "Cinematic", or "Pixar" styles to optimize for video AI. It MUST be pure white background vector cartoon only.

#### Base Prompt (ALWAYS start every scene prompt with EXACTLY this):
```
Modern cute vector YouTube explainer style, thick bold black outlines, flat vibrant colors, minimal soft cel shading, clean simple shapes, whimsical friendly design, high contrast, commercial 2D illustration quality, perfect consistency, 16:9. Pure white background only, no scenery, no sky, no ground, no room, no landscape, no decorative elements, no environment details. Only the main character and minimal symbolic explainer objects. Main character: ALWAYS the same friendly wise old anthropomorphic brown squirrel with rich brown fur, very large fluffy tail, long white beard, white bushy eyebrows, black round expressive eyes, light beige belly, no clothes, same exact proportions, face, tail, pose language, and expression logic, never redesigned. The squirrel is curious, relatable, slightly confused, never guru-like. Fixed symbols: acorn = assets/value, golden leaves = money, oak tree = long-term growth, nest = home/stability, Forest Bank = banks/credit. No 3D, anime, realistic fur, painterly textures, cinematic lighting, detailed backgrounds, or visual drift.
```

#### Scene Prompt Rules & Generation Logic (MANDATORY):
1. **Timing Constraint (8-10 Seconds/Clip):** You MUST generate 1 prompt for EXACTLY every 8-10 seconds of the script (roughly every 15-20 words). For a 10-minute video, you must generate around 60-75 prompts. Ensure no overlap/double-counting when looping.
2. **Visual Action Continuity:** Change the action logic/emotion dynamically based on the script, but NEVER change the squirrel's design. If the script discusses "Debt", the squirrel should sweat holding a "DEBT" weight. If it discusses "Panic", the squirrel runs frantically. Avoid repeating the exact same action too sequentially unless appropriate.
3. **Emotional Typography Overlay (CRITICAL):** For EVERY prompt, you MUST extract the 1-3 most emotionally impactful or important words from that specific audio chunk to display as bold typography.
   - *Example:* If the script says "Why would anyone buy something simply because they believe another person will pay more for it tomorrow?", the extracted typography should be `"PAY MORE?"`.
   - **VEO/AI Text Hack:** You MUST always put the text in exact double quotes and append font instructions. AI video models struggle with text unless explicitly constrained.
4. **Prompt Assembly Strategy:** Append the Action and Typography to the Base Prompt exactly like this:
   `[Base Prompt] Specific Scene: [Action description without background details], with a bold white text box at the bottom that says exactly "[EXTRACTED WORDS]", clear typography, sans-serif font.`

#### Output Format:
Provide the final prompts as raw text. Do NOT include any markdown quotes, bolding, `[MM:SS]` timestamps, or scene headings between lines. Just output a continuous block of plain texts, separated from each other by EXACTLY **one empty line** (for easy bulk copy-paste).

### Phase 5.5: Prompt Alignment Review 🔍 (MANDATORY — Do NOT skip)

After generating all prompts in Phase 5, you MUST run a full alignment audit **before saving the file**. This phase ensures every prompt is honestly grounded in the script.

#### Step 1: Cross-Reference Every Prompt Against the Script

For EACH generated prompt, check the following three criteria:

| # | Check | Rule |
|---|-------|------|
| 1 | **Scene grounding** | The visual action described in the prompt must correspond to a real moment, idea, or emotion in that section of the script. A prompt must NOT invent content the script did not say. |
| 2 | **Typography validity** | The bold text overlay ("EXTRACTED WORDS") must pass at least ONE of these three tests: (A) The exact words appear in the script near that timestamp, OR (B) The words are a direct conceptual summary of what the script is saying at that moment, OR (C) The words create a clear emotional trigger (curiosity, surprise, relief, tension) that amplifies viewer retention — without misrepresenting the script's message. |
| 3 | **No phantom content** | The prompt must NOT visualize statistics, concepts, or comparisons that the script does not mention at all. Common phantom content errors: adding % figures not in the script, referencing rules-of-thumb not stated by the narrator, inserting comparison frames the script never sets up. |

#### Step 2: Coverage Check — Are All Key Script Moments Covered?

After reviewing individual prompts, check coverage at the script level:

1. Read through the full script from start to finish.
2. Identify the **top 5–8 most emotionally impactful or conceptually critical moments** (e.g., the twist, the wealth gap reveal, the "if you only remember one thing" line).
3. Confirm that EACH of those moments has a corresponding prompt. If any is missing, add a new prompt for it.
4. Check for **over-clustering** — if 3+ consecutive prompts illustrate the same idea with no visual progression, consolidate or replace with a more dynamic scene.

#### Step 3: Fix & Flag

For every prompt that fails any check in Step 1 or Step 2:

- **Delete it** if it visualizes content not in the script.
- **Rewrite it** if the typography is misaligned or invented. Replace with words/phrases that are either: (A) directly from the script, or (B) emotionally resonant summaries with a clear trigger hook.
- **Add missing prompts** for any uncovered critical moments identified in Step 2.
- Annotate each fixed prompt with `[REVISED: reason]` inline — then remove the annotation after the full list is finalized.

#### Step 4: Final Alignment Score

After all fixes, output a brief summary:

```
ALIGNMENT REVIEW SUMMARY
Total prompts generated: [N]
Prompts revised: [N]
Prompts added: [N]
Prompts removed: [N]
Critical script moments covered: [N/N]
Typography issues fixed: [N]
Phantom content removed: [N]
Final verdict: APPROVED / NEEDS REVISION
```

Only proceed to Phase 6 if the final verdict is **APPROVED**.

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

Prompt Alignment checks (Phase 5.5):
| # | Check | Pass? |
|---|-------|-------|
| 18 | Phase 5.5 Alignment Review completed and verdict is APPROVED? | |
| 19 | Every prompt's visual action corresponds to an actual script moment (no phantom content)? | |
| 20 | Every typography overlay either quotes the script, summarizes it accurately, or delivers a clear emotional trigger? | |
| 21 | All top 5–8 critical/emotional script moments have a dedicated prompt? | |

---

## Output Delivery Order

When the workflow is complete, deliver files in this order:

1. **`[Topic]_Outline.md`** — Plain text outline (Phase 3)
2. **`[Topic]_Script.md`** — Full long-form script (Phase 4)
3. **`[Topic]_AI_Prompts.md`** — AI image prompts for every scene (Phase 5)
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
