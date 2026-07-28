"""
Core app for the chatbot vs ReAct agent lab.
"""

import json
import os
import re
import sys
import unicodedata
from datetime import datetime, timedelta

from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider, MockProvider

load_dotenv()


def _normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "").lower()
    return " ".join(text.split())


def _plain(text: str) -> str:
    text = unicodedata.normalize("NFD", text or "").lower()
    text = "".join(char for char in text if unicodedata.category(char) != "Mn")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def _extract_identifier(user_query: str):
    cccd = re.search(r"\b\d{12}\b", user_query)
    if cccd:
        return cccd.group(0), "cccd"

    phone = re.search(r"\b0\d{9}\b", user_query)
    if phone:
        return phone.group(0), "phone"

    bhyt = re.search(r"\b[A-Z]{2}\d{10}\b", user_query.upper())
    if bhyt:
        return bhyt.group(0), "bhyt"

    return None, None


def _resolve_requested_date(user_query: str) -> str:
    query_norm = _normalize(user_query)
    today = datetime.now().date()

    if "ngay mai" in query_norm or "mai" in query_norm:
        return (today + timedelta(days=1)).strftime("%d/%m/%Y")

    weekdays = {
        "thu hai": 0,
        "thu ba": 1,
        "thu tu": 2,
        "thu nam": 3,
        "thu sau": 4,
        "thu bay": 5,
        "chu nhat": 6,
    }
    ascii_query = unicodedata.normalize("NFD", query_norm).encode("ascii", "ignore").decode("ascii")
    for label, weekday in weekdays.items():
        if label in ascii_query:
            days_ahead = (weekday - today.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            return (today + timedelta(days=days_ahead)).strftime("%d/%m/%Y")

    return today.strftime("%d/%m/%Y")


def _find_specialty_in_query(user_query: str):
    query_norm = _plain(user_query)
    try:
        from config.mock_data import MOCK_DOCTOR_SCHEDULE
    except Exception:
        return None

    for specialty in MOCK_DOCTOR_SCHEDULE:
        if _plain(specialty) in query_norm:
            return specialty
    return None


def load_test_cases():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_baseline_chatbot(user_query: str, provider):
    print(f"\nCHATBOT BASELINE | Cau hoi: {user_query}")
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"Tra loi:\n{response}")


def _parse_action(text: str):
    match = re.search(r"^Action:\s*([A-Za-z_]\w*)\[(.*)\]\s*$", text.strip(), re.M)
    if not match:
        return None, None

    tool_name = match.group(1)
    args_text = match.group(2).strip()
    if not args_text:
        return tool_name, []

    try:
        parsed = json.loads(f"[{args_text}]")
        return tool_name, parsed
    except Exception:
        parts = [p.strip().strip('"').strip("'") for p in args_text.split(",")]
        return tool_name, parts


def _call_tool(tool_name: str, args):
    tool = AVAILABLE_TOOLS.get(tool_name)
    if not tool:
        return f"LOI: Tool '{tool_name}' khong ton tai."
    try:
        return tool(*args)
    except TypeError as e:
        return f"LOI: Sai so luong tham so cho {tool_name} - {e}"
    except Exception as e:
        return f"LOI: Loi khi goi {tool_name} - {e}"


def _build_fallback_step(user_query: str, observations: list[str]) -> str:
    query_norm = _normalize(user_query)
    query_plain = _plain(user_query)
    last_obs = observations[-1] if observations else ""

    if not observations:
        return f"Thought: Can kiem tra nguy co cap cuu truoc.\nAction: detect_emergency[{json.dumps(user_query, ensure_ascii=False)}]"

    if "EMERGENCY=TRUE" in last_obs:
        return (
            "Thought: Day la tinh huong nguy hiem.\n"
            "Final Answer: Ban co dau hieu nguy hiem. Hay goi 115 hoac toi khoa cap cuu gan nhat ngay."
        )

    if "EMERGENCY=FALSE" in last_obs and len(observations) == 1:
        booking_terms = ("dat lich", "kham", "lich")
        specialty_in_query = _find_specialty_in_query(user_query)
        if specialty_in_query and any(term in query_plain for term in booking_terms):
            date_text = _resolve_requested_date(user_query)
            return (
                "Thought: Da co chuyen khoa ro rang, can tra lich.\n"
                f"Action: lookup_doctor_schedule[{json.dumps(specialty_in_query, ensure_ascii=False)}, {json.dumps(date_text, ensure_ascii=False)}]"
            )

        vague_terms = ("met moi", "chan an", "sut can", "khong biet nen kham o dau")
        if any(term in query_plain for term in vague_terms):
            return (
                "Thought: Trieu chung con mo ho.\n"
                "Final Answer: Ban vui long mo ta ro hon vi tri, thoi gian va trieu chung kem theo de toi goi y chuyen khoa chinh xac hon."
            )
        return f"Thought: Can goi y chuyen khoa.\nAction: map_symptom_to_specialty[{json.dumps(user_query, ensure_ascii=False)}]"

    if last_obs.startswith("Chuyen khoa goi y:"):
        specialty = re.search(r"Chuyen khoa goi y:\s*([^\.]+)", last_obs)
        specialty = specialty.group(1).strip() if specialty else None
        booking_terms = ("dat lich", "kham", "lich")
        if any(term in query_norm for term in booking_terms):
            date_text = _resolve_requested_date(user_query)
            return (
                "Thought: Da co chuyen khoa, can tra lich.\n"
                f"Action: lookup_doctor_schedule[{json.dumps(specialty, ensure_ascii=False)}, {json.dumps(date_text, ensure_ascii=False)}]"
            )
        return (
            f"Thought: Da co goi y chuyen khoa.\n"
            f"Final Answer: Dua tren mo ta cua ban, chuyen khoa phu hop la {specialty}. "
            f"Day chi la goi y dinh tuyen, khong thay the chan doan bac si. Ban co muon toi tra lich kham {specialty} khong?"
        )

    if last_obs.startswith("Khoa "):
        identifier, id_type = _extract_identifier(user_query)
        if identifier:
            return (
                "Thought: Can xac minh danh tinh truoc khi chot lich.\n"
                f"Action: verify_patient_identity[{json.dumps(identifier, ensure_ascii=False)}, {json.dumps(id_type, ensure_ascii=False)}]"
            )
        return (
            f"Thought: Da co lich kham.\n"
            f"Final Answer: Toi da tim thay lich kham trong du lieu mock:\n{last_obs}\n"
            "Ban vui long chon mot khung gio phu hop va cung cap SĐT/CCCD/BHYT de xac minh truoc khi chot lich."
        )

    if last_obs.startswith("Xac minh thanh cong"):
        return (
            "Thought: Da xac minh xong.\n"
            f"Final Answer: Toi da xac minh thanh cong. {last_obs}"
        )

    if last_obs.startswith("LOI:"):
        return f"Thought: Can hoi them thong tin.\nFinal Answer: {last_obs}"

    return "Thought: Can ket thuc.\nFinal Answer: Toi da xu ly xong yeu cau cua ban."


def _looks_like_react_response(text: str) -> bool:
    if not text or not isinstance(text, str):
        return False
    lowered = text.lower()
    return "final answer:" in lowered or "action:" in lowered or "thought:" in lowered


def run_react_agent(user_query: str, provider):
    print(f"\nREACT AGENT | Cau hoi: {user_query}")
    query_norm = _normalize(user_query)
    query_plain = _plain(user_query)

    blocked_terms = ("bo qua", "ignore previous", "toan bo so dien thoai", "benh nhan khac", "lich kham cua benh nhan khac")
    if any(term in query_plain for term in blocked_terms):
        print("Final Answer: Toi khong the cung cap du lieu cua nguoi khac.")
        return

    medication_terms = ("uong thuoc", "lieu luong", "lieu bao nhieu", "bi benh gi", "chan doan")
    if any(term in query_plain for term in medication_terms):
        print("Final Answer: Toi khong the chan doan benh hoac huong dan thuoc/lieu luong.")
        return

    greeting_terms = ("chao", "giup toi nhung gi", "co the giup")
    if any(term in query_plain for term in greeting_terms):
        print("Final Answer: Toi co the ho tro sang loc cap cuu, goi y chuyen khoa, tra lich bac si va huong dan xac minh danh tinh.")
        return

    observations = []
    transcript = []

    for step in range(1, MAX_ITERATIONS + 1):
        if isinstance(provider, MockProvider):
            raw = _build_fallback_step(user_query, observations)
        else:
            prompt = (
                f"User query: {user_query}\n"
                f"Previous observations:\n" + ("\n".join(f"- {obs}" for obs in observations) if observations else "- none") + "\n"
                "Return exactly one next step using the required ReAct format."
            )
            raw = provider.generate(prompt, system_prompt=REACT_SYSTEM_PROMPT)
            if not _looks_like_react_response(raw):
                raw = _build_fallback_step(user_query, observations)

        print(f"\n--- Step {step}/{MAX_ITERATIONS} ---")
        print(raw)
        transcript.append(raw)

        if "Final Answer:" in raw:
            return

        tool_name, args = _parse_action(raw)
        if not tool_name:
            if isinstance(provider, MockProvider):
                raw = _build_fallback_step(user_query, observations)
                print(raw)
                if "Final Answer:" in raw:
                    return
                tool_name, args = _parse_action(raw)
            if not tool_name:
                print("Final Answer: Toi chua lay duoc lenh Action hop le tu model.")
                return

        observation = _call_tool(tool_name, args)
        observations.append(observation)
        print(f"Observation: {observation}")

    print(f"Guardrail: Da dat gioi han toi da {MAX_ITERATIONS} buoc.")


if __name__ == "__main__":
    print("==================================================")
    print("Dai hoc VinUni - Bai lab 3: Chatbot vs React Agent")
    print("==================================================")

    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"LLM Provider: {provider.__class__.__name__} (Model: {model_name})")

    tests = load_test_cases()
    print(f"Da tai thanh cong {len(tests)} test cases\n")

    for test in tests:
        print(f"Test Case {test['id']}: {test['question']}")
        sample_query = test["question"]

        print("--- DEMO 1: CHATBOT BASELINE ---")
        run_baseline_chatbot(sample_query, provider)

        print("\n--- DEMO 2: REACT AGENT ---")
        run_react_agent(sample_query, provider)
