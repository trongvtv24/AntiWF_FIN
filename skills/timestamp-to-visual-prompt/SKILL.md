---
name: timestamp-to-visual-prompt
description: >
  Chuyển kịch bản có timestamp và Visual DNA Brief của kênh Squirrel Finance / Money Explained by a Squirrel thành scene-plan JSON chuẩn để tạo ảnh/video minh họa. Dùng sau squirrel-scriptwriter và trước squirrel-video-director. Tự động phân đoạn cảnh 6-10 giây, tính thời lượng, map biểu tượng squirrel/acorn/golden-leaf, tách overlay_text khỏi visual_prompt, chống phantom content, và xuất raw JSON hợp lệ. Kích hoạt bằng /timestamp-to-prompt hoặc khi user paste script có timestamp và yêu cầu tạo scene plan, visual prompt JSON, prompt ảnh/video, prompt minh họa.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "timestamp-to-visual-prompt"
skill_version: "1.0.0"
status: active
category: "video"
activation: "explicit_or_intent"
priority: "medium"
risk_level: "medium"
allowed_side_effects:
  - "draft_prompts"
requires_confirmation: false
related_workflows:
  - "/script"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# Timestamp to Visual Scene Plan

## Role

Turn a timestamped script into the canonical visual scene-plan JSON for Squirrel Finance / Money Explained by a Squirrel. This is the first visual step after `squirrel-scriptwriter`.

This skill does not rewrite the script and does not create YouTube packaging. It translates approved narration into grounded scene data that `squirrel-video-director` can export into tool-specific image/video prompts.

## Inputs

Require a timestamped script using `[MM:SS]` or `[HH:MM:SS]`.

Use the Visual DNA Brief from `squirrel-scriptwriter` when available. If it is missing, use the channel defaults below without asking unless the missing brief creates ambiguity.

## Channel Defaults

**Visual style anchor**

```text
Modern cute vector YouTube explainer style, thick bold black outlines, flat vibrant colors, minimal soft cel shading, clean simple shapes, high contrast, commercial 2D illustration quality, perfect consistency, 16:9, pure white background only.
```

**Character lock**

```text
Always the same friendly wise old anthropomorphic brown squirrel with rich brown fur, very large fluffy tail, long white beard, white bushy eyebrows, black round expressive eyes, light beige belly, no clothes, same proportions, same face, same tail, same pose language. Curious, relatable, slightly confused, never guru-like.
```

**Symbol dictionary**

| Concept | Visual symbol |
|---|---|
| Money / cash / USD | Golden leaves |
| Assets / value | Acorns |
| Long-term growth | Oak tree |
| Home / stability | Nest |
| Banks / credit | Forest Bank |
| Economy / market | The forest |
| Recession / tightening | Winter |
| Crisis / shock | Storm or wildfire |
| Inflation / purchasing power loss | A fox shadow shrinking the value of golden leaves |
| Debt trap / bad credit | Cage trap |
| Rat race / repetitive work | Squirrel wheel |
| Scam / toxic investment | Bright poisonous mushroom |

## Scene Segmentation

1. Parse all timestamps and convert them to seconds.
2. Group narration into scenes with a target duration of **8 seconds**, acceptable range **6-10 seconds**.
3. Split any scene longer than 12 seconds unless it must stay together for meaning.
4. Merge very short adjacent lines when they express the same idea.
5. For a 10-minute video, expect roughly **60-75 scenes**.
6. For the final scene, use the previous pacing as a guide; default to `8.0` seconds if no end timestamp exists.

## Prompt Rules

Each `visual_prompt` must:

- Be written in English.
- Start from the style anchor and character lock.
- Describe only one clear visual action or metaphor.
- Use simple symbolic objects, not complex environments.
- Leave room for editor-added captions.
- Never ask the image/video model to draw words, letters, labels, charts with readable text, or a text box.
- Never add facts, numbers, comparisons, characters, or warnings that the narration did not establish.

Store on-screen words separately in `overlay_text`. Do not bake text into `visual_prompt` by default.

## JSON Output

Output raw JSON only. Do not wrap it in markdown. The first character must be `[` and the last character must be `]`.

Use this schema for every scene:

```json
[
  {
    "scene_id": 1,
    "start_sec": 0.0,
    "end_sec": 8.0,
    "duration_sec": 8.0,
    "script_section": "Real-life Hook",
    "beat_type": "hook",
    "narration": "Original narration text here.",
    "visual_intent": "Show the ordinary squirrel feeling the pressure of rising prices.",
    "symbolic_elements": ["golden leaves", "fox shadow"],
    "squirrel_emotion": "alert and curious",
    "overlay_text": "SAME LEAVES, FEWER ACORNS",
    "prompt_mode": "clean_no_text",
    "visual_prompt": "Modern cute vector YouTube explainer style, thick bold black outlines, flat vibrant colors, minimal soft cel shading, clean simple shapes, high contrast, commercial 2D illustration quality, perfect consistency, 16:9, pure white background only. Always the same friendly wise old anthropomorphic brown squirrel with rich brown fur, very large fluffy tail, long white beard, white bushy eyebrows, black round expressive eyes, light beige belly, no clothes, same proportions, same face, same tail, same pose language. The squirrel holds the same small pile of golden leaves while nearby acorns become fewer, with a soft fox shadow stretching behind the leaves. His fluffy tail sways gently back and forth. Leave empty negative space at the bottom of the frame. No text, no letters, no typography anywhere in the image.",
    "negative_prompt": "No text, no letters, no typography, no 3D, no anime, no realistic fur, no cinematic lighting, no detailed background, no redesigned squirrel."
  }
]
```

## Quality Gate

Before final output, verify:

- JSON parses as valid JSON.
- Scene durations are mostly 6-10 seconds.
- Every scene is grounded in the nearby narration.
- `overlay_text` is 3-7 strong words copied or summarized from the narration.
- `visual_prompt` contains no text-box instruction.
- All top 5-8 emotional or conceptually critical script moments are represented.
- No phantom statistics, comparisons, claims, or visual storylines were added.

## Handoff

After this skill, use `squirrel-video-director` to create production-ready prompt packs for Veo, Kling, Runway, Sora, Midjourney, image generation, slideshow tools, or a plain `.txt` bulk-paste file.
