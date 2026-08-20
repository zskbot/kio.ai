# KIO.ai — Design System

KIO là một router, không phải một chatbot có logo. Giao diện phải trông giống
**bảng điều khiển của một mạch định tuyến tín hiệu** — nơi một tác vụ đi vào,
được chấm điểm, rẽ nhánh qua skill/tool, quét workspace, rồi thoát ra dưới
dạng JSON. Mọi quyết định màu sắc, chữ, và bố cục bên dưới đều phục vụ ẩn dụ đó.

---

## 1. Color tokens

| Token | Hex | Vai trò |
|---|---|---|
| `--bg` | `#0B0F14` | Nền gốc — mực xanh đen sâu, không phải đen thuần |
| `--panel` | `#10161D` | Panel trái/phải (Agent Activity, Workspace) |
| `--card` | `#171F29` | Thẻ nổi: skill chip, file item, card, bubble |
| `--border` | `#1E2733` | Viền mặc định giữa các panel |
| `--border-hover` | `#2B3644` | Viền khi hover / focus |
| `--signal` | `#FF8A3D` | Amber/copper — tín hiệu chính đang chạy qua router (trạng thái WORKING, plan-item active, con trỏ trace) |
| `--signal-dim` | `#8A4E28` | Amber đã tắt / bước đã đi qua nhưng không còn active |
| `--wire` | `#3FD2C7` | Teal — dây phụ: tool/kết nối, MCP, plugin đã CONNECTED |
| `--wire-dim` | `#1F5F59` | Teal mờ — kết nối idle |
| `--text` | `#E8ECF1` | Chữ chính |
| `--text-muted` | `#6B7684` | Nhãn phụ, timestamp, placeholder |
| `--text-faint` | `#3E4753` | Trạng thái rỗng, chữ gần như ẩn |
| `--success` | `#7FDBA0` | DONE / STAGED / ✓ |
| `--error` | `#E8697D` | ERROR / ✗ |

Nguyên tắc: **amber và teal không bao giờ xuất hiện làm màu nền lớn** — chúng
chỉ là tín hiệu chạy trên nền tối, giống LED trên một bo mạch. Nếu một màn
hình có nhiều hơn một điểm amber "đang chạy" cùng lúc, đó là lỗi thiết kế —
signal luôn duy nhất tại một thời điểm, đúng bản chất một request đi qua router.

---

## 2. Typography

| Vai trò | Font | Dùng cho |
|---|---|---|
| Nhãn / route / badge / code | **JetBrains Mono** | `.section-title`, `.plan-item`, `.file-item`, `.skill-chip`, `.console .log`, trạng thái `READY / WORKING / DONE`, ID plugin |
| Nội dung đọc | **IBM Plex Sans** | Heading trang (`Skills`, `Tools`, `Plugins`), mô tả card, tin nhắn chat, câu dẫn ở start screen |

JetBrains Mono mang cảm giác "đây là log thật, không phải trang trí" — đúng
tinh thần một router hiển thị route thật. IBM Plex Sans chỉ xuất hiện ở nơi
người dùng *đọc*, không phải nơi họ *giám sát*.

Scale gợi ý: nhãn mono 9–11px, letter-spacing `.08em–.1em`, uppercase cho
section title; nội dung Plex Sans 12–14px cho copy, 22–28px cho heading trang
(`letter-spacing:-.03em`).

---

## 3. Signature: Router Trace

Đây là yếu tố nhận diện xuyên suốt — dùng ở docs, ở trạng thái loading của
start screen, và có thể làm hoạt ảnh nền cho panel "Agent Activity" khi
`agentStatus = WORKING`.

Router Trace vẽ đúng luồng thật trong `agent_router.py::route()`:

```
Task → normalize → select_skills / select_tools → inspect_workspace
     → choose_files → make_plan → JSON
```

### ASCII layout (dùng để dựng SVG/HTML)

```
[Task] ──▶ (normalize) ──▶ ⟨select_skills⟩
                                │
                          ⟨select_tools⟩
                                │
                                ▼
                        (inspect_workspace)
                                │
                                ▼
                          [choose_files]
                                │
                                ▼
                          (make_plan)
                                │
                                ▼
                            { JSON }
```

Quy ước ký hiệu:

- `[ ]` khối vuông — điểm vào/ra (Task, choose_files, JSON output)
- `( )` khối bo tròn — bước xử lý thuần router (normalize, inspect_workspace, make_plan)
- `⟨ ⟩` khối hình thoi/lệch — điểm rẽ nhánh chấm điểm (select_skills, select_tools) — đây là nơi amber tách thành hai teal, vì từ một tín hiệu, router chọn ra nhiều skill/tool song song

### Màu trong trace

- Đường nối chính (Task → JSON): `--signal` (amber), vẽ dưới dạng `stroke-dasharray`
  chạy animation `stroke-dashoffset` liên tục — đây là "tín hiệu đang chạy qua router".
- Hai nhánh `select_skills` / `select_tools`: `--wire` (teal), tách ra từ node
  amber rồi nhập lại — thể hiện đây là tool/kết nối được router gọi tới, không
  phải bước tuần tự của chính router.
- Node đã đi qua: viền `--signal-dim`. Node đang active: viền `--signal` + glow
  nhẹ (`box-shadow: 0 0 12px rgba(255,138,61,.35)`).
- Output `{ JSON }`: viền `--success` khi hoàn tất, `--error` nếu route lỗi.

### Nơi dùng

| Vị trí | Cách dùng |
|---|---|
| Trang docs (đầu file này) | Router Trace tĩnh, làm banner giải thích kiến trúc — thay cho `architecture.svg` hiện tại |
| Start screen (`#startScreen`), lúc gõ task và bấm gửi | Trace chạy 1 lần từ trái sang phải trong lúc chờ `/api/task`, thay cho spinner mặc định |
| `.agent-panel` khi `agentStatus = WORKING` | Một dải trace thu nhỏ (chỉ đường amber, không nhãn) chạy ngang dưới `.panel-header`, dừng lại khi `DONE` |
| README / marketing | Bản đầy đủ, có nhãn tên hàm, dùng làm hình đại diện dự án |

Router Trace **không** dùng numbered markers (01/02/03) — thứ tự đã được mã hoá
bằng chính hướng mũi tên và tên hàm thật, thêm số sẽ là trang trí thừa.

---

## 4. Component mapping (áp cho HTML hiện có)

| Class hiện tại | Token áp dụng |
|---|---|
| `.plan-item.active .plan-dot` | nền `--signal`, glow amber — đây chính là "vị trí hiện tại của tín hiệu" trong plan |
| `.skill-chip` | viền `--wire-dim`, icon `◇` màu `--wire` — skill là một nhánh teal đã chọn |
| `.file-status.WORKING` | `--signal` |
| `.file-status.DONE / .STAGED` | `--success` |
| `.status.connected` (Plugins) | `--wire` — plugin connected = dây đang dẫn tín hiệu |
| `.log.success` | `--success`; `.log.error` | `--error`; log thường | `--text-muted` |
| `.send` (nút gửi) | nền `--signal`, chữ `--bg` — nút gửi tự nó là điểm khởi phát tín hiệu |
| `#agentStatus = WORKING` | chữ `--signal`, có thể thêm chấm nhấp nháy amber phía trước |

---

## 5. Việc tiếp theo

1. Viết lại `style.css` theo token bảng trên (giữ nguyên toàn bộ class/id đang
   dùng trong `index.html` và `app.js` — không đổi cấu trúc DOM).
2. Dựng component Router Trace dưới dạng SVG (`assets/router-trace.svg`) +
   một bản animate nhúng trong `app.js` cho trạng thái WORKING.
3. Thay `assets/architecture.svg` trong README bằng bản Router Trace đầy đủ.

Xác nhận bạn muốn mình làm bước 1 (viết lại `style.css`) tiếp theo, hay ưu
tiên bước 2 (SVG Router Trace) trước.