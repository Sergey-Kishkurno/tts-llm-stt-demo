import os
import pyttsx3
import requests
from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import json

# Initialize OpenRouter API key (replace with your actual key)
API_KEY = os.getenv("OPENROUTER_API_KEY") or "YOUR_OPENROUTER_API_KEY"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Initialize text-to-speech engine
engine = pyttsx3.init()


def listen_to_microphone():
    """Listen to microphone and return audio data"""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for ambient noise
        recognizer.adjust_for_ambient_noise(source)
        # Listen for audio (timeout after 5 seconds)
        audio = recognizer.listen(source, timeout=5)

    return audio


def transcribe_audio(audio):
    """Transcribe audio to text using OpenAI Whisper API"""
    # Save audio to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        # Save audio data to file
        with open(tmp_file.name, "wb") as f:
            f.write(audio.get_wav_data())

        # Transcribe using OpenAI (still using OpenAI's Whisper)
        with open(tmp_file.name, "rb") as f:
            # Use OpenAI for transcription (this is still OpenAI's service)
            import openai
            openai.api_key = os.getenv("OPENAI_API_KEY") or "YOUR_OPENAI_API_KEY"
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=f,
                response_format="verbose_json"
            )

        # Clean up temporary file
        os.unlink(tmp_file.name)

    return transcript.text


def generate_response(prompt):
    """Generate response using OpenRouter with Llama-3.3-70B model"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error calling OpenRouter API: {e}")
        return "Sorry, I encountered an error processing your request."


def text_to_speech(text, language="en"):
    """Convert text to speech and play it"""
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Set language
    engine.setProperty('voice',
                       'com.apple.speech.synthesis.voice.Alex' if language == "en" else 'com.apple.speech.synthesis.voice.Samantha')

    engine.say(text)
    engine.runAndWait()


def main():
    """Main loop for voice assistant"""
    print("Voice Assistant Started. Say 'quit' to exit.")

    while True:
        try:
            # Step 1: Listen to microphone
            audio = listen_to_microphone()

            # Step 2: Transcribe audio to text
            transcript = transcribe_audio(audio)
            print(f"Transcribed: {transcript}")

            # Exit condition
            if transcript.lower().strip() in ["quit", "exit", "goodbye"]:
                print("Goodbye!")
                break

            # Step 3: Generate response using OpenRouter Llama model
            response_text = generate_response(transcript)
            print(f"Assistant: {response_text}")

            # Step 4: Convert response to speech
            text_to_speech(response_text)

        except Exception as e:
            print(f"Error occurred: {e}")
            continue


if __name__ == "__main__":
    main()
