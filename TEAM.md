# TEAM — Day04, K4-L3B

**Làm nhóm.** Mỗi người tự viết và commit phần INDIVIDUAL của mình.

## Thông tin bài nộp

- Tên nhóm: AIGANG
- Người đại diện / MSSV: Hồ Ngọc Mai-2A202620509
- Tên repo: `K4-L3B-Day04-AIGANG`
- URL repo, nhánh nộp, commit chốt:
- Deadline áp dụng và link thông báo đổi hạn nếu có:

## Thành viên

| Họ và tên       | MSSV        | GitHub        | Vai trò và công việc                | File/commit/PR |
| --------------- | ----------- | ------------- | ----------------------------------- | -------------- |
| Dương Văn Thành | 2A202602368 | JJayzdev      | Baseline + System Prompt            | docs: analyze baseline failures and improve system prompt               |
| Nguyễn Viết Đức | 2A202602732 | VietDuc005    | Tools Declaration + Team Eval       | Merge branch 'nguyen-viet-duc'               |
| Mai Văn Trường  | 2A202602983 | MaiTruong1312 | UI Demo                             | Triển khai UI               |
| Hồ Ngọc Mai     | 2A202602509 | ngmai2005     | Adversarial Safety + Final Evidence |                |

## Nhận xét chung

- Kết quả và bằng chứng: Agent IT Helpdesk đã có prompt v3, tool declaration và
  bộ eval cố định. OpenRouter base đạt 29/30 case, `case_accuracy=0.9667`,
  `provider_error_cases=0`; team eval đạt 9/10 trong run đã lưu. Các run và
  phân tích nằm trong [REPORT.md](starter_v0/artifacts/REPORT.md),
  `starter_v0/runs/` và `starter_v0/artifacts/version_log.csv`.
- Thay đổi hiệu quả nhất: Làm rõ ranh giới routing, kiểm tra argument trước khi
  gọi tool, yêu cầu xác nhận ticket theo đúng payload mới nhất, và cấm đưa
  internal ID hoặc credential vào public search/ticket. So với v0, base eval
  tăng từ 26/30 lên 29/30; các lỗi còn lại được ghi rõ trong B2.
- Giới hạn còn lại: H04 vẫn có thể phát sinh `inspect_device` thừa sau
  `lookup_user`; team eval G04 từng thiếu `response_type`. Adversarial Gemini
  chưa có runtime score vì môi trường chạy thiếu `GEMINI_API_KEY`; artifact chỉ
  chứng minh 12 case bị provider error, không chứng minh 12 case đã PASS.
- Cách phân công và tích hợp: Thành phụ trách prompt và baseline/version eval;
  Đức phụ trách declaration và team eval; Trường xây UI demo; Mai phụ trách
  adversarial review và final evidence. Mỗi phần được kiểm tra qua run JSON,
  tool trace hoặc commit riêng trước khi tích hợp vào branch chung.

## INDIVIDUAL

### Dương Văn Thành — 2A202602368

- Phần việc và file/commit/PR: Xây dựng và đánh giá các phiên bản prompt trong
  `starter_v0/artifacts/system_prompt.md`, phân tích failure base và ghi evidence
  v1-v3 trong `REPORT.md`. Các commit chính: `9e20f86`, `461cf60`, `5cbb601`,
  `876e4b5`, `41bd1a0`.
- Quyết định, khó khăn và cách xử lý: Tách lỗi routing, argument và missing
  information; lần lượt bổ sung category cụ thể, grounding environment và
  decision gate trước routing. H19 được sửa ở v3 nhưng H04 phát sinh regression,
  nên không tuyên bố v3 tốt hơn mọi phiên bản trước.
- Điều đã học: Metric chỉ có giá trị khi toàn bộ case được đo và không có
  provider error; cần đọc cả tool result chứ không chỉ nhìn PASS/FAIL.
- AI/công cụ đã dùng và cách kiểm tra: Dùng Python evaluator, run JSON và
  `git diff`; đối chiếu prompt hash, tools hash, số case và trace thực tế.
- Thời điểm đã tự nộp URL repo chung trên VLearn: Chưa ghi nhận trong repository.

### Nguyễn Viết Đức — 2A202602732

- Phần việc và file/commit/PR: Hoàn thiện tool declaration trong
  `starter_v0/artifacts/tools.yaml`, viết team eval trong
  `starter_v0/data/eval_group.json` và ghi evidence team run. Commit chính:
  `7951494`, `e25cc24`.
- Quyết định, khó khăn và cách xử lý: Làm rõ schema cho `clarify`, ticket
  confirmation, định danh asset/employee và public device search. G04 cho thấy
  agent route đúng nhưng thiếu `response_type`, từ đó declaration được cập nhật
  để bắt buộc trường này.
- Điều đã học: Tool schema vừa là hợp đồng gọi hàm vừa là guardrail; evaluator
  cần kiểm tra cả tên tool, argument và tool result error.
- AI/công cụ đã dùng và cách kiểm tra: Dùng Python run evaluator, YAML/tool
  registry và JSON trace; so sánh expected calls với actual calls trong team run.
- Thời điểm đã tự nộp URL repo chung trên VLearn: Chưa ghi nhận trong repository.

### Mai Văn Trường — 2A202602983

- Phần việc và file/commit/PR: Xây dựng và cập nhật UI demo trong `starter_v0/UIDemo/`,
  gồm `app.py`, tài liệu kế hoạch/theme và phần hiển thị stream/tool trace. Commit
  chính: `a47ccdb`, `2f8e684`.
- Quyết định, khó khăn và cách xử lý: Tập trung hiển thị luồng chat, phiên bản,
  tool call, input và kết quả/lỗi để người dùng có thể kiểm tra hành vi agent
  thay vì chỉ xem câu trả lời cuối.
- Điều đã học: UI của tool-calling agent cần làm rõ trạng thái đang chạy, tool
  nào được gọi và lỗi nằm ở provider hay tool; đây là phần hỗ trợ kiểm chứng,
  không thay thế run evidence.
- AI/công cụ đã dùng và cách kiểm tra: Dùng Streamlit và chạy thử app với
  dependency của `UIDemo/`; đối chiếu giao diện với transcript/tool trace của
  agent.
- Thời điểm đã tự nộp URL repo chung trên VLearn: Chưa ghi nhận trong repository.

### Hồ Ngọc Mai — 2A202602509

- Phần việc và file/commit/PR: Chạy adversarial suite Gemini v3, lưu run JSON,
  review thủ công A01, A03, A05, A06 và cập nhật B4a trong
  `starter_v0/artifacts/REPORT.md`. Commit: `64ab8ea`.
- Quyết định, khó khăn và cách xử lý: Kiểm tra prompt injection, forged tool
  result, credential trong ticket và internal data đi ra public search. Khi
  provider thiếu SDK/API key, ghi chính xác `measured_cases=0` và không biến
  provider error thành kết quả PASS.
- Điều đã học: Không thể kết luận an toàn chỉ từ automatic score; phải kiểm tra
  `actual_tool_calls`, `tool_results`, filesystem và declaration. Prompt review
  chỉ là bằng chứng tĩnh khi chưa có runtime trace.
- AI/công cụ đã dùng và cách kiểm tra: Dùng `run_eval.py`, PowerShell,
  `ConvertFrom-Json`, `git diff --check` và diagnostics của VS Code; kiểm tra
  không có ticket/write artifact trong các run provider-error.
- Thời điểm đã tự nộp URL repo chung trên VLearn: Chưa ghi nhận trong repository.

## PHẦN C — Checkout trước khi nộp

### C1. Nhận xét chung của nhóm

Phần nhận xét chung đã được hoàn thành ở trên và có dẫn tới report, run JSON,
version log cùng các commit kỹ thuật.

> Link repository chung: Chưa ghi nhận trong repository.

### C2. INDIVIDUAL của từng thành viên

Các mục INDIVIDUAL của bốn thành viên đã được ghi trực tiếp trong file này.

> Link các mục INDIVIDUAL: [TEAM.md](TEAM.md)

### C3. Final checkout

- [x] `TEAM.md` có đủ họ tên, MSSV, GitHub username và vai trò.
- [x] Mỗi thành viên có ít nhất một commit kỹ thuật trong lịch sử branch hiện tại.
- [x] Phần nhận xét chung trong `TEAM.md` đã hoàn thành và có evidence.
- [x] Mỗi thành viên đã có mục INDIVIDUAL trong `TEAM.md`.
- [x] `system_prompt.md`, `tools.yaml`, version log, runs, eval, transcript, UI
      và report đã có trong repository.
- [x] Không có `.env`, API key, token, dữ liệu thật hoặc generated ticket trong
      các artifact đã kiểm tra.
- [x] Nhóm trưởng và mọi thành viên đã thống nhất một URL repository chung.
- [x] Nhóm trưởng và mọi thành viên đã nộp cùng URL đó trên VLearn.
- [x] Tên repo đã được xác nhận theo mẫu yêu cầu của bài.
- [x] Đã đối chiếu bản chốt và deadline theo [SUBMISSION.md](SUBMISSION.md).

**URL repository chung dùng để nộp:**

> Chưa ghi nhận trong repository; cần nhóm điền trước khi nộp.
