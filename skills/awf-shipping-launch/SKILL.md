---
name: awf-shipping-launch
description: >
  Chuẩn bị deploy production với checklist đầy đủ và chiến lược rollout an toàn.
  Kích hoạt khi chuẩn bị deploy tính năng mới lên production, cần pre-launch checklist,
  setup monitoring, plan staged rollout, hay rollback strategy. Keywords: deploy, launch,
  ship, production, rollout, feature flag, monitoring, rollback, checklist trước khi launch.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-shipping-launch"
skill_version: "1.0.0"
status: active
category: "release"
activation: "conditional"
priority: "high"
risk_level: "high"
allowed_side_effects:
  - "release_plan"
requires_confirmation: true
related_workflows:
  - "/deploy"
  - "/rollback"
  - "/audit"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# Shipping & Launch — Deploy An Toàn, Có Thể Roll Back

## Tổng quan
Ship với sự tự tin. Mục tiêu không chỉ là deploy — mà là deploy an toàn, có monitoring sẵn sàng, rollback plan chuẩn bị trước, và hiểu rõ thế nào là success.

> 💡 **Triết lý:** Mọi launch đều phải reversible, observable, và incremental.

---

## Khi nào kích hoạt

✅ **NÊN dùng:**
- Deploy tính năng lên production lần đầu
- Release thay đổi lớn tới users
- Migrate data hoặc infrastructure
- Mở beta hoặc early access
- Bất kỳ deployment nào có risk (tức là tất cả deployments)

---

## Pre-Launch Checklist (Phải hoàn thành trước khi deploy)

### Code Quality
- [ ] Tất cả tests pass (unit, integration, e2e)
- [ ] Build thành công, không có warnings
- [ ] Lint và type checking pass
- [ ] Code đã được review và approve
- [ ] Không có TODO comments cần resolve trước launch
- [ ] Không có `console.log` debug trong production code
- [ ] Error handling cover các failure modes có thể xảy ra

### Security
- [ ] Không có secrets trong code hay version control
- [ ] `npm audit` không có critical/high vulnerabilities
- [ ] Input validation trên tất cả user-facing endpoints
- [ ] Authentication và authorization checks đã setup
- [ ] Security headers configured (CSP, HSTS, v.v.)
- [ ] Rate limiting trên auth endpoints
- [ ] CORS chỉ cho phép specific origins (không wildcard)

### Performance
- [ ] Core Web Vitals trong ngưỡng "Good"
- [ ] Không có N+1 queries trong critical paths
- [ ] Images optimized (compression, responsive sizes, lazy loading)
- [ ] Bundle size trong budget
- [ ] Database queries có appropriate indexes
- [ ] Caching configured cho static assets và repeated queries

### Infrastructure
- [ ] Environment variables đã set trong production
- [ ] Database migrations đã apply (hoặc ready to apply)
- [ ] DNS và SSL đã configured
- [ ] CDN configured cho static assets
- [ ] Logging và error reporting đã configured
- [ ] Health check endpoint tồn tại và trả về 200

### Documentation
- [ ] README updated với setup requirements mới
- [ ] API documentation current
- [ ] ADRs đã viết cho architectural decisions
- [ ] Changelog updated

---

## Chiến lược: Feature Flags (Tách Deployment Khỏi Release)

Deploy code vào production nhưng chưa bật tính năng — đây là best practice:

```typescript
// Feature flag check
const flags = await getFeatureFlags(userId);

if (flags.taskSharing) {
  return <TaskSharingPanel task={task} />;
}
return null; // Behavior cũ
```

**Lifecycle của feature flag:**
```
1. DEPLOY với flag OFF     → Code trong production nhưng inactive
2. ENABLE cho team/beta    → Internal testing trong production environment
3. GRADUAL ROLLOUT         → 5% → 25% → 50% → 100% users
4. MONITOR mỗi stage      → Watch error rates, performance, feedback
5. CLEAN UP                → Xóa flag và dead code path sau full rollout
```

**Rules:**
- Mỗi feature flag có owner và expiration date
- Clean up flags trong vòng 2 tuần sau full rollout
- Không nest feature flags (tạo exponential combinations)
- Test cả hai states (on và off) trong CI

---

## Rollout Sequence Chuẩn

```
1. DEPLOY lên staging
   └── Chạy full test suite
   └── Manual smoke test các critical flows

2. DEPLOY lên production (feature flag OFF)
   └── Verify deployment thành công (health check)
   └── Check error monitoring (không có lỗi mới)

3. ENABLE cho team (flag ON cho internal users)
   └── Team dùng tính năng trong production
   └── 24-hour monitoring window

4. CANARY rollout (flag ON cho 5% users)
   └── Monitor error rates, latency, user behavior
   └── Compare metrics: canary vs baseline
   └── 24-48 hour monitoring window
   └── Advance chỉ khi tất cả thresholds pass (bảng bên dưới)

5. GRADUAL increase (25% → 50% → 100%)
   └── Cùng monitoring ở mỗi bước
   └── Có thể roll back về percentage trước bất cứ lúc nào

6. FULL rollout (flag ON cho tất cả users)
   └── Monitor 1 tuần
   └── Clean up feature flag
```

### Rollout Decision Thresholds

| Metric | Tiếp tục ✅ | Hold và investigate ⚠️ | Roll back 🔴 |
|--------|------------|----------------------|-------------|
| Error rate | Trong 10% baseline | 10-100% trên baseline | > 2x baseline |
| P95 latency | Trong 20% baseline | 20-50% trên baseline | > 50% trên baseline |
| Client JS errors | Không có error type mới | Error mới < 0.1% sessions | Error mới > 0.1% sessions |
| Business metrics | Neutral hoặc positive | Giảm < 5% (có thể là noise) | Giảm > 5% |

---

## Khi Nào Roll Back Ngay

Roll back ngay lập tức nếu:
- Error rate tăng > 2x baseline
- P95 latency tăng > 50%
- User-reported issues tăng đột biến
- Data integrity issues phát hiện
- Security vulnerability phát hiện

---

## Monitoring Cần Setup

```
Application metrics:
├── Error rate (total và theo endpoint)
├── Response time (p50, p95, p99)
├── Request volume
├── Active users
└── Key business metrics (conversion, engagement)

Infrastructure metrics:
├── CPU và memory utilization
├── Database connection pool usage
├── Disk space
├── Network latency
└── Queue depth (nếu có)

Client metrics:
├── Core Web Vitals (LCP, INP, CLS)
├── JavaScript errors
├── API error rates từ client perspective
└── Page load time
```

---

## Rollback Plan Template

Phải có rollback plan TRƯỚC KHI deploy:

```markdown
## Rollback Plan: [Feature/Release]

### Trigger Conditions
- Error rate > 2x baseline
- P95 latency > [X]ms
- User reports về [specific issue]

### Rollback Steps
Option A (nhanh): Disable feature flag
  → Thời gian: < 1 phút

Option B (deploy lại version cũ):
1. git revert <commit> && git push
2. Verify rollback: health check, error monitoring
3. Notify team về rollback

### Database Considerations
- Migration [X] có rollback: `npx prisma migrate rollback`
- Data từ tính năng mới: [giữ lại / clean up]

### Thời gian Roll Back
- Feature flag: < 1 phút
- Redeploy version cũ: < 5 phút
- Database rollback: < 15 phút
```

---

## Post-Launch Verification (1 giờ đầu sau launch)

```
1. Check health endpoint trả về 200
2. Check error monitoring dashboard (không có error types mới)
3. Check latency dashboard (không có regression)
4. Test critical user flow thủ công
5. Verify logs đang flow và readable
6. Confirm rollback mechanism ready (dry run nếu được)
```

---

## ⚠️ Anti-Rationalization

| Lý do bỏ qua | Thực tế |
|---|---|
| "Staging ok là production ok" | Production có data khác, traffic patterns khác, edge cases khác. Monitor sau deploy. |
| "Cái này không cần feature flag" | Mọi tính năng đều benefit từ kill switch. Kể cả thay đổi "đơn giản" cũng có thể break. |
| "Monitoring là overhead" | Không có monitoring = phát hiện vấn đề từ user complaints thay vì dashboards. |
| "Sẽ thêm monitoring sau" | Thêm trước launch. Không debug được cái không nhìn thấy. |
| "Roll back là thừa nhận thất bại" | Roll back là responsible engineering. Ship tính năng broken mới là thất bại. |

---

## 🚩 Red Flags

- Deploy mà không có rollback plan
- Không có monitoring hoặc error reporting trong production
- Big-bang releases (tất cả cùng lúc, không có staging)
- Feature flags không có expiration hoặc owner
- Không ai monitor deploy trong 1 giờ đầu
- Production environment configuration từ memory, không phải code
- "Thứ Sáu buổi chiều, ship luôn" 🚫

---

## ✅ Verification

**Trước khi deploy:**
- [ ] Pre-launch checklist hoàn thành (tất cả sections xanh)
- [ ] Feature flag configured (nếu applicable)
- [ ] Rollback plan đã document
- [ ] Monitoring dashboards đã setup
- [ ] Team đã được notify về deployment

**Sau khi deploy:**
- [ ] Health check trả về 200
- [ ] Error rate bình thường
- [ ] Latency bình thường
- [ ] Critical user flow hoạt động
- [ ] Logs đang flow
- [ ] Rollback đã test hoặc verified ready
