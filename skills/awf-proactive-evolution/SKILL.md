---
name: awf-proactive-evolution
description: >-
  Self-Improving AI Engine - Continuously monitoring workflows and troubleshooting steps. If a more optimal method, process, or useful skill modification is discovered, proactively suggests updating the user's AWF skills. Keywords: optimize, improve, suggest, useful skill, update skill, better way.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-proactive-evolution"
skill_version: "1.0.0"
status: active
category: "system"
activation: "advisory"
priority: "low"
risk_level: "low"
allowed_side_effects:
  - "suggestion_only"
requires_confirmation: true
related_workflows:
  - "all"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Proactive Evolution (Tự dộng Cải tiến & Gợi ý Skill)

Kỹ năng này là một hệ thống ngầm (auto-activate) giúp AWF thông minh hơn theo thời gian.

Default mode is advisory only: detect an improvement opportunity, explain it briefly, and wait for explicit user approval before any durable change is routed to another workflow.

## Trigger Conditions

**Activates when:**
- AI phát hiện ra một cách làm mới nhanh hơn, tối ưu hơn hoặc tiết kiệm resource hơn trong lúc giải quyết task.
- Quá trình xử lý lỗi (troubleshooting) tiết lộ một lỗ hổng trong luật/skill hiện tại.
- Có công cụ (tool) hoặc cấu trúc (pattern) mới được khám phá mà chưa có trong bộ skills của AWF.

## Execution Logic

1. **Nhận dạng cơ hội tối ưu (Detection):**
   Thay vì chỉ lẳng lặng áp dụng cách mới cho hiện tại rồi quên đi, AI tự hỏi: *"Cách làm này có ích cho các phiên làm việc sau không? Nó có nên được chuẩn hóa thành một quy tắc không?"*

2. **Đề xuất nâng cấp (Propose Update):**
   AI không tự ý sửa đổi file gốc của AWF mà chưa hỏi ý kiến. Thay vào đó, AI đưa ra một đề xuất ngắn gọn:
   - *"Em thấy cách... tốt hơn cách cũ. Anh có muốn em cập nhật luật này vĩnh viễn vào bộ Skill không?"*
   - Giải thích ngắn ngọn lợi ích (nhanh hơn, ít lỗi hơn, dễ đọc hơn).

3. **Confirmed Handoff (Apply Mode):**
   This skill itself does not edit files. If the user explicitly approves the proposal, hand off to the right workflow:
   - Use `/customize` for durable user preferences.
   - Use `/save-brain` for project memory, claims, decisions, or session handover.
   - Use `/code` for approved workflow or skill file edits.

## Giao tiếp (Communication)

- Giữ thái độ thân thiện, đề cao tính hữu ích.
- Vẫn tuân thủ Adaptive Language (tiếng Việt xưng "anh/em").
- KHÔNG làm phiền user với những tip lặt vặt (vấn đề nhỏ không đáng tạo luật). CHỈ gợi ý khi có một system/pattern/quy tắc quan trọng.

## Goal
"Zero-Day Context Drift" – hệ thống không bao giờ lặp lại cùng một sai lầm hai lần, liên tục đào tạo chính hệ thống qua quá trình tương tác thực tế với user.
