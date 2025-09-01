import logging
logging.disable(logging.CRITICAL)

import sounddevice as sd
import soundfile as sf
import numpy as np
import nemo.collections.asr as nemo_asr
import os, time, threading
from ollama import chat
from banglatts import BanglaTTS
import pygame

LLM_MODEL = "gemma3:1b"
asr_model = nemo_asr.models.ASRModel.from_pretrained("hishab/titu_stt_bn_fastconformer")
print(f"✅✅ Loaded ASR model and LLM 🧠 {LLM_MODEL}")

tts = BanglaTTS(save_location="save_model_location")

chat_history = []
MAX_HISTORY = 12
def generate_answer(query: str) -> str:
    global chat_history

    # Append current user query
    chat_history.append({"role": "user", "content": query})

    messages = [{"role": "system", "content": "তুমি একজন বাংলা ভয়েস অ্যাসিস্ট্যান্ট। সহজ, পরিষ্কার এবং সংক্ষিপ্ত উত্তর দাও — তবে খুব ছোট নয়। প্রশ্ন বুঝে প্রাসঙ্গিকভাবে উত্তর দাও।"}] + chat_history

    # Keep only last 12 messages (6 user + 6 assistant)
    if len(chat_history) > MAX_HISTORY:
        chat_history = chat_history[-MAX_HISTORY:]

    response = chat(model=LLM_MODEL, messages=messages)
    chat_history.append({"role": "assistant", "content": response["message"]["content"]})

    return response["message"]["content"]

def get_time_lapsed(start_time, emojis="⏰⏱️"):
    now_time = time.time()
    time_elapse = now_time - start_time
    print(f"{emojis}   Time elapsed: {time_elapse:.2f} seconds\n")

def record_audio(output_filename="mic_input_dynamic.wav", sample_rate=16000, channels=1):
    print("🎙️ Press Enter to start recording...")
    input()
    print("⏺️ Recording... Press Enter again to stop.")

    recorded_frames = []

    def callback(indata, frames, time, status):
        if status:
            print(f"⚠️ {status}")
        recorded_frames.append(indata.copy())

    with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback):
        input()
        print("🛑 Stopped recording.")

    audio_data = np.concatenate(recorded_frames, axis=0)
    sf.write(output_filename, audio_data, sample_rate)
    print(f"✅ Saved recording to {output_filename}")
    return output_filename

def transcribe(audio_path: str):
    #converted_path = audio_path.split(".")[0] + "_converted.wav"
    #audio = AudioSegment.from_file(audio_path)
    #audio = audio.set_channels(1)
    #audio.export(converted_path, format="wav")
    print("📜📜 Started transcribing...")
    
    # The fix is on this line: asr_model.transcribe returns a list of strings.
    # We just need to access the first item directly.
    transcriptions = asr_model.transcribe([audio_path])
    transcription_text = transcriptions[0]

    print(transcription_text)
    #os.remove(converted_path)
    print("🗑️ Cleaned temporary audio...")
    return transcription_text

def play_audio_with_stop(audio_path):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    def wait_for_enter():
        input("Press Enter to stop playback...\n")
        pygame.mixer.music.stop()
        print("🚫🚫 Playback stopped.")

        pygame.mixer.quit()
        time.sleep(0.2)

    t = threading.Thread(target=wait_for_enter)
    t.start()
    t.join()

def speak(text: str):
    print(f"🧠 LLM: {text}")
    temp_audio = 'temp_talk.wav'
    path = tts(text, voice='female',filename=temp_audio)
    
    play_audio_with_stop(temp_audio)
    os.remove(temp_audio)

# MAIN LOOP
with open("current_chatting.txt", "w", encoding="utf-8") as file:
    file.write("")
    
while True:
    try:
        print("\n🔁 Ready for next interaction (press Ctrl+C to exit)")

        mic_output_audio = record_audio()

        start_time = time.time()
        transcription = transcribe(mic_output_audio)
        with open("current_chatting.txt", "a", encoding="utf-8") as file:
          file.write(transcription + "\n")
        #os.remove(mic_output_audio)

        llm_response = generate_answer(transcription)
        get_time_lapsed(start_time)

        with open("current_chatting.txt", "a", encoding="utf-8") as file:
          file.write("  -- " + llm_response + "\n\n")
        speak(llm_response)

    except KeyboardInterrupt:
        print("\n👋 Exiting voice assistant...")
        break
    except Exception as e:
        print(f"⚠️ Error: {e}")