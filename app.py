"""
app.py — Umoja: Community Voice Intelligence Hub
Powered by Sunbird AI APIs.
"""
import os
import tempfile
import requests
import gradio as gr
from dotenv import load_dotenv
from backend.pipeline import run_pipeline
from backend.sunbird_client import SPEAKER_IDS
from backend.icons import ICONS

load_dotenv()

LANGUAGES = list(SPEAKER_IDS.keys())   # Luganda, Acholi, Ateso, Runyankole, Lugbara
FORMATS   = ["News Bulletin", "Community Announcement"]

# ── CSS for Sunbird-inspired warm orange theme ─────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --primary: #E65C00;
    --primary-light: #F9A826;
    --bg-panel: #ffffff;
    --border: #f0f0f0;
    --text-main: #333333;
    --text-muted: #666666;
}
body, .gradio-container {
    font-family: 'Inter', sans-serif !important;
}
.gr-button-primary { 
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important; 
    border: none !important; 
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(230, 92, 0, 0.2) !important;
    color: white !important;
}
.gr-button-primary:hover { 
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(230, 92, 0, 0.3) !important;
}
.gr-button-primary:disabled { 
    background: #e0e0e0 !important; 
    box-shadow: none !important;
    opacity: 0.7; cursor: not-allowed !important; 
    transform: none !important;
}
#title-banner {
    background: linear-gradient(135deg, #E65C00 0%, #F9A826 100%);
    border-radius: 16px;
    padding: 30px 40px;
    color: white;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 10px 30px rgba(230, 92, 0, 0.15);
}
#title-banner-content {
    flex-grow: 1;
}
#title-banner h1 { 
    margin: 0; 
    font-size: 2.2rem; 
    font-weight: 700;
    letter-spacing: -0.5px;
    color: white !important;
}
#title-banner p { 
    margin: 8px 0 0; 
    opacity: 0.95; 
    font-size: 1.1rem;
    font-weight: 500;
}
.result-box { 
    background: var(--bg-panel); 
    border: 1px solid var(--border); 
    border-radius: 12px; 
    padding: 20px; 
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    transition: all 0.3s ease;
}
.result-box:hover {
    box-shadow: 0 8px 24px rgba(0,0,0,0.06);
}

/* ──── PROFESSIONAL CLEAN LOADING SPINNER ──── */
.loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 24px;
    background: white;
    border-radius: 16px;
    padding: 60px 40px;
    text-align: center;
    border: 1px solid var(--border);
    box-shadow: 0 10px 40px rgba(0,0,0,0.04);
    min-height: 280px;
}

/* Single elegant spinner */
.spinner {
    width: 64px;
    height: 64px;
    position: relative;
    display: inline-block;
}

.spinner::before {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    border: 3px solid rgba(230, 92, 0, 0.1);
    border-radius: 50%;
    box-sizing: border-box;
}

.spinner::after {
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    border: 3px solid transparent;
    border-top: 3px solid #E65C00;
    border-radius: 50%;
    animation: spin-smooth 1s cubic-bezier(0.5, 0, 0.5, 1) infinite;
    box-sizing: border-box;
}

@keyframes spin-smooth {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-text {
    font-size: 18px;
    font-weight: 600;
    color: var(--text-main);
    letter-spacing: -0.2px;
}

.loading-subtext {
    font-size: 14px;
    color: var(--text-muted);
}

/* ──── RESULT DISPLAY IMPROVEMENTS ──── */
.result-header {
    font-size: 16px;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.result-header svg {
    color: var(--primary);
}

.result-content {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    line-height: 1.7;
    color: var(--text-main);
    font-size: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    margin-bottom: 24px;
    white-space: pre-wrap;
}

.result-content-transcript {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    line-height: 1.7;
    color: var(--text-main);
    font-size: 14px;
    margin-bottom: 24px;
    white-space: pre-wrap;
}

.custom-audio-player {
    background: rgba(230, 92, 0, 0.05);
    border: 1px solid rgba(230, 92, 0, 0.15);
    border-radius: 12px;
    padding: 24px;
    margin-top: 24px;
}

.audio-label {
    font-size: 16px;
    font-weight: 600;
    color: var(--primary);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* ──── STATUS MESSAGES ──── */
.status-message {
    padding: 16px 20px;
    border-radius: 12px;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.status-success {
    background: #f0fdf4;
    color: #166534;
    border: 1px solid #bbf7d0;
}
.status-success svg {
    color: #166534;
}

.status-error {
    background: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
}
.status-error svg {
    color: #991b1b;
}

/* Hide gradio text inputs if any */
.hide-empty:empty {
    display: none;
}
"""


def process(input_mode, text_input, audio_input, target_language, story_format):
    """Gradio callback — runs the pipeline and returns UI-friendly outputs."""

    # Validate token
    if not os.environ.get("SUNBIRD_API_TOKEN", "").strip():
        err = "SUNBIRD_API_TOKEN is not set. Add it to your .env file and restart."
        return (
            f"<div class='status-message status-error'>{ICONS['error']} <div>{err}</div></div>",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(interactive=True),
        )

    use_audio = ("Audio" in input_mode)

    result = run_pipeline(
        input_text=text_input if not use_audio else None,
        audio_path=audio_input  if use_audio else None,
        target_language=target_language,
        story_format=story_format,
    )

    if result["error"]:
        return (
            f"<div class='status-message status-error'>{ICONS['error']} <div>{result['error']}</div></div>",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(interactive=True),
        )

    # Build transcript panel
    if result["transcript"]:
        transcript_html = (
            f"<div class='result-header'>{ICONS['transcript']} Transcript <i>(detected: {result['detected_language']})</i></div>"
            f"<div class='result-content-transcript'>{result['transcript']}</div>"
        )
    else:
        transcript_html = ""

    # Build summary html
    summary_html = (
        f"<div class='result-header'>{ICONS['summary']} English Summary</div>"
        f"<div class='result-content'>{result['summary']}</div>"
    )

    # Build translation html
    translation_html = (
        f"<div class='result-header'>{ICONS['translation']} Translated to {target_language}</div>"
        f"<div class='result-content'>{result['translation']}</div>"
    )

    # Download the audio and pass as file path so Gradio can play it
    audio_file_path = None
    if result["audio_url"]:
        try:
            r = requests.get(result["audio_url"], timeout=30)
            r.raise_for_status()
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                tmp.write(r.content)
                audio_file_path = tmp.name
        except Exception as e:
            print(f"Error downloading audio: {e}")
            pass  # audio player will just be empty

    if audio_file_path:
        audio_label_html = f"<div class='audio-label'>{ICONS['speaker']} Listen in {target_language}</div>"
    else:
        audio_label_html = ""

    # Return tuple in order of outputs: (status_box, loading_indicator, transcript_box, summary_box, translation_box, audio_label, audio_player, run_btn)
    return (
        f"<div class='status-message status-success'>{ICONS['check']} <div>Done! All results are ready below.</div></div>",
        gr.update(visible=False),  # Hide loading indicator
        gr.update(value=transcript_html, visible=bool(result["transcript"])),
        gr.update(value=summary_html, visible=True),
        gr.update(value=translation_html, visible=True),
        gr.update(value=audio_label_html, visible=audio_file_path is not None),
        gr.update(value=audio_file_path, visible=audio_file_path is not None),
        gr.update(interactive=True),
    )


# ── Build UI ───────────────────────────────────────────────────────────────
with gr.Blocks(title="Umoja") as demo:

    gr.HTML(f"""
    <div id="title-banner">
      <div>{ICONS['sun']}</div>
      <div id="title-banner-content">
          <h1>Umoja</h1>
          <p>Community Voice Intelligence Hub powered by Sunbird AI</p>
      </div>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### ① Choose your input")
            input_mode = gr.Radio(
                choices=["Type / Paste Text", "Audio Upload"],
                value="Type / Paste Text",
                label="Input mode",
                interactive=True,
            )

            with gr.Group() as text_group:
                text_input = gr.Textbox(
                    label="Your story or report",
                    placeholder="Paste or type the text you want to summarise and broadcast…",
                    lines=8,
                )

            with gr.Group(visible=False) as audio_group:
                audio_input = gr.Audio(
                    label="Upload audio (MP3, WAV, OGG, M4A — max 5 min)",
                    type="filepath",
                )

            gr.Markdown("### ② Configure output")
            target_language = gr.Dropdown(
                choices=LANGUAGES,
                value="Luganda",
                label="Target local language",
            )
            story_format = gr.Radio(
                choices=FORMATS,
                value="News Bulletin",
                label="Summary format",
            )

            # Note: We can't use HTML in button label directly through gr.Button label, 
            # but we can pass a string without emojis. The premium look is handled via CSS.
            run_btn = gr.Button("Run Pipeline", variant="primary", size="lg")

        with gr.Column(scale=1):
            gr.Markdown("### ③ Results")
            status_box = gr.HTML("<div style='color: var(--text-muted); padding-top: 10px;'><em>Results will appear here after you click Run.</em></div>")
            
            # Loading indicator (shown during processing)
            loading_indicator = gr.HTML(
                """<div class="loading-container">
                   <div class="spinner"></div>
                   <div class="loading-text">Processing your content...</div>
                   <div class="loading-subtext">This may take a moment ......</div>
                   </div>""",
                visible=False
            )

            transcript_box = gr.HTML(visible=False, elem_classes="hide-empty")
            summary_box = gr.HTML(visible=False, elem_classes="hide-empty")
            translation_box = gr.HTML(visible=False, elem_classes="hide-empty")
            audio_label = gr.HTML(visible=False, elem_classes="hide-empty")
            audio_player = gr.Audio(
                visible=False, 
                interactive=False,
                type="filepath",
                elem_classes="custom-audio-player"
            )

    # ── Wire up visibility toggle ──────────────────────────────────────────
    def toggle_input(mode):
        is_audio = "Audio" in mode
        return gr.update(visible=not is_audio), gr.update(visible=is_audio)

    input_mode.change(toggle_input, inputs=input_mode, outputs=[text_group, audio_group])

    # ── Show loading state, then run process ─────────────────────────────────
    def show_loading():
        """Pre-processing callback to show loading indicator."""
        return (
            gr.update(value="<div style='text-align:center; color:var(--text-muted); padding: 12px;'><em>Starting...</em></div>"),  # status_box
            gr.update(visible=True),  # loading_indicator
            gr.update(visible=False),  # transcript_box
            gr.update(visible=False),  # summary_box
            gr.update(visible=False),  # translation_box
            gr.update(visible=False),  # audio_label
            gr.update(visible=False),  # audio_player
        )
    
    # Click shows loading, then chains to process which shows results.
    # Note show_progress="hidden" prevents Gradio's built-in spinner from showing on top of ours.
    run_btn.click(
        fn=show_loading,
        outputs=[
            status_box,
            loading_indicator,
            transcript_box,
            summary_box,
            translation_box,
            audio_label,
            audio_player,
        ],
        show_progress="hidden"
    ).then(
        fn=process,
        inputs=[input_mode, text_input, audio_input, target_language, story_format],
        outputs=[
            status_box, 
            loading_indicator, 
            transcript_box, 
            summary_box, 
            translation_box, 
            audio_label, 
            audio_player, 
            run_btn
        ],
        show_progress="hidden"
    )

    gr.Markdown(
        "---\n"
        "*All AI capabilities are provided exclusively by [Sunbird AI](https://sunbird.ai). "
        "No other model providers are used.*"
    )


if __name__ == "__main__":
    demo.launch(show_error=True, css=CUSTOM_CSS)
