import os
import httpx
import streamlit as st
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from a .env file (if present)
load_dotenv()

START_PHRASE = "UAB Sveikata agentas:"
END_PHRASE = "Šis atsakymas sugeneruotas AI, ir nėra profesionali daktaro nuomonė."


def generate_plan_locally(age: int, health_issues: str, time_min: int, goal: str) -> str:
    """Generate a deterministic weekly plan without calling external models.

    This is a safe fallback if no model is available. The output follows the
    required start/end phrases.
    """
    days = ["Pirmadienis", "Antradienis", "Trečiadienis", "Ketvirtadienis", "Penktadienis", "Šeštadienis", "Sekmadienis"]
    warmup = "5–10 min lengvos apšilimo pratimų"
    plan_lines = [START_PHRASE, f"Amžius: {age}", f"Sveikatos problemos: {health_issues or 'nėra'}", f"Laikas per dieną: {time_min} min", f"Tikslas: {goal}", ""]

    for d in days:
        if goal == "Numesti svorio":
            main = f"Kardio: {max(10, time_min - 10)} min intervalų (pvz., greitas ėjimas arba lengvas bėgimas)"
            strength = f"Plaukimo arba kūno svorio pratimai: {min(30, time_min)} min" if time_min >= 20 else "Lengvi tempimo pratimai"
        else:
            main = f"Jėgos treniruotė: svarmenys arba kūno svorio pratimai, 3 serijos po 8–12 kartų"
            strength = f"Fokusas ant raumenų grupės (pvz., krūtinė, nugara, kojos). Trukmė: {max(15, time_min - 10)} min"

        # adjust for middle of week rest
        if d == "Sekmadienis":
            day_line = f"{d}: Poilsis arba lengvas pasivaikščiojimas (20–30 min)."
        else:
            day_line = f"{d}: {warmup}; {main}; {strength}."

        plan_lines.append(day_line)

    plan_lines.append("")
    plan_lines.append(END_PHRASE)
    return "\n".join(plan_lines)


def call_ollama(prompt: str, model: str = "gemma3:4b", host: Optional[str] = None) -> Optional[str]:
    """Try to call a local Ollama server. If it fails, return None.

    To use Ollama, set OLLAMA_HOST (e.g. http://localhost:11434).
    """
    if not host:
        host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

    try:
        url = host.rstrip("/") + "/api/generate"
        payload = {"model": model, "prompt": prompt}
        with httpx.Client(timeout=30.0) as client:
            r = client.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            # best-effort extraction
            if isinstance(data, dict):
                return data.get("response") or data.get("output") or str(data)
            return str(data)
    except Exception as e:
        # Silent fallback to local generator
        return None


def call_openrouter(prompt: str) -> Optional[str]:
    """Try to call OpenRouter if an API key is provided. Returns None on failure.

    NOTE: This function attempts a best-effort call; network failures are
    captured and result in None so the app falls back gracefully.
    """
    # Read API key from environment (supports .env via load_dotenv())
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None

    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        url = os.environ.get("OPENROUTER_URL", "https://openrouter.ai/v1/chat/completions")
        payload = {
            "model": "qwen3.0-14b",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 800
        }
        with httpx.Client(timeout=30.0) as client:
            r = client.post(url, json=payload, headers=headers)
            r.raise_for_status()
            data = r.json()
            # best-effort parsing
            if isinstance(data, dict):
                # try common completions structure
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0].get("message", {}).get("content") or str(data["choices"][0])
                return data.get("response") or str(data)
            return str(data)
    except Exception:
        return None


def build_prompt(age: int, health_issues: str, time_min: int, goal: str) -> str:
    return (
        f"Generuok savaitės mankštos planą. Amžius: {age}. "
        f"Sveikatos problemos: {health_issues or 'nėra'}. "
        f"Laikas per dieną: {time_min} minučių. "
        f"Tikslas: {goal}. "
        "Atsakymas turi prasidėti: 'UAB Sveikata agentas:' ir baigtis fraze 'Šis atsakymas sugeneruotas AI, ir nėra profesionali daktaro nuomonė.'"
    )


def main():
    st.set_page_config(page_title="UAB Sveikata - Savaitės mankšta", layout="centered")

    st.title("UAB Sveikata — savaitės mankštos planas")

    with st.form("input_form"):
        age = st.number_input("Amžius", min_value=6, max_value=120, value=30, step=1)
        health_issues = st.text_area("Sveikatos problemos (jei yra)", value="", help="Trumpai aprašykite, pvz., hipertenzija, kelio skausmas")
        time_min = st.slider("Laikas mankštai per dieną (min)", min_value=5, max_value=120, value=30, step=5)
        goal = st.selectbox("Tikslas", options=["Numesti svorio", "Priaugti raumenų"], index=0)

        model_choice = st.radio("Modelio pasirinkimas (jei prieinama)", options=["Gemma3 (Ollama local)", "Qwen3 (OpenRouter)", "Vietinis (fallback)"])

        submitted = st.form_submit_button("Generuoti planą")

    if submitted:
        # Basic validation
        if age <= 0 or time_min <= 0 or goal not in ("Numesti svorio", "Priaugti raumenų"):
            st.error("Įveskite galiojančius duomenis visiems laukams.")
            return

        prompt = build_prompt(age, health_issues, time_min, goal)

        result = None
        if model_choice.startswith("Gemma3"):
            st.info("Bandoma naudoti vietinį Ollama serverį...")
            result = call_ollama(prompt, model="gemma3:4b")
        elif model_choice.startswith("Qwen3"):
            st.info("Bandoma naudoti OpenRouter...")
            # call_openrouter will read OPENROUTER_API_KEY via os.getenv (and .env thanks to load_dotenv())
            result = call_openrouter(prompt)

        if not result:
            st.warning("Modelis nepasiekiamas arba įvyko klaida — generuojama vietinė versija.")
            result = generate_plan_locally(age, health_issues, time_min, goal)

        # If the result doesn't contain the required start/end, ensure they are present
        if not result.startswith(START_PHRASE):
            result = START_PHRASE + "\n\n" + result
        if not result.strip().endswith(END_PHRASE):
            result = result.rstrip() + "\n\n" + END_PHRASE

        st.subheader("Sugeneruotas savaitės planas")
        st.text(result)


if __name__ == "__main__":
    main()
