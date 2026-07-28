"""
Tool registry for the medical appointment ReAct agent.

All data used here is mock data. Do not put real patient identifiers in this
project or commit real PII.
"""

import os
import re
import sys
import unicodedata
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.mock_data import (
    EMERGENCY_KEYWORDS,
    MOCK_DOCTOR_SCHEDULE,
    MOCK_PATIENTS,
    SYMPTOM_SPECIALTY_MAP,
)


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "").lower()
    return " ".join(text.split())


def _plain(text: str) -> str:
    text = unicodedata.normalize("NFD", text or "").lower()
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def _mask_identifier(identifier: str) -> str:
    if len(identifier) <= 4:
        return "*" * len(identifier)
    return "*" * (len(identifier) - 4) + identifier[-4:]


def detect_emergency(symptom: str) -> str:
    """Screen a symptom description for emergency warning signs."""
    try:
        if symptom is None:
            return "LOI: Tham so 'symptom' khong duoc de trong."
        if not isinstance(symptom, str):
            return "LOI: Tham so 'symptom' phai la chuoi."

        symptom_clean = symptom.strip()
        if not symptom_clean:
            return "LOI: Tham so 'symptom' khong duoc de trong."

        symptom_norm = _normalize(symptom_clean)
        matched = [kw for kw in EMERGENCY_KEYWORDS if _normalize(kw) in symptom_norm]
        if matched:
            return (
                "EMERGENCY=TRUE | Phat hien dau hieu nguy hiem: "
                f"{', '.join(matched)}. Goi 115 hoac toi khoa cap cuu gan nhat ngay."
            )

        return (
            "EMERGENCY=FALSE | Chua phat hien dau hieu cap cuu trong mo ta. "
            "Co the tiep tuc tu van dat lich thuong."
        )
    except Exception as e:
        return f"LOI: Loi khong xac dinh trong detect_emergency - {e}"


def map_symptom_to_specialty(symptom: str) -> str:
    """Map symptoms to a suggested specialty using approved mock data."""
    try:
        if symptom is None:
            return "LOI: Tham so 'symptom' khong duoc de trong."
        if not isinstance(symptom, str):
            return "LOI: Tham so 'symptom' phai la chuoi."

        symptom_clean = symptom.strip()
        if len(symptom_clean) < 2:
            return (
                "LOI: Mo ta trieu chung qua ngan. Vui long mo ta ro vi tri dau, "
                "bieu hien kem theo va thoi gian xuat hien."
            )

        symptom_norm = _normalize(symptom_clean)
        matches = []
        for specialty, keywords in SYMPTOM_SPECIALTY_MAP.items():
            matched_keywords = [kw for kw in keywords if _normalize(kw) in symptom_norm]
            if matched_keywords:
                matches.append((specialty, matched_keywords))

        if not matches:
            return (
                "LOI: Chua du du kien de goi y chuyen khoa. Vui long mo ta ro vi tri dau, "
                "bieu hien kem theo va thoi gian xuat hien trieu chung."
            )

        specialty, matched_keywords = max(matches, key=lambda item: len(item[1]))
        return (
            f"Chuyen khoa goi y: {specialty}. "
            f"Ly do: mo ta co cac dau hieu lien quan: {', '.join(matched_keywords)}. "
            "Day la goi y khoa kham, khong thay the chan doan bac si."
        )
    except Exception as e:
        return f"LOI: Loi khong xac dinh trong map_symptom_to_specialty - {e}"


def lookup_doctor_schedule(specialty: str, date: str) -> str:
    """Look up available doctors and slots for a specialty and date."""
    try:
        if specialty is None or not isinstance(specialty, str) or not specialty.strip():
            return "LOI: Ten chuyen khoa khong duoc de trong."
        if date is None or not isinstance(date, str) or not date.strip():
            return "LOI: Ngay kham khong duoc de trong."

        specialty_clean = specialty.strip()
        doctors = MOCK_DOCTOR_SCHEDULE.get(specialty_clean)
        if not doctors:
            query_plain = _plain(specialty_clean)
            for known_specialty in MOCK_DOCTOR_SCHEDULE:
                if _plain(known_specialty) == query_plain:
                    specialty_clean = known_specialty
                    doctors = MOCK_DOCTOR_SCHEDULE[known_specialty]
                    break

        if not doctors:
            valid = ", ".join(MOCK_DOCTOR_SCHEDULE.keys())
            return f"LOI: Khong co chuyen khoa '{specialty_clean}'. Chuyen khoa hop le: {valid}."

        date_clean = date.strip()
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_clean):
            parsed = datetime.strptime(date_clean, "%Y-%m-%d")
            date_clean = parsed.strftime("%d/%m/%Y")
        elif re.fullmatch(r"\d{2}/\d{2}/\d{4}", date_clean):
            datetime.strptime(date_clean, "%d/%m/%Y")

        lines = [f"Khoa {specialty_clean} ngay {date_clean}:"]
        for doctor in doctors:
            lines.append(f"- {doctor['name']}: {', '.join(doctor['slots'])}")
        return "\n".join(lines)
    except ValueError:
        return "LOI: Ngay kham sai dinh dang. Dung dd/mm/yyyy hoac yyyy-mm-dd."
    except Exception as e:
        return f"LOI: Loi khong xac dinh trong lookup_doctor_schedule - {e}"


def verify_patient_identity(identifier: str, id_type: str = "phone") -> str:
    """Verify a mock patient identifier before booking is confirmed."""
    try:
        valid_types = ("phone", "cccd", "bhyt")
        if id_type is None or not isinstance(id_type, str):
            return f"LOI: id_type phai la chuoi. Gia tri hop le: {', '.join(valid_types)}."

        id_type_clean = id_type.strip().lower()
        if id_type_clean not in valid_types:
            return f"LOI: id_type '{id_type}' khong hop le. Gia tri hop le: {', '.join(valid_types)}."

        if identifier is None or not isinstance(identifier, str):
            return "LOI: identifier khong duoc de trong va phai la chuoi."

        id_clean = identifier.strip()
        if not id_clean:
            return "LOI: identifier khong duoc de trong."

        patterns = {
            "phone": r"^0\d{9}$",
            "cccd": r"^\d{12}$",
            "bhyt": r"^[A-Z]{2}\d{10}$",
        }
        id_clean = id_clean.upper() if id_type_clean == "bhyt" else id_clean
        if not re.fullmatch(patterns[id_type_clean], id_clean):
            return f"LOI: Dinh dang {id_type_clean} khong hop le."

        patient = MOCK_PATIENTS.get(id_type_clean, {}).get(id_clean)
        if not patient:
            return (
                f"LOI: Khong tim thay ho so benh nhan voi {id_type_clean} "
                f"{_mask_identifier(id_clean)} trong du lieu mock."
            )

        return (
            f"Xac minh thanh cong. Benh nhan: {patient['name']} "
            f"(ma BN: {patient['code']}). {id_type_clean.upper()} {_mask_identifier(id_clean)}."
        )
    except Exception as e:
        return f"LOI: Loi khong xac dinh trong verify_patient_identity - {e}"


AVAILABLE_TOOLS = {
    "detect_emergency": detect_emergency,
    "map_symptom_to_specialty": map_symptom_to_specialty,
    "lookup_doctor_schedule": lookup_doctor_schedule,
    "verify_patient_identity": verify_patient_identity,
}
