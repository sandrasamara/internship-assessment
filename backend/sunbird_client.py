"""
sunbird_client.py — Thin wrapper around all Sunbird AI API endpoints.
"""
import os
import json
import time
import requests
from pathlib import Path

BASE_URL = "https://api.sunbird.ai"

# Increased timeouts for free tier API (can be slow)
TIMEOUT_STT = 600  # 10 minutes for audio transcription
TIMEOUT_DEFAULT = 300  # 5 minutes for other endpoints

# Retry configuration
MAX_RETRIES = 3
INITIAL_BACKOFF = 2  # seconds

# TTS speaker IDs per language
SPEAKER_IDS = {
    "Luganda":    248,
    "Acholi":     241,
    "Ateso":      242,
    "Runyankole": 243,
    "Lugbara":    245,
}

# Language codes used as hints for STT display
LANGUAGE_NAMES = {
    "lug": "Luganda",
    "ach": "Acholi",
    "teo": "Ateso",
    "nyn": "Runyankole",
    "lgg": "Lugbara",
    "eng": "English",
}


def _headers_json() -> dict:
    token = os.environ.get("SUNBIRD_API_TOKEN", "")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def _headers_auth() -> dict:
    token = os.environ.get("SUNBIRD_API_TOKEN", "")
    return {"Authorization": f"Bearer {token}"}


def _request_with_retry(
    method: str,
    url: str,
    timeout: int,
    headers: dict,
    **kwargs
) -> requests.Response:
    """
    Make HTTP request with exponential backoff retry on transient errors.
    
    Args:
        method: HTTP method ('post', 'get', etc.)
        url: Request URL
        timeout: Timeout in seconds
        headers: Request headers
        **kwargs: Additional arguments for requests (json, files, etc.)
    
    Returns:
        Response object
        
    Raises:
        requests.RequestException: If all retries fail
    """
    backoff = INITIAL_BACKOFF
    last_exception = None
    
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.request(
                method=method,
                url=url,
                timeout=timeout,
                headers=headers,
                **kwargs
            )
            response.raise_for_status()
            return response
        except (requests.Timeout, requests.ConnectionError) as e:
            last_exception = e
            if attempt < MAX_RETRIES - 1:
                print(f"Attempt {attempt + 1} failed: {type(e).__name__}. Retrying in {backoff}s...")
                time.sleep(backoff)
                backoff *= 2  # Exponential backoff
            else:
                raise
        except requests.RequestException:
            raise  # Don't retry on other request errors
    
    if last_exception:
        raise last_exception


def transcribe_audio(audio_path: str) -> dict:
    """
    Transcribe an audio file using Sunbird STT.
    Returns {"text": str, "language": str} or raises on error.
    """
    url = f"{BASE_URL}/tasks/stt"
    with open(audio_path, "rb") as f:
        files = {"audio": (Path(audio_path).name, f)}
        response = _request_with_retry(
            method="post",
            url=url,
            timeout=TIMEOUT_STT,
            headers=_headers_auth(),
            files=files
        )
    data = response.json()
    output = data.get("output", {})
    lang_code = output.get("language", "")
    return {
        "text": output.get("text", ""),
        "language_code": lang_code,
        "language_name": LANGUAGE_NAMES.get(lang_code, lang_code),
    }


def summarise_text(text: str) -> str:
    """
    Summarise text using the Sunbird summarisation endpoint.
    Returns the summary string or raises on error.
    """
    url = f"{BASE_URL}/tasks/summarise"
    payload = {"text": text}
    response = _request_with_retry(
        method="post",
        url=url,
        timeout=TIMEOUT_DEFAULT,
        headers=_headers_json(),
        json=payload
    )
    data = response.json()
    print(f"[DEBUG] summarise_text response: {json.dumps(data, indent=2)}")
    
    # API returns 'summarized_text' at top level
    if "summarized_text" in data:
        summary = data["summarized_text"]
        if summary and summary.strip():
            return summary
        else:
            raise ValueError(f"Summarisation API returned empty text. Full response: {json.dumps(data, indent=2)}")
    elif "output" in data and "summary" in data["output"]:
        summary = data["output"]["summary"]
        if summary and summary.strip():
            return summary
        else:
            raise ValueError(f"Summarisation API returned empty output.summary. Full response: {json.dumps(data, indent=2)}")
    elif "summary" in data:
        summary = data["summary"]
        if summary and summary.strip():
            return summary
        else:
            raise ValueError(f"Summarisation API returned empty summary. Full response: {json.dumps(data, indent=2)}")
    else:
        raise KeyError(f"Could not find summary in response. Response keys: {list(data.keys())}. Full response: {json.dumps(data, indent=2)}")


def translate_text(text: str, target_language: str) -> str:
    """
    Translate text into a Ugandan local language using Sunflower Chat.
    Returns the translated string or raises on error.
    """
    url = f"{BASE_URL}/tasks/sunflower_inference"
    system_prompt = (
        f"You are a professional translator. Translate the following text into {target_language}. "
        f"Return ONLY the translated text, with no explanations or extra commentary."
    )
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ]
    }
    response = _request_with_retry(
        method="post",
        url=url,
        timeout=TIMEOUT_DEFAULT,
        headers=_headers_json(),
        json=payload
    )
    data = response.json()
    print(f"[DEBUG] translate_text response: {json.dumps(data, indent=2)}")
    
    # API returns 'content' at top level for Sunflower Chat
    if "content" in data:
        content = data["content"]
        if content and content.strip():
            return content
        else:
            raise ValueError(f"Translation API returned empty content. Full response: {json.dumps(data, indent=2)}")
    elif "generated_text" in data:
        content = data["generated_text"]
        if content and content.strip():
            return content
        else:
            raise ValueError(f"Translation API returned empty generated_text. Full response: {json.dumps(data, indent=2)}")
    elif "output" in data and "generated_text" in data["output"]:
        content = data["output"]["generated_text"]
        if content and content.strip():
            return content
        else:
            raise ValueError(f"Translation API returned empty output.generated_text. Full response: {json.dumps(data, indent=2)}")
    else:
        raise KeyError(f"Could not find translation in response. Response keys: {list(data.keys())}. Full response: {json.dumps(data, indent=2)}")


def synthesise_speech(text: str, language: str) -> str:
    """
    Convert text to speech using the Sunbird TTS endpoint.
    Returns the audio URL string or raises on error.
    """
    speaker_id = SPEAKER_IDS.get(language)
    if speaker_id is None:
        raise ValueError(f"No TTS speaker available for language: {language}")

    url = f"{BASE_URL}/tasks/tts"
    payload = {"text": text, "speaker_id": speaker_id}
    response = _request_with_retry(
        method="post",
        url=url,
        timeout=TIMEOUT_DEFAULT,
        headers=_headers_json(),
        json=payload
    )
    data = response.json()
    print(f"[DEBUG] synthesise_speech response: {json.dumps(data, indent=2)}")
    
    # Try common response formats
    if "audio_url" in data:
        audio_url = data["audio_url"]
        if audio_url and audio_url.strip():
            return audio_url
        else:
            raise ValueError(f"TTS API returned empty audio_url. Full response: {json.dumps(data, indent=2)}")
    elif "output" in data and "audio_url" in data["output"]:
        audio_url = data["output"]["audio_url"]
        if audio_url and audio_url.strip():
            return audio_url
        else:
            raise ValueError(f"TTS API returned empty output.audio_url. Full response: {json.dumps(data, indent=2)}")
    else:
        raise KeyError(f"Could not find audio_url in response. Response keys: {list(data.keys())}. Full response: {json.dumps(data, indent=2)}")