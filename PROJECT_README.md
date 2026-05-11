# 🌻 Umoja — Community Voice Intelligence Hub

> **Umoja** (Swahili/Luganda: *"conversations"*) is a Generative AI web application
> that lets anyone — a journalist, community radio producer, or NGO field worker — speak or type
> a story in any supported language and instantly receive an AI-generated English summary,
> a translation into a chosen Ugandan local language, and a synthesised audio broadcast of that
> translation. Every AI capability is powered exclusively by **Sunbird AI**.

---

## Architecture Overview

```
User Input (text or audio)
        │
        ▼
┌───────────────────────┐
│  [STT] if audio:      │  POST /tasks/stt
│  Transcribe → text    │  Sunbird Speech-to-Text
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  [Summarise]          │  POST /tasks/summarise
│  English summary      │  Sunbird Summarisation (+ PII anonymisation)
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  [Translate]          │  POST /tasks/sunflower_inference
│  → chosen local lang  │  Sunflower LLM (multi-turn chat)
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│  [TTS]                │  POST /tasks/tts
│  Audio broadcast clip │  Sunbird Text-to-Speech
└───────────┬───────────┘
            │
            ▼
   UI displays: transcript · summary · translation · audio player
```

---

## Local Setup

### Prerequisites
- Python 3.9+
- A [Sunbird AI API token](https://api.sunbird.ai/)

### Steps

```bash
# 1. Clone
git clone https://github.com/<your-username>/internship-assessment.git
cd internship-assessment

# 2. Virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate.bat

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Open .env and set SUNBIRD_API_TOKEN=<your token>

# 5. Run the app
python app.py
# Open http://localhost:7860 in your browser
```

### Run tests (Part 1)
```bash
pytest
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SUNBIRD_API_TOKEN` | ✅ Yes | Your Sunbird AI bearer token from https://api.sunbird.ai/ |

---

## Usage Walkthrough

1. **Choose input mode** — "Type / Paste Text" or "Audio Upload"
2. **If audio**: upload an MP3/WAV/OGG/M4A file (≤ 5 minutes). The app will transcribe it automatically.
3. **Pick a target language** — Luganda, Acholi, Ateso, Runyankole, or Lugbara.
4. **Pick a summary format** — News Bulletin or Community Announcement.
5. **Click "Run Pipeline"**.
6. The results panel shows:
   - 🎙️ Transcript (audio mode only) with detected language badge
   - 📝 English summary (with PII anonymised)
   - 🌍 Translated summary in your chosen language
   - 🔊 Audio player with the synthesised speech clip

---

## Deployed Link

🔗 **[Live Demo on Hugging Face Spaces](https://huggingface.co/spaces/<your-username>/Umoja)**

---

## Known Limitations

- **5-minute audio cap**: audio files longer than 5 minutes are rejected with a clear error.
- **Supported STT languages**: Luganda, Acholi, Ateso, Runyankole, Lugbara, English only.
- **Summarisation language**: the `/tasks/summarise` endpoint works best with English input; other languages are passed through but may produce lower-quality summaries.
- **TTS voices**: all voices are female except Swahili (male); Swahili is not available as a target language in the translation step because Sunflower is optimised for Ugandan languages.
- **Audio URL expiry**: the TTS audio URL returned by Sunbird is a temporary signed URL — the app downloads it immediately to avoid expiry issues.
- **Rate limits**: Sunbird AI free-tier accounts have rate limits; heavy concurrent use may result in 429 errors surfaced to the user.