# 📊 BÁO CÁO GIÁM SÁT & ĐÁNH GIÁ (OBSERVABILITY TRACE LOGS)
*Dành cho Role 5: Observability & Reviewer*

---

## 🎯 1. BẢNG CHẤM ĐIỂM AGENTIC FIT (SCORING MATRIX)

| Tiêu chí | Điểm (1-5) | Lý do đánh giá |
| :--- | :---: | :--- |
| 🧠 **Multi-step Reasoning** | `5/5` | Agent phải suy luận qua nhiều bước: hiểu triệu chứng → kiểm tra dấu hiệu cấp cứu → đặt câu hỏi làm rõ → xác định chuyên khoa phù hợp → xác nhận với bệnh nhân → tra cứu lịch → xác thực danh tính → đặt lịch. Mỗi bước phụ thuộc vào thông tin thu thập ở bước trước. |
| 🛠️ **Tool Interaction** | `5/5` | Agent cần phối hợp nhiều công cụ chuyên biệt như Emergency Detector, Symptom-to-Specialty Mapper, Doctor/Schedule Lookup, Patient Identity Verification, Booking Engine, Notification Service và Human Escalation. Hầu hết quyết định nghiệp vụ đều phải thông qua tool, không thể dựa vào LLM thuần túy.|
| 🔀 **Dynamic Decision** | `4/5` | Luồng xử lý thay đổi liên tục theo ngữ cảnh hội thoại và kết quả từ các tool. Ví dụ: phát hiện cấp cứu thì dừng toàn bộ quy trình đặt lịch để chuyển cấp cứu; thiếu thông tin thì hỏi tiếp; không còn lịch thì đề xuất khung giờ khác; người dùng yêu cầu gặp nhân viên thì chuyển tiếp ngay. |
| ⏳ **Long Horizon** | `3/5` | Đây là quy trình nhiều bước với trạng thái hội thoại kéo dài. Agent phải ghi nhớ ngữ cảnh, quản lý thông tin bệnh nhân, phối hợp nhiều tool và xử lý các nhánh khác nhau cho đến khi hoàn tất đặt lịch hoặc chuyển tiếp sang nhân viên. |
| **TỔNG ĐIỂM FIT** | **17/20** | **KẾT LUẬN: BÀI TOÁN RẤT NÊN DÙNG REACT AGENT!** |

---

## 🔍 2. SO SÁNH PHẢN HỒI (TEST CASE #3)

**Câu hỏi**: *"Tôi thấy mệt mỏi, chán ăn và sụt cân trong 2 tuần qua, không biết nên khám ở đâu."*

### 🤖 Chatbot Baseline:
* **Phản hồi**: *"Chào bạn, rất chia sẻ với tình trạng sức khỏe hiện tại của bạn.

Việc cơ thể mệt mỏi, chán ăn và sụt cân không rõ nguyên nhân trong 2 tuần là những dấu hiệu cảnh báo cơ thể bạn đang gặp vấn đề, có thể liên quan đến nhiều cơ quan khác nhau như hệ tiêu hóa, nội tiết, hoặc suy nhược cơ thể.

Vì tôi là chatbot hỗ trợ thông tin, tôi xin gợi ý lộ trình để bạn đi khám như sau:

### 1. Bạn nên khám chuyên khoa nào?
Tùy vào tình trạng cụ thể, bạn có thể cân nhắc các chuyên khoa sau:
*   **Khoa Nội tổng quát:** Đây là nơi tốt nhất để bắt đầu. Bác sĩ sẽ thăm khám lâm sàng, đánh giá tổng thể và chỉ định các xét nghiệm cơ bản (như xét nghiệm máu, chức năng gan, thận, đường huyết, tuyến giáp...) để tìm nguyên nhân gốc rễ.
*   **Khoa Tiêu hóa:** Nếu bạn cảm thấy chán ăn đi kèm các triệu chứng như đầy hơi, đau bụng, hoặc thay đổi thói quen đại tiện.
*   **Khoa Nội tiết:** Nếu bạn có thêm các triệu chứng như run tay, hồi hộp, vã mồ hôi hoặc nghi ngờ các vấn đề về chuyển hóa (như tiểu đường hoặc tuyến giáp).

### 2. Gợi ý nơi khám bệnh
Tại Việt Nam, bạn có thể lựa chọn các địa chỉ uy tín sau:
*   **Tại các bệnh viện công lập:** Bệnh viện Đại học Y Dược, Bệnh viện Chợ Rẫy (TP.HCM), Bệnh viện Bạch Mai, Bệnh viện Đại học Y Hà Nội (Hà Nội). Đây là những nơi có chuyên môn cao và đầy đủ thiết bị chẩn đoán.
*   **Tại các bệnh viện/phòng khám đa khoa tư nhân uy tín:** Nếu bạn muốn tiết kiệm thời gian chờ đợi, các bệnh viện như Vinmec, Hồng Ngọc, Tâm Anh hoặc các phòng khám đa khoa quốc tế có hệ thống đặt lịch trước rất thuận tiện.

### 3. Lời khuyên trước khi đi khám
Để bác sĩ chẩn đoán chính xác nhất, bạn hãy chuẩn bị thông tin sau:
*   **Ghi chú lại:** Mức cân nặng bạn đã sụt là bao nhiêu kg? Bạn có bị sốt về chiều không? Có khó ngủ hay căng thẳng tâm lý gần đây không?
*   **Nhịn ăn sáng:** Khi đi khám, tốt nhất bạn nên **nhịn ăn sáng** (chỉ uống nước lọc) để sẵn sàng lấy máu xét nghiệm nếu bác sĩ yêu cầu.
*   **Mang theo:** Các loại thuốc hoặc thực phẩm chức năng bạn đang sử dụng (nếu có).

**Lưu ý quan trọng:** Nếu bạn xuất hiện các triệu chứng như khó thở, đau ngực dữ dội, nôn ra máu hoặc ngất xỉu, hãy đến ngay **Phòng cấp cứu** của bệnh viện gần nhất, không nên chờ đợi.

Bạn có muốn tôi hướng dẫn thêm về cách mô tả triệu chứng với bác sĩ để cuộc thăm khám đạt hiệu quả cao nhất không? Chúc bạn sớm tìm ra nguyên nhân và phục hồi sức khỏe!"*
* **Nhận xét**: An toàn nhưng không giải quyết được nhu cầu thực tế của người dùng.

### 🧠 ReAct Agent:
* --- Step 1/8 ---
* Thought: Tôi cần kiểm tra xem các triệu chứng mệt mỏi, chán ăn và sụt cân của người dùng có dấu hiệu cấp cứu hay không.
* Action: detect_emergency["mệt mỏi, chán ăn, sụt cân"]
* Observation: EMERGENCY=FALSE | Chua phat hien dau hieu cap cuu trong mo ta. Co the tiep tuc tu van dat lich thuong.

* --- Step 2/8 ---
* Thought: Vì không có dấu hiệu cấp cứu, tôi cần xác định chuyên khoa phù hợp dựa trên triệu chứng của người dùng.
* Action: map_symptom_to_specialty["mệt mỏi, chán ăn, sụt cân"]
* Observation: Chuyen khoa goi y: Nội tổng quát. Ly do: mo ta co cac dau hieu lien quan: mệt mỏi, chán ăn, sụt cân. Day la goi y khoa kham, khong thay the chan doan bac si.

* --- Step 3/8 ---
* Thought: Tôi đã có thông tin về chuyên khoa phù hợp là Nội tổng quát từ các quan sát trước đó. Để có thể hỗ trợ bạn kiểm tra lịch trống và đặt lịch khám, tôi cần biết ngày bạn dự định đến khám.

* Final Answer: Dựa trên các triệu chứng mệt mỏi, chán ăn và sụt cân mà bạn mô tả, bạn nên đăng ký khám tại chuyên khoa **Nội tổng quát**. Để tôi có thể kiểm tra lịch trống của bác sĩ và hỗ trợ bạn đặt lịch, vui lòng cho biết bạn muốn khám vào ngày nào?
