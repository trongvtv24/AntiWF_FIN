---
name: awf-auto-save
description: >-
  Eternal Context System - Auto-save session to prevent context loss.
  Triggers: workflow end, user leaving, decisions, periodic checkpoint.
  Warns when context is getting full.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-auto-save"
skill_version: "1.0.0"
status: active
category: "context"
activation: "automatic"
priority: "high"
risk_level: "medium"
allowed_side_effects:
  - "write_context_checkpoint"
requires_confirmation: false
related_workflows:
  - "/save-brain"
  - "/code"
  - "/visualize"
  - "/plan"
required_gates:
  - "global_safety_truthfulness_gate"
  - "context_system"
# AWF_METADATA_END
---

# AWF Auto-Save (Eternal Context v4.0)

Tự động lưu checkpoint nhẹ để không mất ngữ cảnh giữa các workflow hoặc session.

## Context System Boundary (AWF 4.0)

Skill này tuân thủ `global_workflows/CONTEXT_SYSTEM.md`.

- Được append checkpoint nhẹ vào `.brain/session_log.txt`.
- Được update các field hẹp trong `.brain/session.json`: `summary`, `working_on`, `current_plan_path`, `current_phase`, `pending_tasks`, `recent_changes`, `errors_encountered`, `skipped_tests`, `last_run`, `handover_required`.
- Không được tự ghi `brain.json` trừ khi `/save-brain` đang chạy.
- Không được tự ghi note/ADR/decision bền vững; việc đó thuộc `/save-brain` hoặc `awf-note-taking` sau khi user xác nhận.
- Claim chưa kiểm chứng phải đi vào `.brain/claims.md` thông qua `/save-brain`, không được ghi thành project fact.
- Nếu cần ghi decision/claim, auto-save chỉ được lưu pointer ngắn trong `decision_refs` hoặc `claim_refs` sau khi durable log đã tồn tại.

## Trigger Conditions

### 1. Workflow End (Automatic)
Sau khi hoan thanh bat ky workflow nao:
- `/plan` → Save decisions, specs
- `/code` → Save progress, files changed
- `/debug` → Save errors resolved
- `/test` → Save test results
- `/deploy` → Save deployment info

### 2. User Leaving Detection
Pattern matching trong tin nhan user:
```
patterns:
  - "bye", "tạm biệt", "tam biet", "tạm nghỉ", "tam nghi"
  - "tôi đi", "toi di", "đi ăn cơm", "di an com", "nghỉ thôi", "nghi thoi"
  - "hết giờ", "het gio", "mai làm tiếp", "mai lam tiep", "save"
  - "đóng app", "dong app", "tắt máy", "tat may"
```

### 3. Decision Made Detection
Khi user dua ra quyet dinh:
```
patterns:
  - "chọn phương án", "chon phuong an", "dùng cái này", "dung cai nay"
  - "ok", "đồng ý", "dong y", "làm vậy", "lam vay"
  - "quyết định là", "quyet dinh la", "sẽ dùng", "se dung"
```

### 4. Periodic Checkpoint
Moi 15 tin nhan → Background save

### 5. Context Warning (80% estimate)
```
token_estimate = message_count * 150 + code_blocks * 300
if token_estimate > 100000:  # 80% of 128K
    trigger_emergency_save()
    show_warning()
```

## Execution Logic

### Step 1: Detect Trigger

```
on_message(user_input):
    increment message_count

    if matches_leaving_pattern(user_input):
        trigger = "user_leaving"
    elif matches_decision_pattern(user_input):
        trigger = "decision_made"
    elif message_count % 15 == 0:
        trigger = "periodic"
    elif estimate_tokens() > 100000:
        trigger = "emergency"
    else:
        return  # No save needed

    execute_save(trigger)
```

### Step 2: Generate Summary

```
summary = {
    "project": brain.project.name,
    "current_feature": session.working_on.feature,
    "current_task": session.working_on.task,
    "status": session.working_on.status,
    "progress_percent": calculate_progress(),
    "last_action": get_last_action(),
    "next_step": suggest_next_step(),
    "blockers_count": count_blockers()
}
```

### Step 3: Save to Session

```
append_to_file(".brain/session_log.txt", {
    timestamp: now(),
    trigger: trigger_type,
    workflow: active_workflow,
    summary: compress_summary(summary),
    message_count: current_count,
    files: changed_files
})

session.summary = merge_summary(session.summary, summary)
session.working_on = merge_narrow_progress(session.working_on, summary)
session.handover_required = trigger_type == "emergency"
save_only_allowed_fields(".brain/session.json")
```

### Step 4: Notify User (if enabled)

```
if trigger == "user_leaving":
    show: "💾 Thay ban chuan bi di, da auto-save session."

if trigger == "workflow_end":
    show: "💾 Da luu tien do. Ban co the dong app an toan."

if trigger == "emergency":
    show: "⚠️ Context sap day. Da save backup. Nen bat dau session moi."

if trigger == "periodic" or "decision_made":
    # Silent save - no notification
```

## Token Estimation Heuristic

```
function estimate_tokens():
    base = message_count * 150
    code_blocks = count_code_blocks() * 300
    error_dumps = count_errors() * 200

    return base + code_blocks + error_dumps

function get_warning_level():
    tokens = estimate_tokens()
    if tokens > 115000: return "critical"  # 90%
    if tokens > 100000: return "warning"   # 80%
    if tokens > 80000: return "info"       # 60%
    return "safe"
```

## Snapshot Management

### Save Snapshot (7 days retention)
```
on_workflow_end():
    snapshot = {
        timestamp: now(),
        session: session.json,
        brain_summary: extract_brain_summary()
    }
    save_to(".brain/snapshots/{date}_{time}.json")

    # Cleanup old snapshots
    delete_snapshots_older_than(7_days)
```

### Restore from Snapshot
```
if session.json corrupted:
    latest_snapshot = get_latest_snapshot()
    restore_from(latest_snapshot)
    show: "Da khoi phuc tu backup gan nhat."
```

## User Messages

```yaml
workflow_end:
  vi: "💾 Da luu tien do. Ban co the dong app an toan."
  en: "💾 Progress saved. You can safely close the app."

user_leaving:
  vi: "💾 Thay ban chuan bi di, da auto-save session."
  en: "💾 Detected you're leaving, session auto-saved."

context_warning:
  vi: "⚠️ Context sap day. Da save backup. Nen go /save-brain roi bat dau session moi."
  en: "⚠️ Context nearly full. Backup saved. Consider starting new session."

emergency_save:
  vi: "⚠️ Da luu khan cap. Go /recap trong session moi de tiep tuc."
  en: "⚠️ Emergency save complete. Use /recap in new session to continue."
```

## Integration with Workflows

Mọi workflow nên gọi auto-save khi kết thúc nếu có thay đổi đáng ghi nhớ:

```markdown
# Cuoi moi workflow.md:

## Post-Workflow: Auto-Save

Sau khi hoan thanh workflow:
1. Cap nhat session.summary
2. Append checkpoint vao `.brain/session_log.txt`
3. Update field hẹp trong `.brain/session.json`
4. Hien thong bao nếu `notify_on_save=true`: "💾 Da luu tien do."
```

## Config Options

```json
{
  "auto_save_config": {
    "enabled": true,
    "notify_on_save": true,
    "checkpoint_interval": 15,
    "warn_threshold": 80,
    "snapshot_retention_days": 7
  }
}
```

## Error Handling

```
if save_fails:
    retry 3 times with exponential backoff
    if still fails:
        show: "⚠️ Khong the luu session. Kiem tra quyen ghi file."
        log error to console

if disk_full:
    delete oldest snapshots
    retry save
```
