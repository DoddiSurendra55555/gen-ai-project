
import io
import os
import time
import wave

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

TRANSCRIPTION_MODEL = "gemini-3.1-flash-lite"
VOICE_MODEL = "gemini-3.8-flash-tts"
VOICE_NAME = "Kore"


def get_gemini_client():
    """Create a Gemini client using the API key in .env."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY was not found. "
            "Please check your .env file."
        )

    return genai.Client(api_key=api_key)


def _generate_with_retry(client, model, contents, config=None):
    """Retry temporary Gemini server errors."""

    for attempt in range(3):
        try:
            return client.models.generate_content(
                model=model,
                contents=contents,
                config=config,
            )

        except Exception as error:
            error_message = str(error)

            temporary_error = (
                "503" in error_message
                or "429" in error_message
                or "UNAVAILABLE" in error_message.upper()
            )

            if temporary_error and attempt < 2:
                time.sleep(2 ** (attempt + 1))
                continue

            raise RuntimeError(
                f"Gemini request failed: {error}"
            ) from error

    raise RuntimeError("Gemini request failed after retries.")


def transcribe_audio(audio_bytes):
    """
    Convert a recorded English WAV answer into text.

    Args:
        audio_bytes: Recorded audio in WAV format.

    Returns:
        Transcribed English text.
    """

    if not audio_bytes:
        raise ValueError("No audio recording was provided.")

    if not isinstance(audio_bytes, bytes):
        raise ValueError("Invalid audio data.")

    client = get_gemini_client()

    audio_part = types.Part.from_bytes(
        data=audio_bytes,
        mime_type="audio/wav",
    )

    prompt = (
        "Transcribe the spoken English audio accurately. "
        "Return only the words spoken by the speaker. "
        "Do not summarize, translate, or add explanations. "
        "If the recording contains no understandable speech, "
        "return an empty response."
    )

    response = _generate_with_retry(
        client=client,
        model=TRANSCRIPTION_MODEL,
        contents=[prompt, audio_part],
    )

    transcript = (response.text or "").strip()

    if not transcript:
        raise ValueError(
            "No understandable speech was detected. "
            "Please record your answer again."
        )

    return transcript


def generate_speech(text):
    """
    Convert text into spoken English audio.

    Args:
        text: Text that the AI interviewer should speak.

    Returns:
        WAV audio bytes ready for Streamlit playback.
    """

    if not text or not text.strip():
        raise ValueError("No text was provided for voice generation.")

    client = get_gemini_client()

    prompt = (
        "Speak clearly and naturally in English like a "
        "professional and friendly job interviewer. "
        "Read the following text exactly as written:\n\n"
        + text.strip()
    )

    config = types.GenerateContentConfig(
        response_modalities=["AUDIO"],
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=VOICE_NAME
                )
            )
        ),
    )

    response = _generate_with_retry(
        client=client,
        model=VOICE_MODEL,
        contents=prompt,
        config=config,
    )

    audio_data = None
    mime_type = None

    for part in response.parts:
        if part.inline_data is not None:
            audio_data = part.inline_data.data
            mime_type = part.inline_data.mime_type
            break

    if not audio_data:
        raise RuntimeError(
            "Gemini did not return any audio data."
        )

    # If Gemini already returned a WAV file, use it directly.
    if audio_data.startswith(b"RIFF"):
        return audio_data

    # Gemini TTS normally returns raw PCM audio.
    # Convert it into WAV so Streamlit can play it.
    if mime_type and (
        "pcm" in mime_type.lower()
        or "l16" in mime_type.lower()
    ):
        wav_buffer = io.BytesIO()

        with wave.open(wav_buffer, "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(24000)
            wav_file.writeframes(audio_data)

        return wav_buffer.getvalue()

    raise RuntimeError(
        f"Unsupported Gemini audio format: {mime_type}"
    )
