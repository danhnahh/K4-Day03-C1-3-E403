"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Chủ đề nhóm: 🏥 ĐẶT LỊCH KHÁM BỆNH & TƯ VẤN CHUYÊN KHOA

✅ TRẠNG THÁI: MỐC 3 (ReAct Loop & Safeguards)
   - Docstring chuẩn 8 trường contract (từ Mốc 2).
   - Đã bọc try/except + validate input cho cả 4 tool.
   - Khi gặp lỗi → trả chuỗi "LỖI: ..." chứ KHÔNG raise exception.
   - Logic nghiệp vụ (mock data, tra cứu) sẽ bổ sung sau.

⚠️ BẢO MẬT: Toàn bộ dữ liệu bệnh nhân/lịch/SĐT/CCCD/BHYT trong file này là
   DỮ LIỆU GIẢ LẬP (MOCK). Tuyệt đối KHÔNG nhập PII thật và KHÔNG commit PII thật.
"""

# =============================================================================
# 📋 DANH SÁCH 4 TOOL
# -----------------------------------------------------------------------------
# 1. detect_emergency          — Emergency Detector (rule-based, cờ khẩn cấp)
# 2. map_symptom_to_specialty  — Symptom-to-Specialty Mapper (ánh xạ đã duyệt)
# 3. lookup_doctor_schedule    — Doctor/Schedule Lookup (nguồn sự thật lịch)
# 4. verify_patient_identity   — Patient Identity Verification (SĐT/CCCD/BHYT)
# =============================================================================


def detect_emergency(symptom: str) -> str:
    """🚨 [Tool 1] EMERGENCY DETECTOR — Sàng lọc dấu hiệu nguy hiểm (rule-based).

    Contract (8 trường):
      • Name        : detect_emergency
      • Purpose     : Quét từ khóa/mẫu triệu chứng nguy hiểm NGAY Ở BƯỚC ĐẦU,
                      trước khi tư vấn khoa hay đặt lịch. Dùng khi người dùng mô
                      tả triệu chứng. KHÔNG dùng để chẩn đoán bệnh cụ thể.
      • Input       : symptom (str, required) — mô tả triệu chứng.
      • Output      : str có token cờ tuyệt đối ở đầu chuỗi để Agent parse chắc
                      chắn:
                        "EMERGENCY=TRUE | <khuyến cáo gọi 115 / tới cấp cứu>"
                        "EMERGENCY=FALSE | <an toàn, có thể tiếp tục đặt lịch>"
      • Error       : symptom rỗng/None/không phải chuỗi -> trả chuỗi lỗi
                      "LỖI: ...", KHÔNG raise exception.
      • Side-effect : Read-only (không thay đổi trạng thái).
      • Example     : detect_emergency("Tôi bị đau tức ngực, khó thở")
                      -> "EMERGENCY=TRUE | Dấu hiệu nguy hiểm (đau ngực, khó
                          thở). Gọi 115 hoặc tới cấp cứu ngay, không đặt lịch
                          hẹn thường."
      • Safety      : Bọc toàn bộ trong try/except, mọi nhánh đều return str.

    Args:
        symptom (str): Mô tả triệu chứng của người dùng.

    Returns:
        str: Chuỗi bắt đầu bằng "EMERGENCY=TRUE|FALSE" hoặc "LỖI: ...".
    """
    try:
        # --- Validate input ---
        if symptom is None:
            return "LỖI: Tham số 'symptom' không được để trống (None)."
        if not isinstance(symptom, str):
            return "LỖI: Tham số 'symptom' phải là chuỗi (str)."
        symptom_clean = symptom.strip()
        if not symptom_clean:
            return "LỖI: Tham số 'symptom' không được để trống."

        # TODO: Bổ sung logic quét từ khóa nguy hiểm + trả cờ EMERGENCY=TRUE/FALSE
        return "[TODO] detect_emergency — logic chưa được cài đặt."
    except Exception as e:
        return f"LỖI: Lỗi không xác định trong detect_emergency — {e}"


def map_symptom_to_specialty(symptom: str) -> str:
    """🧭 [Tool 2] SYMPTOM-TO-SPECIALTY MAPPER — Ánh xạ triệu chứng -> chuyên khoa.

    Contract (8 trường):
      • Name        : map_symptom_to_specialty
      • Purpose     : Tra bảng ánh xạ (đã được đội ngũ y khoa duyệt) để GỢI Ý
                      KHÁM KHOA nào. Dùng sau khi detect_emergency báo an toàn.
                      Đây là gợi ý ĐỊNH TUYẾN, KHÔNG phải chẩn đoán/kê đơn.
      • Input       : symptom (str, required) — mô tả triệu chứng.
      • Output      : str — tên chuyên khoa gợi ý + 1 dòng lý do + câu miễn trừ
                      "Đây là gợi ý khoa khám, không thay thế chẩn đoán bác sĩ."
      • Error       : symptom rỗng/quá ngắn/không đủ dữ kiện -> chuỗi lỗi mời mô
                      tả rõ hơn (vị trí, biểu hiện). KHÔNG raise.
      • Side-effect : Read-only.
      • Example     : map_symptom_to_specialty("đau răng, ê buốt khi ăn lạnh")
                      -> "Chuyên khoa gợi ý: Răng-Hàm-Mặt. Lý do: triệu chứng
                          liên quan răng/nướu. (Đây là gợi ý khoa khám, không
                          thay thế chẩn đoán bác sĩ.)"
      • Safety      : Bọc try/except, mọi nhánh đều return str.

    Args:
        symptom (str): Mô tả triệu chứng của người dùng.

    Returns:
        str: Tên chuyên khoa gợi ý kèm lý do + miễn trừ, hoặc "LỖI: ...".
    """
    try:
        # --- Validate input ---
        if symptom is None:
            return "LỖI: Tham số 'symptom' không được để trống (None)."
        if not isinstance(symptom, str):
            return "LỖI: Tham số 'symptom' phải là chuỗi (str)."
        symptom_clean = symptom.strip()
        if len(symptom_clean) < 2:
            return (
                "LỖI: Mô tả triệu chứng quá ngắn. Vui lòng mô tả rõ hơn "
                "(vị trí đau, biểu hiện cụ thể, thời gian) để gợi ý khoa khám chính xác."
            )

        # TODO: Bổ sung bảng ánh xạ triệu chứng ↔ chuyên khoa + logic tra cứu
        return "[TODO] map_symptom_to_specialty — logic chưa được cài đặt."
    except Exception as e:
        return f"LỖI: Lỗi không xác định trong map_symptom_to_specialty — {e}"


def lookup_doctor_schedule(specialty: str, date: str) -> str:
    """📅 [Tool 3] DOCTOR/SCHEDULE LOOKUP — Nguồn sự thật duy nhất về lịch.

    Contract (8 trường):
      • Name        : lookup_doctor_schedule
      • Purpose     : Truy vấn danh sách bác sĩ trong 1 chuyên khoa và các khung
                      giờ còn trống vào 1 ngày cụ thể. Dùng sau khi đã xác định
                      được chuyên khoa. Đây là nguồn sự thật (single source of
                      truth) — không được để LLM tự bịa lịch.
      • Input       : specialty (str, required) — tên chuyên khoa (vd
                      "Răng-Hàm-Mặt"); date (str, required) — ngày cần khám,
                      định dạng chấp nhận: dd/mm/yyyy hoặc yyyy-mm-dd.
      • Output      : str — danh sách bác sĩ + các slot giờ trống của ngày đó.
      • Error       : Khoa không tồn tại -> "LỖI: ..." kèm LIỆT KÊ khoa hợp lệ
                      để Agent tự sửa hướng; ngày sai định dạng/không có thật
                      (vd 32/13/2026)/đã qua -> "LỖI: ...". KHÔNG raise.
      • Side-effect : Read-only (chỉ tra cứu, không giữ chỗ/đặt lịch).
      • Example     : lookup_doctor_schedule("Răng-Hàm-Mặt", "29/07/2026")
                      -> "Khoa Răng-Hàm-Mặt ngày 29/07/2026:\\n- BS. Trần Văn
                          Hùng: 08:00, 09:30, 14:00\\n- BS.CKI Lê Thị Mai:
                          10:30, 15:30"
      • Safety      : Bọc try/except; validate khoa & ngày trước khi tra.

    Args:
        specialty (str): Tên chuyên khoa cần tra.
        date (str): Ngày cần khám (dd/mm/yyyy hoặc yyyy-mm-dd).

    Returns:
        str: Danh sách bác sĩ + slot trống, hoặc "LỖI: ...".
    """
    try:
        # --- Validate specialty ---
        if specialty is None or not isinstance(specialty, str) or not specialty.strip():
            return "LỖI: Tên chuyên khoa không được để trống."

        # --- Validate date ---
        if date is None or not isinstance(date, str) or not date.strip():
            return "LỖI: Ngày khám không được để trống. Vui lòng nhập theo định dạng dd/mm/yyyy hoặc yyyy-mm-dd."

        # TODO: Bổ sung dữ liệu bác sĩ + slot; validate khoa & ngày chi tiết
        return "[TODO] lookup_doctor_schedule — logic chưa được cài đặt."
    except Exception as e:
        return f"LỖI: Lỗi không xác định trong lookup_doctor_schedule — {e}"


def verify_patient_identity(identifier: str, id_type: str = "phone") -> str:
    """🪪 [Tool 4] PATIENT IDENTITY VERIFICATION — Xác minh danh tính bệnh nhân.

    Contract (8 trường):
      • Name        : verify_patient_identity
      • Purpose     : Xác minh người đặt lịch qua SĐT / CCCD / mã BHYT với hồ sơ
                      bệnh nhân (mock) trước khi cho phép đặt lịch — đóng vai CỔNG
                      DANH TÍNH. Dùng trước bước chốt đặt lịch.
      • Input       : identifier (str, required) — số định danh; id_type (str,
                      default "phone") — một trong "phone" | "cccd" | "bhyt".
      • Output      : str — kết quả xác minh. Khi in phải CHE BỚT số định danh
                      (chỉ hiện vài ký tự cuối) để bảo vệ PII.
      • Error       : id_type không hợp lệ / định dạng số sai (SĐT ≠ 10 số,
                      CCCD ≠ 12 số...) / không tìm thấy hồ sơ -> "LỖI: ...".
                      KHÔNG raise. KHÔNG rò rỉ thông tin hồ sơ người khác.
      • Side-effect : Read-only (chỉ tra cứu hồ sơ mock).
      • Example     : verify_patient_identity("0912345678", "phone")
                      -> "✅ Xác minh thành công. Bệnh nhân: Nguyễn V.A (mã BN:
                          BN-1023). SĐT ******5678. Đủ điều kiện đặt lịch."
      • Safety      : Bọc try/except; validate định dạng; masking khi hiển thị.

    Args:
        identifier (str): Số định danh (SĐT/CCCD/mã BHYT).
        id_type (str): Loại định danh: "phone" | "cccd" | "bhyt".

    Returns:
        str: Kết quả xác minh (đã che bớt số), hoặc "LỖI: ...".
    """
    try:
        # --- Validate id_type ---
        valid_types = ("phone", "cccd", "bhyt")
        if id_type is None or not isinstance(id_type, str):
            return f"LỖI: Loại định danh (id_type) phải là chuỗi. Giá trị hợp lệ: {', '.join(valid_types)}."
        id_type_clean = id_type.strip().lower()
        if id_type_clean not in valid_types:
            return f"LỖI: Loại định danh '{id_type}' không hợp lệ. Giá trị hợp lệ: {', '.join(valid_types)}."

        # --- Validate identifier ---
        if identifier is None or not isinstance(identifier, str):
            return "LỖI: Số định danh (identifier) không được để trống và phải là chuỗi."
        id_clean = identifier.strip()
        if not id_clean:
            return "LỖI: Số định danh (identifier) không được để trống."

        # TODO: Bổ sung hồ sơ bệnh nhân mock + validate định dạng chi tiết + masking PII
        return "[TODO] verify_patient_identity — logic chưa được cài đặt."
    except Exception as e:
        return f"LỖI: Lỗi không xác định trong verify_patient_identity — {e}"


# Danh sách các tool được đăng ký để Agent (Role 4) sử dụng
AVAILABLE_TOOLS = {
    "detect_emergency": detect_emergency,
    "map_symptom_to_specialty": map_symptom_to_specialty,
    "lookup_doctor_schedule": lookup_doctor_schedule,
    "verify_patient_identity": verify_patient_identity,
}
