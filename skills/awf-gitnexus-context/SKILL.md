---
name: awf-gitnexus-context
description: >-
  Code Intelligence Engine - Phan tich kien truc codebase 360 do voi GitNexus.
  Tu dong kich hoat khi dung /code, /debug, /refactor, /audit.
  Cung cap: impact analysis, call chain, dependency graph, pre-commit risk check.
  Keywords: impact, dependency, caller, callee, architecture, refactor risk,
  breaking change, call chain, symbol, function graph, gitnexus.
version: 1.0.0
triggers:
  - workflow: /code
  - workflow: /debug
  - workflow: /refactor
  - workflow: /audit
# AWF_METADATA_START
type: skill
name: "awf-gitnexus-context"
skill_version: "1.0.0"
status: active
category: "code_intelligence"
activation: "conditional"
priority: "medium"
risk_level: "low"
allowed_side_effects:
  - "read_index"
requires_confirmation: false
related_workflows:
  - "/code"
  - "/debug"
  - "/refactor"
  - "/audit"
  - "/rollback"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF GitNexus Context Skill

Cung cap kha nang phan tich kien truc code sau thong qua GitNexus Knowledge Graph.

## Cach hoat dong

### Buoc 1: Kiem tra index ton tai

Truoc khi bat ky workflow nao bat dau (/code, /debug, /refactor, /audit),
kiem tra xem repo hien tai da duoc index chua:

```
if .gitnexus/ ton tai trong thu muc project hien tai:
    → Bao: "🔬 GitNexus san sang — em co the phan tich impact va kien truc truoc khi thay doi."
    → Kich hoat cac tool (xem phan duoi)

if .gitnexus/ KHONG ton tai:
    → Bao (1 lan, khong lam phien them):
      "💡 Tip: Chay `gitnexus analyze` de unlock kha nang phan tich kien truc code sau hon.
       (Chi can chay 1 lan cho moi project)"
    → Tiep tuc binh thuong, KHONG block workflow
```

---

## Cac Tool co san (khi da co index)

### 1. Impact Analysis — Ai se bi anh huong?

**Dung khi:** Sap sua/xoa/doi ten mot ham, class, interface.

```
Goi: impact({target: "[ten_symbol]", direction: "upstream", minConfidence: 0.8})

Ket qua tra ve:
- Depth 1 (WILL BREAK): Cac ham goi truc tiep → "Chac chan hong"
- Depth 2 (LIKELY AFFECTED): Cac module lien quan → "Co the anh huong"
- Risk level: low / medium / high

Options them:
- direction: "upstream" (ai phu thuoc vao no) hoac "downstream" (no phu thuoc vao ai)
- maxDepth: 1-5 (do sau can truy)
- includeTests: true/false
- relationTypes: ["CALLS", "IMPORTS", "EXTENDS", "IMPLEMENTS"]
```

**Khi nao dung:**
- Truoc khi `/refactor` bat ky symbol nao
- Khi `/debug` de tim tat ca cho co the bi anh huong boi loi
- Truoc khi `/audit` kiem tra security surface area

---

### 2. Context — Xem toa do 360° cua mot Symbol

**Dung khi:** Can hieu mot ham/class dang lam gi, ai goi, goi ai.

```
Goi: context({name: "[ten_symbol]"})

Ket qua tra ve:
- filePath: Duong dan file
- startLine: Dong bat dau
- incoming.calls: [Danh sach caller — ai goi symbol nay]
- incoming.imports: [Ai import symbol nay]
- outgoing.calls: [Symbol nay goi ham nao]
- processes: [No tham gia vao flow nao, buoc thu may]
```

**Khi nao dung:**
- Dau tien khi `/debug` bat dau dieu tra mot loi tai symbol cu the
- Khi `/code` muon hieu ro truoc khi them/sua logic
- Khi `/audit` muon kiem tra diem dau vao (entry points)

---

### 3. Query — Tim kiem thong minh theo chu de

**Dung khi:** Tim tat ca code lien quan den mot chu de (VD: "authentication", "payment").

```
Goi: query({query: "[chu de can tim]"})

Ket qua tra ve:
- processes: Danh sach cac flows lien quan (VD: LoginFlow, PaymentFlow)
- symbol_count: So symbol tham gia
- definitions: Interface/Type lien quan
```

**Khi nao dung:**
- `/audit` → query("authentication"), query("payment"), query("user input") de tim diem rui ro
- `/debug` → query("[mo ta loi]") de tim code lien quan
- `/brainstorm` moi tinh nang → hieu nhung gi da co de tranh trung lap

---

### 4. Detect Changes — Kiem tra rui ro truoc khi commit

**Dung khi:** Truoc khi `/deploy` hoac sau khi /code xong nhieu file.

```
Goi: detect_changes({scope: "all"})

Ket qua tra ve:
- changed_count: So symbol da thay doi
- affected_count: So symbol bi anh huong gian tiep
- risk_level: low / medium / high
- affected_processes: Cac flow bi anh huong
- changed_symbols: Danh sach cu the
```

**Khi nao dung:**
- Cuoi `/code` pha nao do → Bao cao rui ro truoc khi anh test
- Truoc `/deploy` → Check lan cuoi khong co breaking change an
- `/audit` → Ket hop voi impact analysis de bao cao toan dien

---

### 5. Cypher Query — Truy van do thi tuy chinh

**Dung khi:** Can truy van phuc tap ma cac tool tren chua dap ung.

```
Vi du: Tim tat ca ham co nhieu hon 10 caller
MATCH (caller)-[r:CodeRelation {type: 'CALLS'}]->(fn)
WITH fn, COUNT(caller) as callerCount
WHERE callerCount > 10
RETURN fn.name, fn.filePath, callerCount
ORDER BY callerCount DESC
```

---

## Tich hop vao tung Workflow

### /code
```
Sau buoc 0.3 (Luu Current Plan vao Session):

0.4. GitNexus Context Check
├── Co .gitnexus/ ?
│   ├── YES → Bao "🔬 GitNexus san sang"
│   │         Truoc khi sua bat ky symbol quan trong:
│   │         → Uu tien chay impact() de to sang rui ro
│   └── NO  → Bao tip 1 lan, tiep tuc binh thuong
```

### /debug
```
Trong Giai doan 2.1 (Log Analysis), THEM buoc:

2.1.5. GitNexus Symbol Investigation (neu co index)
→ Xac dinh ten symbol/ham bi loi tu error log
→ context({name: "[symbol loi]"})
→ Dung caller list + process list lam bang chung trong Hypothesis Formation
→ Neu nhieu caller → Rui ro regression cao, bao user truoc khi fix
```

### /refactor
```
THEM buoc bat buoc truoc khi bat dau refactor:

Pre-Refactor Safety Check:
1. impact({target: "[symbol can refactor]", direction: "upstream"})
2. Hien thi danh sach diem bi anh huong
3. Neu risk_level = "high" → BAT BUOC xin phep anh truoc
4. Neu risk_level = "medium" → Canh bao va cho anh xac nhan
5. Neu risk_level = "low" → Tiep tuc, chhi mention nhanh
```

### /audit
```
THEM Giai doan: GitNexus Structural Audit

1. Kiem tra High-Blast-Radius Symbols:
   → Tim cac symbol co nhieu caller nhat
   → Day la cac diem rui ro cao nhat neu bi hack/loi

2. Tight Coupling Detection:
   → Tim process cross nhieu community (>3)
   → Day la dau hieu kien truc tightly coupled

3. Entry Point Mapping:
   → context() cho tung entry point (API routes, CLI commands)
   → Kiem tra authentication/authorization co mat khong
```

---

## Huong dan setup lan dau (cho moi project moi)

```
1. Mo terminal trong thu muc project
2. Chay: gitnexus analyze
   → Qua trinh index ~30 giay den vai phut (tuy lon nho repo)
   → Tao thu muc .gitnexus/ (gitignored tu dong)
3. De MCP server tu dong chay khi can (cau hinh trong mcp_config.json)
4. Tu lan sau: AI tu dong co "bo nao kien truc" khi lam viec voi repo nay
```

## Luu y quan trong

```
- .gitnexus/ da duoc gitignore tu dong (khong push len repo)
- Index duoc luu LOCAL tren may anh (privacy: code khong ra ngoai)
- Neu co thay doi lon (them/xoa nhieu file) → chay lai gitnexus analyze
- 1 MCP server phuc vu nhieu repo (qua global registry ~/.gitnexus/)
```

## Error Handling

```
Neu gitnexus mcp chua chay:
    → Skill KHONG lam hong workflow
    → Bao: "💡 GitNexus chua khoi dong. Chay `gitnexus mcp` neu muon dung."
    → Tiep tuc workflow binh thuong

Neu repo chua analyze:
    → Bao tip 1 lan
    → KHONG nhac lai

Neu query khong tra ve ket qua:
    → Thong bao ngan: "Khong tim thay trong graph."
    → Dung grep/read file binh thuong nhu fallback
```
