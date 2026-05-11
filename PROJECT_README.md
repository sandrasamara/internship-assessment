# Umoja Community Voice Intelligence Hub

### Link **https://huggingface.co/spaces/samasandy/Umoja**

## What is Umoja?

**Umoja** (Swahili/Luganda: *"conversations"*) is an intelligent content processing platform designed to empower journalists, community radio producers, NGO field workers, and community members in Uganda. It transforms spoken or written stories into accessible multi-language formats instantly.

Users can speak or type a story in any language, and Umoja automatically:
- **Summarizes** the content in English with PII anonymization
- **Translates** the summary into a chosen Ugandan local language
- **Synthesizes** the translated text into natural-sounding audio for broadcast

Every AI capability is powered exclusively by **Sunbird AI**, ensuring reliable and contextually-aware processing tailored for African languages and communities.

---

## Key Features

###  Dual Input Modes
- **Text Input**: Type or paste stories, reports, or transcripts directly
- **Audio Upload**: Upload recorded audio files (MP3, WAV, OGG, M4A) up to 5 minutes with automatic speech-to-text transcription

### Multilingual Support
Supports 5 Ugandan languages with native text-to-speech voices:
- Luganda
- Acholi  
- Ateso
- Runyankole
- Lugbara

###  Intelligent Processing
- **Summarization**: Automatically condenses content into concise English summaries
- **PII Anonymization**: Protects sensitive information during summarization
- **Format Options**: Generate summaries as "News Bulletin" or "Community Announcement"

###  Audio Broadcasting
- Natural-sounding Text-to-Speech synthesis in target language
- Ready-to-broadcast audio files for community radio stations and digital platforms
- Language-specific speaker voices for authentic local delivery

###  User-Friendly Interface
- Modern, intuitive web interface built with Gradio
- Real-time processing with visual feedback
- One-click pipeline execution
- Professional Sunbird-inspired design

---

## How It Works

### Processing Pipeline

The application follows a four-stage intelligent pipeline:

```
1. TRANSCRIBE (if audio input)
   └─ Converts audio to text using Sunbird Speech-to-Text

2. SUMMARIZE
   └─ Creates concise English summary with PII protection

3. TRANSLATE
   └─ Translates summary to selected Ugandan language via Sunbird LLM

4. SYNTHESIZE
   └─ Generates natural audio using Sunbird Text-to-Speech
```

### User Experience Flow

1. **Select Input** → Choose between typing text or uploading audio
2. **Configure** → Pick target language and summary format
3. **Process** → Click "Run Pipeline" to start
4. **Receive Results** → View transcript, summary, translation, and listen to audio

---

## Use Cases

###  Community Radio
Produce multi-language radio content from a single story submission, reaching diverse linguistic communities without duplication of effort.

###  Journalism & News
Rapidly generate summarized content in multiple languages for broader audience reach while protecting reporter sources through PII anonymization.

###  NGO Field Operations
Convert field reports into accessible multi-language formats for community engagement, training, and documentation.

###  Education & Advocacy
Create accessible educational content in local languages to improve information dissemination in multilingual communities.

###  Public Communication
Enable government agencies and organizations to communicate important announcements in all major Ugandan languages simultaneously.

---

## Technical Architecture

### Core Components

- **Frontend**: Gradio web interface with professional styling and real-time feedback
- **Backend Pipeline**: Orchestrates sequential AI operations from user input to audio output
- **Sunbird AI Integration**: Leverages Sunbird's APIs for STT, summarization, translation, and TTS
- **Audio Processing**: Lightweight audio metadata extraction using Mutagen
- **Error Handling**: Comprehensive retry logic with exponential backoff for API resilience

### Tech Stack

- **Framework**: Python with Gradio for UI
- **Dependencies**: requests, python-dotenv, mutagen, pytest
- **Deployment**: Runs locally or in containerized environments
- **API Integration**: RESTful communication with Sunbird AI endpoints

---

## Key Capabilities

###  Data Protection
- PII anonymization during summarization
- Secure API communication with authentication tokens
- No local storage of user content beyond processing

###  Performance
- Configurable timeouts for different operations (10 min for audio processing, 5 min for other tasks)
- Automatic retry logic with exponential backoff for transient failures
- Optimized for African network conditions

###  Language-Specific Intelligence
- Context-aware translation using Sunbird's Sunflower LLM
- Proper handling of Ugandan language nuances and idioms
- Native speaker voices for authentic audio output

###  Flexible Output Formats
- Generates summaries in different tones (News Bulletin, Community Announcement)
- Multiple output channels (text transcript, summary, translation, audio)
- Display detected source language during transcription

---


## Project Purpose

Umoja democratizes content translation and audio broadcasting for African communities. By removing language barriers and technical complexity, it enables any storyteller to create and share their voice across Uganda's diverse linguistic landscape. Whether it's a journalist breaking news, a health worker sharing vital information, or a community leader broadcasting announcements, Umoja makes professional-quality multi-language content production accessible to everyone.