# Northstar Service Desk — UI Demo

Giao diện chat Streamlit tích hợp trực tiếp agent loop của bài lab. UI hiển thị phiên bản artifact, provider/model, hội thoại nhiều lượt và toàn bộ tool trace gồm tên tool, input JSON, kết quả hoặc lỗi.

## Cài đặt

Từ thư mục `starter_v0`:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -r UIDemo\requirements.txt
Copy-Item .env.example .env
```

Điền API key của một provider vào `.env`. Không commit file này.

## Chạy UI

```powershell
streamlit run UIDemo\app.py
```

Streamlit sẽ in địa chỉ local, thường là `http://localhost:8501`.

## Cách dùng

1. Chọn provider, version và tùy chọn model trong sidebar.
2. Gửi yêu cầu hoặc chọn một câu gợi ý.
3. Mở từng tool event để xem input và kết quả/lỗi.
4. Tiếp tục trả lời khi agent yêu cầu bổ sung hoặc xác nhận.
5. Chọn **Tải transcript** để lấy evidence JSON.

Transcript cũng được tự động lưu sau mỗi lượt tại `starter_v0/transcripts/`.

## Artifact version

UI ưu tiên các file theo version nếu tồn tại:

- `artifacts/system_prompt_v1.md` và `artifacts/tools_v1.yaml`; hoặc
- `artifacts/v1/system_prompt.md` và `artifacts/v1/tools.yaml`.

Nếu chưa có bản riêng, UI dùng `artifacts/system_prompt.md` và `artifacts/tools.yaml`, nhưng vẫn hiển thị version được chọn cùng hash thực tế để người xem nhận biết artifact.

## An toàn và accessibility

- API key nhập trên UI chỉ nằm trong process hiện tại, không ghi vào transcript.
- Tool error và provider error luôn được hiển thị thay vì bị che.
- UI có focus ring, touch target tối thiểu 44px, responsive mobile và hỗ trợ `prefers-reduced-motion`.
- Ticket vẫn tuân theo xác nhận do agent prompt và `create_ticket` tool kiểm soát.

## Ảnh nền

Ảnh **Sapphire haze** của Alessio Soggetti được lưu cục bộ tại
`UIDemo/assets/sapphire-haze.jpg` và sử dụng theo
[Unsplash License](https://unsplash.com/license). Trang nguồn:
<https://unsplash.com/photos/mountains-cfKC0UOZHJo>.
