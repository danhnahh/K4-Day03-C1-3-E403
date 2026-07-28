"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề nhóm: 🏥 ĐẶT LỊCH KHÁM BỆNH & TƯ VẤN CHUYÊN KHOA

⚠️ TRẠNG THÁI: MỐC 1 (Định hình) — đây mới là KHUNG (skeleton) liệt kê 4 tool
   nhóm sẽ xây. Phần logic thật (dữ liệu mock, validate, xử lý lỗi an toàn)
   sẽ được cài đặt ở Mốc 2 (docstring/spec) và Mốc 3 (safe error, không crash).

⚠️ BẢO MẬT: Toàn bộ dữ liệu bệnh nhân/lịch/SĐT/CCCD/BHYT trong file này là
   DỮ LIỆU GIẢ LẬP (MOCK). Tuyệt đối KHÔNG nhập PII thật và KHÔNG commit PII thật.
"""

# =============================================================================
# 📋 DANH SÁCH 4 TOOL (MỐC 1)
# -----------------------------------------------------------------------------
# 1. detect_emergency          — Emergency Detector (rule-based, cờ khẩn cấp)
# 2. map_symptom_to_specialty  — Symptom-to-Specialty Mapper (ánh xạ đã duyệt)
# 3. lookup_doctor_schedule    — Doctor/Schedule Lookup (nguồn sự thật lịch)
# 4. verify_patient_identity   — Patient Identity Verification (SĐT/CCCD/BHYT)
# =============================================================================


def detect_emergency(symptom: str) -> str:
    """
    🚨 [Tool 1] EMERGENCY DETECTOR — Sàng lọc dấu hiệu nguy hiểm (rule-based).

    Purpose : Quét từ khóa/mẫu triệu chứng nguy hiểm TRƯỚC mọi bước khác. Nếu
              phát hiện cấp cứu -> khuyến cáo gọi 115 / tới cấp cứu, KHÔNG đi
              tiếp luồng đặt lịch thường.
    Input   : symptom (str) — mô tả triệu chứng của người dùng.
    Output  : str có token cờ tuyệt đối:
              "EMERGENCY=TRUE | ..."  hoặc  "EMERGENCY=FALSE | ...".
    Error   : Input rỗng/không hợp lệ -> trả chuỗi lỗi, KHÔNG raise.
    Side eff: Read-only.
    """
    # TODO (Mốc 2/3): danh sách từ khóa nguy hiểm + trả cờ EMERGENCY=TRUE/FALSE
    return "[TODO Mốc 2/3] detect_emergency chưa được cài đặt."


def map_symptom_to_specialty(symptom: str) -> str:
    """
    🧭 [Tool 2] SYMPTOM-TO-SPECIALTY MAPPER — Ánh xạ triệu chứng -> chuyên khoa.

    Purpose : Tra bảng ánh xạ (đã được đội ngũ y khoa duyệt) để gợi ý KHÁM KHOA
              nào. Đây là gợi ý định tuyến, KHÔNG phải chẩn đoán/kê đơn.
    Input   : symptom (str) — mô tả triệu chứng.
    Output  : str — tên chuyên khoa gợi ý + 1 dòng lý do + câu miễn trừ.
    Error   : Không đủ dữ kiện/không khớp -> chuỗi lỗi gợi ý mô tả rõ hơn.
    Side eff: Read-only.
    """
    # TODO (Mốc 2/3): bảng ánh xạ triệu chứng ↔ chuyên khoa
    return "[TODO Mốc 2/3] map_symptom_to_specialty chưa được cài đặt."


def lookup_doctor_schedule(specialty: str, date: str) -> str:
    """
    📅 [Tool 3] DOCTOR/SCHEDULE LOOKUP — Nguồn sự thật duy nhất về lịch.

    Purpose : Truy vấn bác sĩ trong 1 chuyên khoa và các khung giờ còn trống
              vào 1 ngày cụ thể.
    Input   : specialty (str) — tên chuyên khoa; date (str) — ngày cần khám.
    Output  : str — danh sách bác sĩ + slot trống.
    Error   : Khoa không tồn tại -> liệt kê khoa hợp lệ; ngày sai định dạng/
              vô lý (vd 32/13) hoặc quá khứ -> chuỗi lỗi. KHÔNG raise.
    Side eff: Read-only.
    """
    # TODO (Mốc 2/3): dữ liệu mock bác sĩ + slot, validate khoa & ngày
    return "[TODO Mốc 2/3] lookup_doctor_schedule chưa được cài đặt."


def verify_patient_identity(identifier: str, id_type: str = "phone") -> str:
    """
    🪪 [Tool 4] PATIENT IDENTITY VERIFICATION — Xác minh danh tính bệnh nhân.

    Purpose : Xác minh người đặt lịch qua SĐT / CCCD / mã BHYT trước khi cho
              phép đặt lịch (cổng danh tính).
    Input   : identifier (str) — số định danh; id_type (str) — "phone"|"cccd"|"bhyt".
    Output  : str — kết quả xác minh (che bớt số khi hiển thị để bảo vệ PII).
    Error   : Sai định dạng / không tìm thấy hồ sơ -> chuỗi lỗi. KHÔNG raise.
    Side eff: Read-only (chỉ tra cứu hồ sơ mock).
    """
    # TODO (Mốc 2/3): hồ sơ bệnh nhân mock + validate định dạng + masking
    return "[TODO Mốc 2/3] verify_patient_identity chưa được cài đặt."


# Danh sách các tool được đăng ký để Agent (Role 4) sử dụng
AVAILABLE_TOOLS = {
    "detect_emergency": detect_emergency,
    "map_symptom_to_specialty": map_symptom_to_specialty,
    "lookup_doctor_schedule": lookup_doctor_schedule,
    "verify_patient_identity": verify_patient_identity,
}
