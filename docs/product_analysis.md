# 🏥 PHÂN TÍCH KIẾN TRÚC SẢN PHẨM: AI AGENT TƯ VẤN CHUYÊN KHOA & ĐẶT LỊCH KHÁM BỆNH
*Góc nhìn Senior AI Product Architect*

---

## 🎯 1. Mục tiêu sản phẩm (Product Goal)

Xây dựng một AI Agent tổng đài (hotline) có khả năng:

- Hiểu mô tả triệu chứng bằng ngôn ngữ tự nhiên của bệnh nhân (không có kiến thức y khoa chuyên môn).
- Định hướng bệnh nhân đến **đúng chuyên khoa** phù hợp với triệu chứng.
- Tự động hoàn tất việc **đặt lịch khám** với bác sĩ/khoa phù hợp, còn lịch trống.
- Giảm tải cho nhân viên tổng đài, giảm thời gian chờ, giảm tỷ lệ đặt sai khoa (phải chuyển khoa lại tại bệnh viện).

> **Lưu ý phạm vi:** Agent **không chẩn đoán bệnh**, không đưa ra lời khuyên điều trị. Vai trò duy nhất là *định tuyến* (routing) và *đặt lịch* (scheduling).

---

## 👥 2. Đối tượng người dùng (Target Users)

| Nhóm | Đặc điểm |
| :--- | :--- |
| Bệnh nhân/người nhà gọi đến | Đa dạng độ tuổi, có thể lớn tuổi, lo lắng, diễn đạt triệu chứng mơ hồ, không rành công nghệ |
| Người đặt hộ (con cái đặt cho cha mẹ) | Cần cung cấp thông tin của người thứ ba → vấn đề xác thực danh tính |
| Nhân viên tổng đài/lễ tân | Người xử lý các ca agent chuyển tiếp (escalation) |
| Bác sĩ/phòng khám | Bên nhận lịch, cần dữ liệu chính xác, không bị double-booking |
| Bộ phận vận hành bệnh viện | Theo dõi log, tỷ lệ đặt đúng khoa, compliance dữ liệu |

---

## 🚶 3. Hành trình người dùng (User Journey)

1. Bệnh nhân gọi hotline → Agent chào hỏi, hỏi lý do gọi.
2. Bệnh nhân mô tả triệu chứng bằng ngôn ngữ tự nhiên (có thể mơ hồ, nhiều triệu chứng cùng lúc).
3. Agent kiểm tra **dấu hiệu khẩn cấp** trước tiên (bắt buộc, không phụ thuộc LLM).
4. Nếu không khẩn cấp → Agent đặt câu hỏi làm rõ (tuổi, thời gian khởi phát, mức độ đau...).
5. Agent xác định chuyên khoa phù hợp, xác nhận lại với bệnh nhân ("Anh/chị có vẻ phù hợp với khoa Tiêu hóa, đúng không ạ?").
6. Agent tra cứu lịch bác sĩ/khoa còn trống.
7. Agent đề xuất 2-3 khung giờ khả dụng.
8. Bệnh nhân chọn giờ → Agent xác thực danh tính (họ tên, SĐT, mã BHYT/CCCD nếu cần).
9. Agent xác nhận lại toàn bộ thông tin trước khi chốt (double-check bắt buộc).
10. Agent gọi Booking Tool để giữ chỗ → nhận mã đặt lịch.
11. Agent gửi xác nhận qua SMS/Zalo/Email.
12. Kết thúc cuộc gọi, hoặc agent hỏi thêm nhu cầu khác.

---

## ⚙️ 4. Yêu cầu chức năng (Functional Requirements)

- Hiểu và trích xuất triệu chứng từ hội thoại tự do, đa lượt (multi-turn).
- Đặt câu hỏi làm rõ khi thông tin không đủ để phân loại chuyên khoa.
- Ánh xạ triệu chứng → chuyên khoa (có thể trả về nhiều khả năng, cần hỏi thêm để thu hẹp).
- Phát hiện dấu hiệu cấp cứu và chuyển hướng ngay lập tức.
- Tra cứu lịch trống theo chuyên khoa/bác sĩ/thời gian mong muốn.
- Đặt lịch, giữ chỗ, tránh trùng lịch (race condition khi nhiều người đặt cùng slot).
- Xác thực danh tính bệnh nhân (đặc biệt khi đặt hộ).
- Gửi xác nhận, nhắc lịch, hỗ trợ hủy/đổi lịch.
- Chuyển tiếp (escalate) sang nhân viên thật khi agent không xử lý được hoặc bệnh nhân yêu cầu.
- Ghi log toàn bộ quyết định và lời gọi công cụ (tool call) phục vụ audit.

---

## 🧩 5. Yêu cầu phi chức năng (Non-functional Requirements)

- **Độ trễ:** phản hồi thoại phải đủ nhanh (thường < 1-2s/lượt) để giữ trải nghiệm hội thoại tự nhiên.
- **Tính sẵn sàng:** hoạt động 24/7 vì liên quan đến sức khỏe.
- **Bảo mật & quyền riêng tư dữ liệu:** tuân thủ Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân (dữ liệu y tế là dữ liệu nhạy cảm) — mã hóa, hạn chế truy cập, minimization.
- **Khả năng kiểm toán (auditability):** mọi quyết định định tuyến/đặt lịch phải truy vết được — ai, khi nào, dựa trên input gì.
- **Độ chính xác/an toàn cao hơn ưu tiên tốc độ:** vì sai sót ảnh hưởng đến sức khỏe con người.
- **Khả năng mở rộng:** chịu tải cao giờ cao điểm (sáng thứ Hai, sau kỳ nghỉ lễ).
- **Đa ngôn ngữ/giọng địa phương** (tiếng Việt các vùng miền, người lớn tuổi nói không rõ ràng).
- **Fallback an toàn:** khi hệ thống lỗi, phải chuyển ngay sang người thật, không được "treo" bệnh nhân.

---

## 🧠 6. Trách nhiệm của Agent (LLM-based Orchestrator)

- Duy trì ngữ cảnh hội thoại đa lượt.
- Diễn giải ngôn ngữ tự nhiên, xử lý mơ hồ, hỏi lại khi cần.
- Quyết định **khi nào** cần gọi tool nào (routing giữa các bước).
- Tổng hợp kết quả từ nhiều tool thành câu trả lời tự nhiên, đồng cảm.
- Nhận diện khi vượt quá khả năng xử lý → gọi Escalation Tool.
- **Không tự ý** đưa ra thông tin lịch bác sĩ, mã đặt lịch, hoặc chẩn đoán nếu chưa có kết quả thực từ tool (chống hallucination).
- Luôn xác nhận lại với người dùng trước hành động không thể đảo ngược (đặt lịch chính thức).

---

## 🛠️ 7. Trách nhiệm của Tools (Deterministic Systems)

| Tool | Vai trò |
| :--- | :--- |
| **Emergency Detector** | Rule-based, quét từ khóa/mẫu triệu chứng nguy hiểm, trả về cờ boolean tuyệt đối |
| **Symptom-to-Specialty Mapper** | Tra cứu bảng ánh xạ triệu chứng ↔ chuyên khoa đã được đội ngũ y khoa duyệt |
| **Doctor/Schedule Lookup** | Truy vấn hệ thống lịch thực tế (nguồn sự thật duy nhất) |
| **Booking/Reservation Engine** | Giao dịch có tính nguyên tử (atomic transaction), chống double-booking |
| **Patient Identity Verification** | Xác minh qua SĐT/CCCD/mã BHYT với hệ thống hồ sơ bệnh nhân |
| **Notification Service** | Gửi SMS/Zalo/Email xác nhận, mã đặt lịch |
| **Human Escalation/Handoff** | Chuyển cuộc gọi/tin nhắn sang nhân viên hoặc tổng đài cấp cứu 115 |

---

## 🤖 8. Quyết định nên do LLM đảm nhiệm

- Hiểu ý định và cảm xúc người dùng từ câu nói tự nhiên, không theo mẫu cố định.
- Quyết định câu hỏi làm rõ tiếp theo khi thông tin chưa đủ.
- Xử lý các trường hợp mô tả nhiều triệu chứng cùng lúc, ưu tiên triệu chứng nào để hỏi trước.
- Diễn đạt lại kết quả tool (lịch trống, tên khoa) thành ngôn ngữ tự nhiên, thân thiện.
- Nhận diện khi cuộc hội thoại đi lệch hướng (hỏi ngoài phạm vi y tế, yêu cầu tư vấn thuốc) → điều hướng lại đúng phạm vi.
- Chọn giữa **các chuyên khoa có khả năng** (ví dụ đau bụng: Tiêu hóa vs Sản phụ khoa vs Ngoại) dựa trên ngữ cảnh hội thoại, nhưng **không tự quyết định cuối cùng** nếu còn mơ hồ — phải hỏi thêm.

---

## 📏 9. Quyết định nên do luật xác định (Deterministic Rules)

- **Phát hiện cấp cứu**: danh sách từ khóa/triệu chứng nguy hiểm (đau ngực, khó thở, liệt nửa người, chảy máu nhiều, mất ý thức...) → luôn override LLM, không được "suy luận thêm".
- **Ánh xạ triệu chứng → chuyên khoa cuối cùng**: dựa trên bảng tra cứu do đội y khoa phê duyệt, không để LLM tự sáng tạo ra chuyên khoa không tồn tại.
- **Kiểm tra lịch trống & đặt lịch**: hoàn toàn thông qua hệ thống giao dịch, không bao giờ để LLM "tự tin" xác nhận giờ mà chưa gọi tool.
- **Xác thực danh tính**: quy tắc cứng (đúng SĐT đã đăng ký, đúng OTP...).
- **Chính sách hủy/đổi lịch** (ví dụ: chỉ được đổi trước 24h): rule cứng, không thương lượng qua ngôn ngữ.
- **Định dạng dữ liệu** (số điện thoại, ngày giờ, mã bệnh nhân): validate cứng trước khi gửi vào hệ thống.
- **Giới hạn số lần thử/spam** để chống lạm dụng hệ thống.

---

## ⚠️ 10. Rủi ro và tình huống thất bại tiềm ẩn

| Rủi ro | Hậu quả |
| :--- | :--- |
| LLM bỏ sót dấu hiệu cấp cứu | **Nguy hiểm tính mạng** — rủi ro nghiêm trọng nhất |
| LLM hallucination về lịch bác sĩ/mã đặt lịch | Bệnh nhân đến nơi không có lịch thật |
| Định tuyến sai chuyên khoa | Bệnh nhân mất thời gian, phải chuyển khoa tại viện |
| Đặt trùng lịch (race condition) | Xung đột lịch, một trong hai bệnh nhân bị từ chối khi đến |
| LLM vượt phạm vi, đưa lời khuyên y khoa/liều thuốc | Rủi ro pháp lý, rủi ro sức khỏe |
| Giả mạo danh tính khi đặt hộ | Lộ thông tin y tế của người khác |
| Rò rỉ dữ liệu nhạy cảm (triệu chứng, SĐT, CCCD) | Vi phạm pháp luật bảo vệ dữ liệu cá nhân |
| Người dùng lớn tuổi không hiểu hội thoại AI | Bỏ cuộc, trải nghiệm kém, cần lối thoát nhanh sang người thật |
| Hệ thống lỗi/timeout đúng lúc khẩn cấp | Không escalate kịp thời |
| Vòng lặp hỏi-đáp vô tận không tiến triển | Bệnh nhân bực bội, cúp máy |

---

## 🛡️ 11. Guardrails bắt buộc

1. **Emergency override tuyệt đối**: bất kỳ tín hiệu cấp cứu nào cũng ngắt luồng hội thoại thông thường và chuyển hướng ngay, không chờ LLM "suy nghĩ thêm".
2. **Không để LLM tự phát sinh dữ liệu nghiệp vụ**: mọi thông tin về lịch, bác sĩ, mã đặt lịch phải đến từ kết quả tool call thực tế, có trích dẫn nguồn.
3. **Xác nhận rõ ràng trước hành động không thể đảo ngược**: bắt buộc người dùng xác nhận (yes/no) trước khi gọi Booking Tool thật sự.
4. **Giới hạn phạm vi nội dung**: chặn/redirect nếu người dùng hỏi chẩn đoán, liều lượng thuốc, tiên lượng bệnh — luôn nhắc "đây không phải tư vấn y khoa".
5. **Luôn có lối thoát sang người thật** bất cứ lúc nào người dùng yêu cầu ("gặp nhân viên").
6. **Xác thực danh tính bắt buộc** trước khi tiết lộ hoặc chỉnh sửa lịch hẹn đã có.
7. **Data minimization & mã hóa**: chỉ lưu trữ dữ liệu cần thiết, mã hóa khi lưu trữ/truyền tải.
8. **Ghi log đầy đủ** (Thought/Action/Observation) để phục vụ audit và điều tra sự cố.
9. **Timeout & fallback rõ ràng**: nếu tool lỗi/timeout, thông báo minh bạch và chuyển người thật, không im lặng hoặc đoán mò.
10. **Giới hạn số vòng hỏi lại** (ví dụ tối đa 3-4 lần làm rõ) trước khi tự động chuyển sang nhân viên hỗ trợ.

---

## 🔁 12. Quy trình suy luận nhiều bước (Multi-step Reasoning Workflow)

Ví dụ minh họa một luồng đặt lịch thành công theo mô hình ReAct (Thought → Action → Observation):

```
Thought: Bệnh nhân vừa nói "Tôi bị đau bụng âm ỉ 3 ngày nay, kèm buồn nôn".
         Trước tiên phải kiểm tra đây có phải dấu hiệu cấp cứu không.
Action: Gọi Emergency Detector Tool(triệu chứng="đau bụng âm ỉ 3 ngày, buồn nôn")
Observation: emergency_flag = FALSE (không thuộc danh sách dấu hiệu nguy hiểm)

Thought: Không phải cấp cứu. Tuy nhiên triệu chứng "đau bụng + buồn nôn"
         có thể ứng với nhiều chuyên khoa (Tiêu hóa, Sản phụ khoa nếu là nữ, Ngoại).
         Cần hỏi thêm để thu hẹp.
Action: Hỏi người dùng "Anh/chị có thể cho biết cơn đau ở vị trí nào
        và anh/chị là nam hay nữ không ạ?"
Observation: Người dùng trả lời "Tôi là nữ, đau ở vùng bụng dưới bên phải"

Thought: Vị trí đau vùng bụng dưới bên phải + giới tính nữ vẫn cần loại trừ
         giữa Tiêu hóa (ví dụ viêm ruột thừa) và Sản phụ khoa.
         Tra cứu bảng ánh xạ triệu chứng để xác định chuyên khoa ưu tiên.
Action: Gọi Symptom-to-Specialty Mapper Tool(vị trí="bụng dưới phải",
        giới_tính="nữ", triệu_chứng=["đau âm ỉ", "buồn nôn"])
Observation: Kết quả trả về: chuyên khoa đề xuất = "Tiêu hóa" (độ tin cậy cao),
             khuyến nghị dự phòng = "Ngoại tổng quát" nếu đau tăng dần

Thought: Đã có chuyên khoa đề xuất, cần xác nhận lại với bệnh nhân trước khi tra lịch.
Action: Hỏi xác nhận "Dựa trên mô tả, tôi đề xuất anh/chị khám chuyên khoa
        Tiêu hóa, anh/chị đồng ý không ạ?"
Observation: Người dùng xác nhận "Vâng, đồng ý"

Thought: Chuyên khoa đã chốt. Bước tiếp theo là tra lịch bác sĩ còn trống.
Action: Gọi Doctor/Schedule Lookup Tool(chuyên_khoa="Tiêu hóa",
        thời_gian_mong_muốn="trong tuần này")
Observation: Trả về 3 khung giờ trống: Thứ 4 (9h), Thứ 5 (14h), Thứ 6 (10h)
             — BS. Nguyễn Văn A

Thought: Có lịch trống, cần trình bày lựa chọn cho bệnh nhân.
Action: Đề xuất "Tôi có các khung giờ sau với BS. Nguyễn Văn A:
        Thứ 4 (9h), Thứ 5 (14h), Thứ 6 (10h). Anh/chị chọn giờ nào?"
Observation: Người dùng chọn "Thứ 5, 14h"

Thought: Trước khi đặt lịch chính thức, cần xác thực danh tính bệnh nhân.
Action: Gọi Patient Identity Verification Tool(SĐT, họ_tên)
Observation: Xác thực thành công, khớp hồ sơ bệnh nhân hiện có

Thought: Mọi điều kiện đã đủ. Cần xác nhận lần cuối trước hành động
         không thể đảo ngược (đặt lịch).
Action: Xác nhận "Tôi sẽ đặt lịch khám Tiêu hóa với BS. Nguyễn Văn A,
        Thứ 5 lúc 14h. Anh/chị xác nhận đặt lịch chứ?"
Observation: Người dùng xác nhận "Đúng rồi, đặt giúp tôi"

Thought: Đã có xác nhận rõ ràng, tiến hành gọi tool đặt lịch giao dịch.
Action: Gọi Booking/Reservation Engine(bác_sĩ="Nguyễn Văn A",
        thời_gian="Thứ 5, 14h", bệnh_nhân_id=...)
Observation: booking_status = SUCCESS, mã_đặt_lịch = "APT-88231"

Thought: Đặt lịch thành công, cần gửi xác nhận và kết thúc quy trình.
Action: Gọi Notification Tool(kênh="SMS/Zalo", nội_dung="Xác nhận lịch khám
        Tiêu hóa - BS. Nguyễn Văn A - Thứ 5, 14h - Mã: APT-88231")
Observation: notification_status = SENT

Thought: Toàn bộ mục tiêu đã hoàn tất (định tuyến đúng khoa + đặt lịch
         thành công + xác nhận đã gửi). Kết thúc phiên.
Action: Thông báo cho người dùng "Lịch khám của anh/chị đã được xác nhận,
        mã đặt lịch APT-88231, tin nhắn xác nhận đã được gửi qua Zalo.
        Anh/chị còn cần hỗ trợ gì thêm không?"
Observation: Người dùng "Không, cảm ơn" → Kết thúc phiên.
```

### 🚨 Nhánh rẽ bắt buộc (deterministic override)

Nếu ở bước đầu tiên `emergency_flag = TRUE`, toàn bộ luồng trên bị hủy ngay lập tức, thay bằng:

```
Thought: Phát hiện dấu hiệu cấp cứu, không được tiếp tục định tuyến bình thường.
Action: Gọi Human/Emergency Escalation Tool → chuyển cuộc gọi sang cấp cứu/115
        hoặc nhân viên trực, đồng thời cảnh báo "Vui lòng gọi ngay 115
        hoặc đến cấp cứu gần nhất".
Observation: Escalation thành công, cuộc gọi được chuyển tiếp.
```
