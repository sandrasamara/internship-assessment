import gradio as gr

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
.audio-container {
    background: #fff8f3;
    border: 1px solid #ffe8d6;
    border-radius: 12px;
    padding: 24px;
    margin-top: 24px;
}
"""

with gr.Blocks(css=CUSTOM_CSS) as demo:
    audio_input = gr.Audio(
        label="Upload audio (MP3, WAV, OGG, M4A — max 5 min)",
        type="filepath",
    )

demo.launch(server_port=7860)
