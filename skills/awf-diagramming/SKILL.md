---
name: awf-diagramming
description: >
  Tạo diagrams kỹ thuật chuyên nghiệp từ mô tả text — ER diagram, Flowchart, Sequence diagram,
  Architecture diagram, Class diagram bằng Mermaid / PlantUML / ASCII art.
  Tự động kích hoạt khi dùng /design, /plan, /review hoặc khi user nhắc đến vẽ sơ đồ.
  Keywords: diagram, sơ đồ, flowchart, ER, sequence, architecture, mermaid, vẽ, chart, flow.
version: 1.0.0
# AWF_METADATA_START
type: skill
name: "awf-diagramming"
skill_version: "1.0.0"
status: active
category: "architecture"
activation: "conditional"
priority: "medium"
risk_level: "low"
allowed_side_effects:
  - "generate_diagram"
requires_confirmation: false
related_workflows:
  - "/plan"
  - "/design"
  - "/review"
required_gates:
  - "global_safety_truthfulness_gate"
# AWF_METADATA_END
---

# AWF Diagramming — Biến Mô Tả Thành Sơ Đồ

## Tổng quan
Một diagram tốt truyền đạt kiến trúc trong 5 giây mà 500 từ mô tả không làm được.
Skill này tự động chọn đúng loại diagram cho đúng tình huống và output Mermaid code có thể render ngay.

> 💡 **Nguyên tắc:** Diagram là artifact, không phải decoration. Mỗi diagram phải trả lời đúng 1 câu hỏi cụ thể.

---

## Khi nào kích hoạt

✅ **Tự động kích hoạt khi:**
- User dùng `/design` → vẽ Architecture + ER diagram
- User dùng `/plan` → vẽ Flowchart cho user journey
- User dùng `/review` → vẽ Dependency graph nếu phát hiện coupling
- User nói: "vẽ sơ đồ", "diagram", "flowchart", "draw me", "visualize"

---

## Bảng chọn Diagram type

| Câu hỏi cần trả lời | Loại diagram | Khi nào dùng |
|---------------------|-------------|-------------|
| Dữ liệu trông như thế nào? | **ER Diagram** | Database design, data modeling |
| Code gọi nhau như thế nào? | **Sequence Diagram** | API flows, authentication, messaging |
| Logic chạy theo hướng nào? | **Flowchart** | Business logic, decision trees, user journey |
| System gồm những gì? | **Architecture Diagram** | Infra, microservices, deployment |
| Class quan hệ với nhau thế nào? | **Class Diagram** | OOP design, domain modeling |
| Process theo thứ tự ra sao? | **Gantt / Timeline** | Project planning, release schedule |
| State machine? | **State Diagram** | UI states, order lifecycle |

---

## Templates sẵn dùng

### 🗄️ ER Diagram (Database Schema)

```mermaid
erDiagram
    USER {
        int id PK
        string email UK
        string name
        datetime created_at
    }
    ORDER {
        int id PK
        int user_id FK
        decimal total
        string status
        datetime created_at
    }
    ORDER_ITEM {
        int id PK
        int order_id FK
        int product_id FK
        int quantity
        decimal price
    }
    PRODUCT {
        int id PK
        string name
        decimal price
        int stock
    }

    USER ||--o{ ORDER : "places"
    ORDER ||--|{ ORDER_ITEM : "contains"
    PRODUCT ||--o{ ORDER_ITEM : "included in"
```

### 🔄 Sequence Diagram (API Flow)

```mermaid
sequenceDiagram
    participant C as Client
    participant API as API Gateway
    participant Auth as Auth Service
    participant DB as Database

    C->>API: POST /login {email, password}
    API->>Auth: validateCredentials()
    Auth->>DB: SELECT user WHERE email=?
    DB-->>Auth: user record
    Auth-->>API: {userId, token}
    API-->>C: 200 {token, expiresIn}

    Note over C,API: Token stored client-side
    C->>API: GET /profile (Bearer token)
    API->>Auth: verifyToken(token)
    Auth-->>API: {userId, valid: true}
    API->>DB: SELECT * FROM users WHERE id=?
    DB-->>API: user data
    API-->>C: 200 {user}
```

### 🏗️ Architecture Diagram (System Overview)

```mermaid
graph TB
    subgraph Client
        Web[Web App<br/>Next.js]
        Mobile[Mobile App<br/>React Native]
    end

    subgraph Gateway
        CDN[CDN<br/>Cloudflare]
        LB[Load Balancer<br/>Nginx]
    end

    subgraph Services
        API[API Service<br/>Node.js]
        Auth[Auth Service<br/>Node.js]
        Worker[Background Worker<br/>BullMQ]
    end

    subgraph Storage
        PG[(PostgreSQL<br/>Primary DB)]
        Redis[(Redis<br/>Cache + Queue)]
        S3[(S3<br/>File Storage)]
    end

    Web --> CDN
    Mobile --> CDN
    CDN --> LB
    LB --> API
    LB --> Auth
    API --> PG
    API --> Redis
    API --> S3
    API --> Worker
    Worker --> PG
    Worker --> Redis
```

### 📊 Flowchart (Business Logic)

```mermaid
flowchart TD
    Start([User clicks Checkout]) --> CheckLogin{Logged in?}
    CheckLogin -->|No| Login[Show Login Modal]
    Login --> CheckLogin
    CheckLogin -->|Yes| ValidateCart{Cart valid?}
    ValidateCart -->|Empty| ShowError[Error: Cart trống]
    ValidateCart -->|Has items| CheckStock{Stock available?}
    CheckStock -->|Out of stock| RemoveItems[Remove sold-out items]
    RemoveItems --> ValidateCart
    CheckStock -->|In stock| ShowPayment[Show Payment Form]
    ShowPayment --> ProcessPayment{Payment success?}
    ProcessPayment -->|Failed| PaymentError[Show error, retry]
    PaymentError --> ShowPayment
    ProcessPayment -->|Success| CreateOrder[Create Order]
    CreateOrder --> SendEmail[Send confirmation email]
    SendEmail --> Done([Order confirmed ✅])
```

### 🔵 State Diagram (Lifecycle)

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Pending : Submit
    Pending --> Processing : Payment received
    Pending --> Cancelled : Timeout / Cancel
    Processing --> Shipped : Dispatch
    Processing --> Cancelled : Out of stock
    Shipped --> Delivered : Confirmed
    Shipped --> Returned : Return request
    Delivered --> [*]
    Cancelled --> [*]
    Returned --> Refunded : Approved
    Refunded --> [*]
```

---

## Quy trình tạo Diagram

### Bước 1: Phân tích yêu cầu
```
User nói → Xác định:
  - Câu hỏi cần trả lời là gì?
  - Audience là ai? (Engineer? Business? Designer?)
  - Context đang ở phase nào? (Design? Review? Debug?)
```

### Bước 2: Chọn đúng loại (xem bảng trên)

### Bước 3: Draft nhanh
- Start simple — 5-7 nodes để validate structure trước
- Không cần perfect ngay lần đầu
- Hỏi user "Đây đúng flow chưa?" trước khi detail hơn

### Bước 4: Render + Export
Output theo format:
```markdown
## [Tên Diagram]

> [Mô tả 1 câu: diagram này trả lời câu hỏi gì]

```mermaid
[code]
```

**Đọc diagram này:**
- [Hướng dẫn đọc ngắn gọn nếu phức tạp]
- [Key relationships hoặc decision points]
```

---

## Tích hợp với AWF Workflows

### → `/design` (Auto-trigger)
Khi user kết thúc `/design`, tự động gợi ý:
```
"Anh muốn em vẽ thêm không?
1️⃣ ER Diagram cho database schema vừa design
2️⃣ Sequence Diagram cho API flow chính
3️⃣ Architecture Diagram overview toàn hệ thống"
```

### → `/plan` (Auto-trigger)
Khi plan xong, offer:
```
"Em vẽ User Journey Flowchart cho feature này nhé? (type: y/n)"
```

### → `/review` (Conditional)
Nếu phát hiện coupling phức tạp trong code review:
```
"Em thấy module dependencies khá rối. Anh muốn em vẽ Dependency Graph không?"
```

---

## Best Practices

**✅ Diagram tốt:**
- Có title rõ ràng
- Trả lời đúng 1 câu hỏi
- Không quá 15 nodes (quá nhiều = cần split)
- Có legend nếu dùng nhiều ký hiệu

**❌ Diagram xấu:**
- "God diagram" — cố nhét mọi thứ vào 1 diagram
- Nodes tên quá tắt không ai hiểu
- Không có direction rõ ràng (vẽ thế nào cũng được)
- Copy-paste từ tool không có context

---

## 🚩 Red Flags

- User hỏi về architecture nhưng không có diagram → thiếu shared understanding
- Diagram quá phức tạp (>20 nodes) → cần split thành nhiều views
- Diagram mô tả "current state" mà không có "desired state" → không actionable
- Vẽ diagram sau khi code (should be before)
