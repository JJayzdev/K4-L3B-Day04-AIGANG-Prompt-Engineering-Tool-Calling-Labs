# Kế Hoạch Triển Khai UI Demo (Agent Chat Dashboard)

> **Dự án**: K4-L3B-Day04 Prompt Engineering & Tool Calling Labs  
> **Thư mục**: `starter_v0/UIDemo/`  
> **Mục tiêu**: Xây dựng giao diện UI Chat trực quan đáp ứng 100% tiêu chí Rubric (hiển thị Tool, Input, Kết quả/Lỗi, Version và Transcript).

---

## 1. Yêu Cầu Giao Diện (Theo Rubric & README)

| Tiêu chí | Mô tả chi tiết | Trạng thái hiển thị trên UI |
|---|---|---|
| **Hiển thị Tool** | Tên tool được Agent gọi trong từng lượt (VD: `check_service_status`, `lookup_user`) | Badge / Icon công cụ nổi bật |
| **Hiển thị Input** | Các tham số truyền vào tool dạng JSON được định dạng đẹp | Block Code JSON expandable |
| **Hiển thị Kết quả/Lỗi** | Nội dung trả về từ Tool hoặc thông báo lỗi nếu có | Thẻ thông báo Success (Xanh) / Error (Đỏ) |
| **Hiển thị Version** | Nhãn phiên bản artifact (v0, v1, v2, v3) | Header & Metadata Panel |
| **Lưu Transcript** | Tự động ghi nhận file `.transcript.json` giống `chat.py` | Nút bấm Tải transcript / Auto-save |

---

## 2. Lựa Chọn Công Nghệ (Tech Stack)

* **Framework UI**: **Streamlit** (hoặc **Flask + HTML5/CSS3/Vanilla JS**).
  * *Lý do chọn Streamlit/Flask*: Tích hợp trực tiếp với mã nguồn Python hiện có (`agent.py`, `chat.py`, `providers`, `tools`) mà không cần build phức tạp, hỗ trợ hiển thị JSON và trace log đa lượt dễ dàng.
* **Styling & Theme**: Modern Dark/Light Mode với hiệu ứng thẻ card trực quan cho Tool Call Execution.

---

## 3. Kiến Trúc Cấu Trúc File Trong `UIDemo/`

```text
starter_v0/UIDemo/
├── kehoach.md           # [FILE NÀY] Kế hoạch tổng thể và hướng dẫn chi tiết
├── app.py               # Ứng dụng chính (Streamlit / Flask Web UI)
├── requirements.txt     # Phụ thuộc bổ sung cho UI (streamlit, etc.)
└── README.md            # Hướng dẫn chạy và sử dụng UI
```

---

## 4. Các Bước Triển Khai Chi Tiết (Roadmap)

### Giai đoạn 1: Chuẩn bị & Tích hợp Core Agent Loop
1. Import các module core từ `starter_v0`: `load_lab_env`, `make_provider`, `load_tool_declarations`, `run_model_tool_loop`, `write_transcript`.
2. Khởi tạo Session State lưu trữ lịch sử chat (`history`), thông tin cấu hình (`provider`, `model`, `version`), và log tool calls (`tool_events`).

### Giai đoạn 2: Thiết kế Giao diện Chi tiết
1. **Sidebar (Thanh điều khiển)**:
   * Cho phép chọn Provider (`openrouter`, `openai`, `anthropic`, `gemini`).
   * Chọn Model & nhập API Key (nếu chưa có trong `.env`).
   * Chọn phiên bản Prompt/Tool (`v0`, `v1`, `v2`, `v3`).
   * Hiển thị danh sách các Tool khả dụng trong hệ thống.
2. **Main Area (Khu vực trò chuyện chính)**:
   * **Header**: Tên ứng dụng, nhãn Version hiện tại, chỉ báo trạng thái kết nối.
   * **Chat Feed**: Khung hiển thị tin nhắn của User và Agent.
   * **Tool Trace Card (Nằm ngay bên dưới câu trả lời của Agent)**:
     * Dạng Accordion hoặc Timeline step.
     * Mỗi bước thể hiện: **Tool Name** $\rightarrow$ **Input JSON** $\rightarrow$ **Output/Error Badge**.
   * **Input Box**: Khung nhập liệu câu hỏi từ người dùng.

### Giai đoạn 3: Xử lý Đa Lượt & Clarification (Hỏi lại khi thiếu thông tin)
1. Bắt sự kiện khi tool trả về `awaiting_user: true` (ví dụ `clarify` tool).
2. Hiển thị thông báo chờ thông tin từ người dùng và tự động tiếp tục luồng hội thoại ở lượt kế tiếp.

### Giai đoạn 4: Lưu & Xuất Transcript
1. Sau mỗi lượt tương tác, gọi hàm `write_transcript()` để ghi log vào thư mục `starter_v0/transcripts/`.
2. Thêm nút "Tải xuống Transcript JSON" ngay trên UI để sinh viên dễ dàng thu thập evidence nộp bài.

---

## 5. Hướng Dẫn Chạy UI Demo

```powershell
# 1. Di chuyển vào thư mục starter_v0
cd starter_v0

# 2. Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# 3. Cài đặt dependency UI (nếu dùng Streamlit)
pip install streamlit

# 4. Chạy ứng dụng UI
streamlit run UIDemo/app.py
```

---

## 6. Tiêu Chí Kiểm Thử & Nghiệm Thu UI

- [ ] UI chạy ổn định, không bị crash khi Provider gặp lỗi.
- [ ] Mọi tool call đều hiển thị rõ 3 phần: Tên tool, Input JSON, Output/Error.
- [ ] Nhãn version (`v0`, `v1`,...) được truyền chính xác vào transcript.
- [ ] File transcript được tạo và lưu thành công trong `starter_v0/transcripts/`.
