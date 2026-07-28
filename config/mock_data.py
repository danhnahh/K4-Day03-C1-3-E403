"""
🗄️ MOCK DATA — Dữ liệu giả lập cho các Tool (Role 2)
Chủ đề nhóm: 🏥 ĐẶT LỊCH KHÁM BỆNH & TƯ VẤN CHUYÊN KHOA

⚠️ BẢO MẬT: Toàn bộ dữ liệu trong file này là GIẢ LẬP (MOCK).
   Tuyệt đối KHÔNG nhập PII thật và KHÔNG commit PII thật.
"""

# ─────────────────────────────────────────────────────────────────────────────
# 🚨 Từ khóa triệu chứng nguy hiểm (cho detect_emergency)
# ─────────────────────────────────────────────────────────────────────────────
EMERGENCY_KEYWORDS = [
    "đau ngực", "đau tức ngực", "tức ngực", "khó thở", "ngất",
    "bất tỉnh", "co giật", "xuất huyết", "chảy máu không cầm",
    "sốt cao co giật", "liệt nửa người", "tê cứng", "mất ý thức",
    "ngừng thở", "sốc phản vệ", "nuốt hóa chất", "uống thuốc quá liều",
    "tai nạn giao thông", "vết thương hở lớn", "gãy xương hở",
    "đột quỵ", "nhồi máu", "tím tái",
]

# ─────────────────────────────────────────────────────────────────────────────
# 🧭 Bảng ánh xạ triệu chứng -> chuyên khoa (cho map_symptom_to_specialty)
# ─────────────────────────────────────────────────────────────────────────────
SYMPTOM_SPECIALTY_MAP = {
    "Răng-Hàm-Mặt": [
        "đau răng", "sưng nướu", "ê buốt", "chảy máu chân răng",
        "sâu răng", "lung lay răng", "đau hàm", "răng khôn",
    ],
    "Tai-Mũi-Họng": [
        "đau họng", "viêm họng", "khàn tiếng", "ù tai", "chảy mũi",
        "nghẹt mũi", "đau tai", "viêm xoang", "amidan",
    ],
    "Nội tổng quát": [
        "mệt mỏi", "sốt", "sốt nhẹ", "đau đầu", "chóng mặt",
        "chán ăn", "sụt cân", "mất ngủ", "đau bụng",
    ],
    "Da liễu": [
        "nổi mẩn", "ngứa", "phát ban", "mụn", "nấm da",
        "rụng tóc", "chàm", "vảy nến", "dị ứng da",
    ],
    "Nhi": [
        "trẻ sốt", "trẻ ho", "trẻ tiêu chảy", "trẻ biếng ăn",
        "trẻ quấy khóc", "trẻ nổi mẩn",
    ],
    "Mắt": [
        "đau mắt", "mờ mắt", "đỏ mắt", "nhức mắt", "cận thị",
        "chảy nước mắt",
    ],
    "Cơ-Xương-Khớp": [
        "đau lưng", "đau khớp", "cứng khớp", "thoát vị đĩa đệm",
        "đau vai gáy", "viêm khớp", "đau cổ",
    ],
    "Tiêu hóa": [
        "đau dạ dày", "ợ chua", "trào ngược", "tiêu chảy",
        "táo bón", "đầy bụng", "buồn nôn",
    ],
    "Tim mạch": [
        "hồi hộp", "tim đập nhanh", "huyết áp cao", "huyết áp thấp",
        "đau thắt ngực nhẹ",
    ],
    "Nội tiết": [
        "tiểu đường", "tuyến giáp", "rối loạn nội tiết", "tăng cân bất thường",
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# 📅 Dữ liệu bác sĩ + slot trống (cho lookup_doctor_schedule)
# ─────────────────────────────────────────────────────────────────────────────
MOCK_DOCTOR_SCHEDULE = {
    "Răng-Hàm-Mặt": [
        {"name": "BS. Trần Văn Hùng", "slots": ["08:00", "09:30", "14:00"]},
        {"name": "BS.CKI Lê Thị Mai", "slots": ["10:30", "15:30"]},
    ],
    "Tai-Mũi-Họng": [
        {"name": "BS. Nguyễn Hoàng Nam", "slots": ["08:30", "10:00", "14:30"]},
        {"name": "BS.CKII Phạm Thu Hà", "slots": ["09:00", "15:00"]},
    ],
    "Nội tổng quát": [
        {"name": "BS. Lê Minh Tuấn", "slots": ["07:30", "09:00", "13:30", "15:00"]},
        {"name": "BS.CKI Đỗ Thị Hồng", "slots": ["08:00", "10:30"]},
    ],
    "Da liễu": [
        {"name": "BS. Vũ Quang Đại", "slots": ["09:00", "14:00"]},
        {"name": "BS.CKI Trần Ngọc Lan", "slots": ["10:00", "15:30"]},
    ],
    "Nhi": [
        {"name": "BS. Hoàng Thị Ngọc", "slots": ["08:00", "09:30", "14:00", "15:30"]},
        {"name": "BS.CKII Nguyễn Văn Bình", "slots": ["10:00", "13:30"]},
    ],
    "Mắt": [
        {"name": "BS. Phan Anh Dũng", "slots": ["08:30", "10:30", "14:30"]},
    ],
    "Cơ-Xương-Khớp": [
        {"name": "BS.CKI Ngô Thanh Sơn", "slots": ["08:00", "10:00", "14:00"]},
        {"name": "BS. Đinh Thị Tuyết", "slots": ["09:30", "15:00"]},
    ],
    "Tiêu hóa": [
        {"name": "BS. Bùi Đức Long", "slots": ["08:00", "09:30", "14:00"]},
        {"name": "BS.CKI Lý Thị Huệ", "slots": ["10:30", "15:30"]},
    ],
    "Tim mạch": [
        {"name": "BS.CKII Trương Minh Khoa", "slots": ["08:00", "10:00"]},
        {"name": "BS. Đặng Thị Yến", "slots": ["14:00", "15:30"]},
    ],
    "Nội tiết": [
        {"name": "BS.CKI Hà Văn Phúc", "slots": ["09:00", "14:30"]},
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# 🪪 Hồ sơ bệnh nhân mock (cho verify_patient_identity)
# ─────────────────────────────────────────────────────────────────────────────
MOCK_PATIENTS = {
    "phone": {
        "0912345678": {"name": "Nguyễn Văn An", "code": "BN-1023"},
        "0987654321": {"name": "Trần Thị Bích", "code": "BN-2047"},
        "0901122334": {"name": "Lê Hoàng Minh", "code": "BN-3105"},
        "0933445566": {"name": "Phạm Thị Dung", "code": "BN-4082"},
    },
    "cccd": {
        "012345678901": {"name": "Nguyễn Văn An", "code": "BN-1023"},
        "098765432109": {"name": "Trần Thị Bích", "code": "BN-2047"},
    },
    "bhyt": {
        "DN4012345678": {"name": "Nguyễn Văn An", "code": "BN-1023"},
        "HN1098765432": {"name": "Lê Hoàng Minh", "code": "BN-3105"},
    },
}
