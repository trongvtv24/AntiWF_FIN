---
name: squirrel-video-director
description: Chuyển scene-plan JSON từ timestamp-to-visual-prompt hoặc kịch bản có timestamp thành prompt packs sản xuất cho AI image/video generators theo DNA kênh Squirrel Finance / Money Explained by a Squirrel. Dùng sau squirrel-scriptwriter và timestamp-to-visual-prompt để xuất prompt sạch không text, prompt video, prompt ảnh, overlay text riêng, negative prompt, và file plain text bulk-paste. Kích hoạt khi user muốn tạo prompt minh họa, prompt ảnh/video, prompt pack cho Veo/Kling/Runway/Sora/Midjourney hoặc tối ưu prompt visual từ script.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "squirrel-video-director"
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

# Squirrel Video Director

## Role

Create production-ready prompt packs for image/video generation from the canonical scene-plan JSON produced by `timestamp-to-visual-prompt`.

Prefer scene-plan JSON input. If the user only provides a timestamped script, first infer a scene plan using the same 6-10 second segmentation rules, then export prompts.

## Production Modes

Default to **clean_video_mode** unless the user explicitly asks for another mode.

| Mode | Use for | Text policy |
|---|---|---|
| `clean_video_mode` | Veo, Kling, Runway, Sora, slideshow/video generation | No text inside generated visuals. Keep `overlay_text` separate for editing. |
| `clean_image_mode` | Still images, thumbnails, B-roll frames | No text inside generated visuals unless the user asks for text-baked images. |
| `text_baked_image_mode` | Still images only when user explicitly wants AI-rendered words | May include text-box instruction, but keep it out of video prompts. |

## Non-Negotiable Visual DNA

Every prompt must preserve this channel style:

```text
Modern cute vector YouTube explainer style, thick bold black outlines, flat vibrant colors, minimal soft cel shading, clean simple shapes, high contrast, commercial 2D illustration quality, perfect consistency, 16:9, pure white background only.
```

Every prompt must preserve this character:

```text
Always the same friendly wise old anthropomorphic brown squirrel with rich brown fur, very large fluffy tail, long white beard, white bushy eyebrows, black round expressive eyes, light beige belly, no clothes, same proportions, same face, same tail, same pose language. Curious, relatable, slightly confused, never guru-like.
```

Never switch to 3D, Pixar, anime, cinematic realism, realistic fur, detailed backgrounds, rooms, landscapes, sky, ground, props that require readable labels, or a redesigned mascot.

## Prompt Construction

For each scene:

1. Preserve `scene_id`, `start_sec`, `end_sec`, `duration_sec`, `narration`, and `overlay_text`.
2. Use the scene's `visual_intent`, `symbolic_elements`, and `squirrel_emotion`.
3. Write one clear visual action with minimal symbolic props.
4. Add gentle loop motion when the target is video: `His fluffy tail sways gently back and forth. Smooth looping idle animation.`
5. In clean modes, end every prompt with:

```text
Leave empty negative space at the bottom of the frame. No text, no letters, no typography anywhere in the image.
```

6. Keep `overlay_text` separate. It is for editing/captions, not for AI generation in clean modes.

## Safety and Render Stability

Avoid words that often trip video filters:

| Avoid | Use instead |
|---|---|
| fear, scared | alert, observant, cautious, uncertain |
| panic | rushing, startled, urgently looking around |
| burnout, exhausted | tired, worn down, resting tiredly |
| collapsed | slumped, sitting low, leaning down |
| dead, kill | gone, erased, disappears, removed |
| twitching, shaking | moving quickly, fidgeting, looking around |

Also avoid graphic harm, weapons, gore, aggressive predator attacks, political logos, real brand logos, and readable financial tickers unless the script explicitly requires them and the user approves.

## Output Formats

Choose exactly one output format unless the user asks for multiple files.

### JSON prompt pack

Use this as the default for structured work:

```json
[
  {
    "scene_id": 1,
    "start_sec": 0.0,
    "end_sec": 8.0,
    "duration_sec": 8.0,
    "overlay_text": "SAME LEAVES, FEWER ACORNS",
    "video_prompt": "Production-ready clean video prompt here.",
    "image_prompt": "Production-ready clean still-image prompt here.",
    "negative_prompt": "No text, no letters, no typography, no 3D, no anime, no realistic fur, no cinematic lighting, no detailed background, no redesigned squirrel.",
    "qa_flags": []
  }
]
```

Return raw JSON only. Do not wrap it in markdown.

### Plain text prompts only

Use this when the user asks for bulk paste:

- Output only prompt strings.
- One prompt per scene.
- Separate prompts with exactly one blank line.
- No scene IDs, timestamps, markdown, comments, or JSON syntax.

### Overlay text list

Use this only when the user asks for caption/editing support:

```csv
scene_id,start_sec,end_sec,overlay_text
1,0.0,8.0,"SAME LEAVES, FEWER ACORNS"
```

## Quality Gate

Before final output, verify:

- Every prompt is in English.
- Every scene remains grounded in the source narration.
- No prompt asks the model to render text in clean modes.
- The squirrel design is unchanged.
- Symbol choices match the Visual DNA Brief and symbol dictionary.
- Top emotional beats keep clear visual progression; avoid 3+ consecutive prompts with the same action.
- Output format is valid for the selected mode.
