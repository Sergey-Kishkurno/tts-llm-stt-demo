# TTS-LLM-STT Demo

## Basic Scenario

You run `main.py` to start a simple **voice assistant loop** on your Mac.

1. **Startup**
   - The program prints a message like: *“Voice Assistant Started. Say 'quit' to exit.”*
   - It initializes a local **text-to-speech** engine (so it can speak responses out loud).

2. **A person speaks**
   - The assistant begins listening to your microphone.
   - It briefly adjusts for ambient noise, then captures a short audio segment (with a timeout).

3. **Speech → text (transcription)**
   - The recorded audio is saved to a temporary `.wav` file.
   - That file is sent to a speech-to-text service (Whisper) to get a **transcribed text string**.
   - The temporary file is deleted.
   - The assistant prints the transcript to the console (so you can see what it heard).

4. **Exit check**
   - If what you said is essentially **“quit” / “exit” / “goodbye”**, it prints *“Goodbye!”* and stops.

5. **Text → LLM response**
   - Otherwise, your transcript is sent as a prompt to an LLM endpoint (via OpenRouter) using a chat-completions request.
   - The assistant receives a generated answer and prints it to the console.

6. **LLM response → spoken audio**
   - The assistant speaks the generated response aloud using the system voice.

7. **Repeat forever (until you quit)**
   - The loop continues: listen → transcribe → respond → speak.
   - If any error happens (mic issue, network, API error, etc.), it prints the error and goes back to listening again.



## Languages Capabilities

OpenRouter - Multimodal
https://openrouter.ai/docs/guides/overview/multimodal/overview


OpenRouter - Audio
https://openrouter.ai/docs/guides/overview/multimodal/audio#sending-audio-files


TranslateGemma - 55 languages
https://blog.google/innovation-and-ai/technology/developers-tools/translategemma/



