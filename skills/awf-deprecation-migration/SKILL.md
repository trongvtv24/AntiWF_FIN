---
name: awf-deprecation-migration
description: >
  Quản lý quy trình loại bỏ code cũ, API, hoặc tính năng không còn cần thiết một cách an toàn.
  Kích hoạt khi cần xóa system cũ, migrate users sang implementation mới, hay consolidate
  duplicate code. Keywords: deprecate, xóa code, migration, refactor, legacy, sunset, remove.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-deprecation-migration"
skill_version: "1.0.0"
status: active
category: "maintenance"
activation: "conditional"
priority: "medium"
risk_level: "high"
allowed_side_effects:
  - "code_change_plan"
requires_confirmation: true
related_workflows:
  - "/refactor"
  - "/code"
  - "/audit"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# Deprecation & Migration — Xóa Code An Toàn

## Tổng quan
Code là liability, không phải asset. Mỗi dòng code có ongoing cost: bugs cần fix, dependencies cần update, security patches, và cognitive overhead cho mọi người tiếp cận sau. Deprecation là kỷ luật loại bỏ code không còn worth keeping, và migration là process di chuyển users an toàn từ cũ sang mới.

> 💡 **Triết lý:** Xóa code là thành tích, không phải thất bại.

---

## Khi nào kích hoạt

✅ **NÊN dùng:**
- Thay thế system, API, hoặc library cũ bằng cái mới
- Sunset tính năng không còn cần thiết
- Consolidate duplicate implementations
- Remove dead code mà không ai own nhưng nhiều chỗ depend on
- Plan lifecycle của system mới (deprecation planning bắt đầu từ lúc design)

---

## Quyết định Có Nên Deprecate Không

Trước khi deprecate bất cứ gì, trả lời 5 câu hỏi này:

```
1. System này có còn cung cấp unique value không?
   → Có: maintain. Không: tiếp tục.

2. Bao nhiêu users/consumers phụ thuộc vào nó?
   → Quantify phạm vi migration.

3. Đã có replacement chưa?
   → Chưa có: build replacement trước. Không deprecate mà không có alternative.

4. Migration cost cho mỗi consumer là bao nhiêu?
   → Nếu có thể automate: làm luôn. Nếu manual và tốn công: cân nhắc vs maintenance cost.

5. Ongoing cost của việc KHÔNG deprecate là gì?
   → Security risk, engineer time, complexity opportunity cost.
```

---

## Advisory vs Compulsory Deprecation

| Loại | Khi nào dùng | Cơ chế |
|------|-------------|--------|
| **Advisory** | Migration tùy chọn, system cũ vẫn stable | Warnings, docs, nudges. Users migrate theo timeline của họ. |
| **Compulsory** | System cũ có security issues, block progress, maintenance cost không bền vững | Hard deadline. Phải cung cấp migration tooling. |

**Default: Advisory.** Dùng Compulsory chỉ khi maintenance cost hoặc risk justify việc force migration.

---

## 4 Bước Quy Trình Chuẩn

### Bước 1: Build Replacement Trước

Không deprecate khi chưa có alternative. Replacement phải:
- Cover tất cả critical use cases của system cũ
- Có documentation và migration guides
- Đã proven in production (không chỉ "theoretically better")

### Bước 2: Announce & Document

```markdown
## Deprecation Notice: OldService

**Status:** Deprecated as of [date]
**Replacement:** NewService (xem migration guide bên dưới)
**Removal date:** Advisory — chưa có hard deadline
**Lý do:** OldService yêu cầu manual scaling và thiếu observability.
            NewService xử lý cả hai tự động.

### Migration Guide
1. Thay `import { client } from 'old-service'`
   bằng `import { client } from 'new-service'`
2. Cập nhật configuration (xem examples bên dưới)
3. Chạy migration verification script: `npx migrate-check`
```

### Bước 3: Migrate Từng Bước

Migrate consumers từng cái một, không phải tất cả cùng lúc. Với mỗi consumer:

```
1. Xác định tất cả touchpoints với deprecated system
2. Update sang replacement
3. Verify behavior match (tests, integration checks)
4. Remove references đến system cũ
5. Confirm không có regressions
```

> ⚠️ **Churn Rule:** Nếu bạn own infrastructure đang deprecated, bạn có trách nhiệm migrate users — hoặc cung cấp backward-compatible updates. Không được announce deprecation rồi để users tự xoay xở.

### Bước 4: Remove System Cũ

Chỉ sau khi tất cả consumers đã migrate:

```
1. Verify zero active usage (metrics, logs, dependency analysis)
2. Remove code
3. Remove associated tests, docs, configuration
4. Remove deprecation notices
5. 🎉 Celebrate — xóa code là thành tích!
```

---

## Patterns Migration Hiệu Quả

### Strangler Pattern
Chạy hệ thống cũ và mới song song. Route traffic từng bước từ cũ sang mới:

```
Phase 1: New handles 0%,  old handles 100%
Phase 2: New handles 10%  (canary)
Phase 3: New handles 50%
Phase 4: New handles 100%, old idle
Phase 5: Remove old system
```

### Adapter Pattern
Tạo adapter translate calls từ interface cũ sang implementation mới:

```typescript
// Adapter: old interface, new implementation
class LegacyTaskService implements OldTaskAPI {
  constructor(private newService: NewTaskService) {}

  // Old method signature, delegates to new implementation
  getTask(id: number): OldTask {
    const task = this.newService.findById(String(id));
    return this.toOldFormat(task);
  }
}
```

### Feature Flag Migration
Dùng feature flags để switch consumers từng cái:

```typescript
function getTaskService(userId: string): TaskService {
  if (featureFlags.isEnabled('new-task-service', { userId })) {
    return new NewTaskService();
  }
  return new LegacyTaskService();
}
```

---

## Zombie Code (Code Không Ai Sở Hữu)

Zombie code: không được maintain actively, không có owner rõ ràng, tích lũy security vulnerabilities. Dấu hiệu:
- Không có commits trong 6+ months nhưng vẫn có consumers
- Không có assigned maintainer
- Failing tests không ai fix
- Dependencies với known vulnerabilities không ai update

**Cách xử lý:** Hoặc assign owner và maintain đúng cách, hoặc deprecate với migration plan cụ thể. Zombie code không được ở trạng thái limbo.

---

## ⚠️ Anti-Rationalization

| Lý do bỏ qua | Thực tế |
|---|---|
| "Nó vẫn chạy được mà" | Working code không maintain tích lũy security debt silently. |
| "Ai đó có thể cần sau này" | Nếu cần sau, rebuild lại được. Keep "just in case" tốn hơn rebuild. |
| "Migration quá tốn kém" | So sánh migration cost với ongoing maintenance cost trong 2-3 năm. Migration thường rẻ hơn long-term. |
| "Deprecate sau khi xong system mới" | Deprecation planning bắt đầu từ lúc design. Khi xong system mới sẽ có priorities khác. Plan ngay. |
| "Users sẽ tự migrate" | Không bao giờ. Cung cấp tooling, docs, và incentives — hoặc tự migrate. |
| "Có thể maintain cả hai mãi" | Hai systems làm cùng việc = double maintenance, testing, docs, onboarding cost. |

---

## 🚩 Red Flags

- Deprecated systems không có replacement available
- Deprecation announcements không có migration tooling hoặc docs
- "Soft" deprecation advisory mãi mà không có progress
- Zombie code không owner mà vẫn có consumers
- Thêm tính năng mới vào deprecated system
- Deprecate mà không đo current usage
- Xóa code mà không verify zero active consumers

---

## ✅ Verification Checklist

Sau khi hoàn thành deprecation:
- [ ] Replacement production-proven và cover tất cả critical use cases
- [ ] Migration guide tồn tại với steps cụ thể và examples
- [ ] Tất cả active consumers đã migrate (verified bằng metrics/logs)
- [ ] Code cũ, tests, docs, và configuration đã xóa hoàn toàn
- [ ] Không còn references đến deprecated system trong codebase
- [ ] Deprecation notices đã xóa (đã xong nhiệm vụ)
