# UAB Sveikata — Streamlit aplikacija

Trumpas aprašymas

Ši maža Streamlit aplikacija generuoja savaitės mankštos planą pagal vartotojo įvestis: amžių, sveikatos problemas, kiek minučių per dieną skiriama mankštai ir tikslą (numesti svorio arba priaugti raumenų).

Funkcionalumas

- Pasirenkami modeliai:
  - Gemma3 (vietinis per Ollama) — jei nustatytas `OLLAMA_HOST` ir veikia Ollama serveris.
  - Qwen3 (per OpenRouter) — jei nustatytas `OPENROUTER_API_KEY`.
  - Vietinis (fallback) — sukuriamas deterministinis planas be jokių tinklo skambučių.
- Planas visada pradeda su:

  UAB Sveikata agentas:

  ir baigiasi su:

  Šis atsakymas sugeneruotas AI, ir nėra profesionali daktaro nuomonė.

Paleidimas lokaliai

1. Sukurkite virtualią aplinką ir įdiekite priklausomybes:

```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Paleiskite Streamlit:

```bash
streamlit run streamlit_app.py
```

Konfigūracija (neprivaloma)

- Jei turite vietinį Ollama serverį, nustatykite aplinkos kintamąjį `OLLAMA_HOST` (pvz. `http://localhost:11434`). Programa bandys aiškinti per `POST {OLLAMA_HOST}/api/generate`.
- Jei norite naudoti OpenRouter, nustatykite `OPENROUTER_API_KEY` ir (neprivaloma) `OPENROUTER_URL`.

Pastabos

- Programoje yra saugus vietinis fallback, todėl aplikacija veiks ir be prieigos prie modelių tinkamai sugeneruodama paprastą savaitinį planą.
- Tai mokomojo/ kontrolinio darbo implementacija, kuri nėra medicininė rekomendacija.
