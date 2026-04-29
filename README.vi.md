# AntiWF_FIN - Antigravity Workflow Framework v4.0

[English](README.md)

AntiWF_FIN là bộ hệ thống AWF v4 dành cho Antigravity, gồm các workflow slash-command toàn cục, skill tái sử dụng, schema, template và manifest trung tâm để định tuyến yêu cầu của người dùng vào đúng workflow và bộ skill phù hợp.

## Nguồn Sự Thật

| File | Vai trò |
| --- | --- |
| `awf_manifest.yaml` | Router trung tâm cho workflows, skills, gates, risk levels và handoff paths |
| `global_workflows/references/CORE_OPERATING_GUIDE.md` | Thứ tự đọc nhẹ và quy tắc tiết kiệm context trước khi mở workflow hoặc skill dài |
| `global_workflows/GLOBAL_SAFETY_TRUTHFULNESS_GATE.md` | Gate bắt buộc về tính trung thực và an toàn cho claim, chỉnh sửa, deploy, publishing, research và content |
| `global_workflows/CONTEXT_SYSTEM.md` | Hợp đồng memory chuẩn cho các file trong `.brain/` |
| `schemas/*.schema.json` | Hợp đồng máy đọc được cho các file memory của AWF |
| `templates/*.example.json` | File ví dụ khớp với schema và context contract |

## Nhóm Workflow

Luồng phát triển phần mềm chính:

```text
/init -> /brainstorm -> /plan -> /design -> /visualize -> /code -> /run -> /test -> /audit -> /deploy
```

Bảo trì và khôi phục:

```text
/recap -> /next -> /debug -> /refactor -> /rollback -> /save-brain
```

Content và publishing:

```text
/script -> /fb-post
```

## Cam Kết Của AWF v4

- Mọi workflow quan trọng đều đi qua `awf_manifest.yaml`.
- Các claim quan trọng về sự thật hoặc thuyết phục phải đi qua global truthfulness gate.
- Durable memory chỉ được ghi qua `/save-brain`.
- Checkpoint nhẹ được ghi append-only vào `session_log.txt`.
- Fact, decision và unverified claim được tách riêng.
- Workflow high-risk và critical phải khai báo yêu cầu confirmation trong manifest.

## File Context

AWF v4 dùng `.brain/` làm thư mục memory cục bộ của dự án:

```text
.brain/
  brain.json          Fact ổn định đã được repo/user xác nhận
  session.json        Trạng thái công việc hiện tại
  session_log.txt     Checkpoint nhẹ dạng append-only
  handover.md         Bàn giao phiên khi context dài hoặc bắt đầu việc rủi ro
  decisions.md        Decision log dạng append-only
  claims.md           Claim ledger cho assumption và khoảng trống kiểm chứng
  preferences.json    Preference cục bộ về giao tiếp và phong cách làm việc
```

Dùng các file trong `templates/` làm điểm bắt đầu và validate với `schemas/`.

## Cài Đặt

Sao chép các thư mục và file lõi vào thư mục dữ liệu Antigravity:

```text
global_workflows/
skills/
schemas/
templates/
plugins/
awf_manifest.yaml
mcp_config.json
```

Vị trí Windows thường dùng:

```text
%USERPROFILE%\.gemini\antigravity\
```

## Kiểm Tra

Chạy validator AWF sau khi thay đổi workflows, skills, schemas, templates hoặc `awf_manifest.yaml`:

```bash
python -m pip install -r requirements-dev.txt
python tools/validate_awf.py --strict
```

Validator này hỗ trợ AWF extended frontmatter như `risk_level`, `required_gates`, `allowed_side_effects` và `related_workflows`.

## Ghi Chú

- `fb-publisher` được giữ là skill publishing private/local.
- Runtime data, cache folder, local session data, log và secret không nên đưa vào commit mới trừ khi chủ động version hóa.
- Sau khi thay đổi metadata của workflow hoặc skill, hãy validate để chắc mọi path trong `awf_manifest.yaml` còn tồn tại.
