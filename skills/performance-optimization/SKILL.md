---
name: performance-optimization
description: >
  Đo lường và tối ưu performance ứng dụng một cách có hệ thống. Kích hoạt khi có
  performance requirements, khi Core Web Vitals kém, khi có N+1 queries, bundle size phình to,
  hoặc khi user/monitoring báo cáo app chậm. Nguyên tắc: MEASURE FIRST — tối ưu không có data = đoán mò.
  Keywords: performance, tối ưu, chậm, LCP, CLS, INP, N+1 query, bundle size, lazy loading, cache.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "performance-optimization"
skill_version: "1.0.0"
status: active
category: "quality"
activation: "conditional"
priority: "high"
risk_level: "medium"
allowed_side_effects:
  - "measure"
  - "code_change_after_request"
requires_confirmation: false
related_workflows:
  - "/audit"
  - "/refactor"
  - "/code"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# Performance Optimization — Đo Trước, Sửa Sau

## Tổng quan
Đo lường trước khi tối ưu. Performance work không có measurement = đoán mò — và đoán dẫn tới premature optimization, thêm complexity mà không cải thiện gì thực sự.

> 💡 **Workflow cốt lõi:** Profile → Identify → Fix → Verify → Guard

---

## Khi nào kích hoạt

✅ **NÊN dùng:**
- Có performance requirements trong spec (load time budgets, SLAs)
- Users hoặc monitoring báo cáo chậm
- Core Web Vitals scores dưới ngưỡng
- Nghi ngờ một thay đổi gây regression
- Build feature xử lý dataset lớn hoặc traffic cao

❌ **KHÔNG dùng:**
- Tối ưu trước khi có bằng chứng vấn đề — Premature optimization thêm complexity hơn performance gain

---

## Core Web Vitals Targets

| Metric | Tốt | Cần cải thiện | Kém |
|--------|-----|---------------|-----|
| **LCP** (Largest Contentful Paint) | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| **INP** (Interaction to Next Paint) | ≤ 200ms | ≤ 500ms | > 500ms |
| **CLS** (Cumulative Layout Shift) | ≤ 0.1 | ≤ 0.25 | > 0.25 |

---

## Workflow: 5 Bước Chuẩn

```
1. MEASURE  → Lấy baseline với data thực
2. IDENTIFY → Tìm bottleneck thực sự (không phải giả định)
3. FIX      → Xử lý đúng bottleneck đó
4. VERIFY   → Đo lại, xác nhận cải thiện
5. GUARD    → Thêm monitoring hoặc test để tránh regression
```

---

## Bước 1: Đo lường

**Hai cách tiếp cận — dùng cả hai:**

- **Synthetic (Lighthouse, DevTools Performance tab):** Điều kiện controlled, reproducible. Tốt cho CI regression detection.
- **RUM (Real User Monitoring - web-vitals library, CrUX):** Data người dùng thực. Cần để validate fix thực sự hiệu quả.

**Frontend:**
```javascript
// RUM: Web Vitals library trong code
import { onLCP, onINP, onCLS } from 'web-vitals';
onLCP(console.log);
onINP(console.log);
onCLS(console.log);

// Synthetic: Chrome DevTools → Performance tab → Record
// hoặc Lighthouse CLI: npx lighthouse https://yoursite.com
```

**Backend:**
```javascript
// Simple timing
console.time('db-query');
const result = await db.query(...);
console.timeEnd('db-query');

// Full: APM (Application Performance Monitoring)
// Datadog, New Relic, hoặc OpenTelemetry
```

---

## Bước 2: Tìm Bottleneck

**Triệu chứng → Nguyên nhân:**

```
App bị chậm ở đâu?
├── First page load
│   ├── Bundle lớn? → Check code splitting, tree shaking
│   ├── Server response chậm? → Profile backend, check queries
│   └── Render-blocking resources? → Check CSS/JS blocking
├── Interaction sluggish
│   ├── UI freeze khi click? → Long tasks > 50ms trên main thread
│   ├── Form input lag? → Check re-renders, controlled component overhead
│   └── Animation jank? → Layout thrashing, forced reflows
├── API / Backend
│   ├── Single endpoint chậm? → Profile DB queries, check indexes
│   ├── Tất cả endpoints chậm? → Connection pool, memory, CPU
│   └── Intermittent? → Lock contention, GC pauses
```

---

## Patterns Phổ Biến Cần Fix

### N+1 Query (Backend) — Nguy hiểm nhất

```javascript
// ❌ BAD: N+1 — 1 query mỗi task để lấy owner
const tasks = await db.tasks.findMany();
for (const task of tasks) {
  task.owner = await db.users.findUnique({ where: { id: task.ownerId } });
}

// ✅ GOOD: 1 query duy nhất với join
const tasks = await db.tasks.findMany({
  include: { owner: true },
});
```

### Unbounded Data Fetching

```javascript
// ❌ BAD: Fetch tất cả records
const allTasks = await db.tasks.findMany();

// ✅ GOOD: Paginated với limits
const tasks = await db.tasks.findMany({
  take: 20,
  skip: (page - 1) * 20,
  orderBy: { createdAt: 'desc' },
});
```

### Missing Image Optimization (Frontend)

```html
<!-- ❌ BAD: Không dimension, không format tối ưu -->
<img src="/hero.jpg" />

<!-- ✅ GOOD: Hero image với priority high -->
<img
  src="/hero.webp"
  width="1200"
  height="600"
  fetchpriority="high"
  alt="Mô tả ảnh"
/>

<!-- ✅ GOOD: Ảnh below-fold — lazy load -->
<img
  src="/content.webp"
  width="800"
  height="400"
  loading="lazy"
  decoding="async"
  alt="Mô tả ảnh"
/>
```

### React Re-renders Không Cần Thiết

```tsx
// ❌ BAD: Tạo object mới mỗi render → children re-render
function TaskList() {
  return <TaskFilters options={{ sortBy: 'date', order: 'desc' }} />;
}

// ✅ GOOD: Stable reference
const DEFAULT_OPTIONS = { sortBy: 'date', order: 'desc' } as const;
function TaskList() {
  return <TaskFilters options={DEFAULT_OPTIONS} />;
}

// ✅ GOOD: Memo cho expensive components
const TaskItem = React.memo(function TaskItem({ task }) {
  return <div>{/* expensive render */}</div>;
});
```

### Large Bundle Size

```typescript
// ✅ GOOD: Dynamic import cho heavy features
const ChartLibrary = lazy(() => import('./ChartLibrary'));

// ✅ GOOD: Route-level code splitting
const SettingsPage = lazy(() => import('./pages/Settings'));
function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <SettingsPage />
    </Suspense>
  );
}
```

### Missing Backend Caching

```javascript
// Cache data ít thay đổi nhưng đọc nhiều
const CACHE_TTL = 5 * 60 * 1000; // 5 phút
let cachedConfig = null;
let cacheExpiry = 0;

async function getAppConfig() {
  if (cachedConfig && Date.now() < cacheExpiry) return cachedConfig;
  cachedConfig = await db.config.findFirst();
  cacheExpiry = Date.now() + CACHE_TTL;
  return cachedConfig;
}

// HTTP caching cho static assets
app.use('/static', express.static('public', {
  maxAge: '1y',
  immutable: true, // Dùng content hashing trong filename
}));
```

---

## Performance Budget (Ngưỡng không được vượt)

```
JavaScript bundle:  < 200KB gzipped (initial load)
CSS:                < 50KB gzipped
Images:             < 200KB per image (above the fold)
Fonts:              < 100KB total
API response time:  < 200ms (p95)
Time to Interactive: < 3.5s trên 4G
Lighthouse score:   ≥ 90
```

**Enforce trong CI:**
```bash
# Bundle size check
npx bundlesize --config bundlesize.config.json

# Lighthouse CI
npx lhci autorun
```

---

## ⚠️ Anti-Rationalization

| Lý do bỏ qua | Thực tế |
|---|---|
| "Tối ưu sau" | Performance debt compound. Fix anti-patterns rõ ràng ngay, defer micro-optimizations. |
| "Trên máy em nhanh mà" | Máy em không phải máy user. Profile trên hardware và network đại diện. |
| "Tối ưu này rõ ràng cần làm" | Nếu không đo, không biết. Profile trước. |
| "User không nhận ra 100ms" | Research: 100ms delays impact conversion rates. User nhận ra nhiều hơn nghĩ. |
| "Framework lo performance rồi" | Framework ngăn một số issues nhưng không fix N+1 queries hay bundle size. |

---

## 🚩 Red Flags

- Tối ưu không có profiling data để justify
- N+1 query patterns trong data fetching
- List endpoints không có pagination
- Images không có dimensions, lazy loading, responsive sizes
- Bundle size tăng mà không có review
- Không có performance monitoring trong production
- `React.memo` và `useMemo` khắp nơi (overuse cũng tệ như underuse)

---

## ✅ Verification Checklist

Sau bất kỳ thay đổi performance nào:
- [ ] Có measurements before/after (số liệu cụ thể)
- [ ] Bottleneck cụ thể đã được identify và address
- [ ] Core Web Vitals trong ngưỡng "Good"
- [ ] Bundle size không tăng đáng kể
- [ ] Không có N+1 queries trong code mới
- [ ] Performance budget pass trong CI (nếu đã setup)
- [ ] Existing tests vẫn pass (optimization không break behavior)
