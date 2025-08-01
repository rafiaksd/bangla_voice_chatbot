########################
### MIC VOICE RECORD
########################
 
import sounddevice as sd
import soundfile as sf
import numpy as np

print("🎙️ Press Enter to start recording...")
input()
print("⏺️ Recording... Press Enter again to stop.")

sample_rate = 44100
channels = 1
recorded_frames = []

def callback(indata, frames, time, status):
    if status:
        print(f"⚠️ {status}")
    recorded_frames.append(indata.copy())

# Open audio stream
with sd.InputStream(samplerate=sample_rate, channels=channels, callback=callback):
    input()  # Wait for Enter to stop
    print("🛑 Stopped recording.")

# Combine all recorded chunks
audio_data = np.concatenate(recorded_frames, axis=0)

# Save the result
mic_output_audio = "mic_input_dynamic.wav"
sf.write(mic_output_audio, audio_data, sample_rate)
print(f"✅ Saved recording to {mic_output_audio}")

########################
### NEMO TRANSCRIBE
########################

from pydub import AudioSegment
import nemo.collections.asr as nemo_asr
from nemo.utils import logging as nemo_logging
import os, time

nemo_logging.setLevel("ERROR")

def get_time_lapsed(start_time, emojis="⏰⏱️"):
    now_time = time.time()
    time_elapse = now_time - start_time
    print(f"{emojis}   Time elapsed: {time_elapse:.2f} seconds\n")
    return round(time_elapse, 2)

start_time = time.time()

auido_file = mic_output_audio
audio_converted = auido_file.split(".")[0] + ".wav"

# Convert to mono WAV
audio = AudioSegment.from_file(auido_file)
audio = audio.set_channels(1)  # mono
audio.export(audio_converted, format="wav")

asr_model = nemo_asr.models.ASRModel.from_pretrained("hishab/titu_stt_bn_fastconformer")
print("✅✅ Loaded asr model")

print("📜📜Started transcribing...")
transcriptions = asr_model.transcribe([audio_converted])
transcription_text = transcriptions[0].text

with open("current_chatting.txt", "w", encoding="utf-8") as file:
    file.write(transcription_text + "\n")


print("========================================")
print("========================================")
print(transcriptions)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(transcription_text)

os.remove(audio_converted)
print("🗑️🗑️🗑️  Cleaned temporary audio...")

get_time_lapsed(start_time)

#################################
### GENERATE LLM RESPONSE
#################################
from ollama import chat
LLM_MODEL = "gemma3:4b" #gemma3:4b-it-qat

def generate_answer(query: str) -> str:
    response = chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": "তুমি একজন সহজ ভাষায় উত্তর দেওয়া বাংলা ভয়েস অ্যাসিস্ট্যান্ট। সংক্ষেপে উত্তর দাও।"
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )
    return response["message"]["content"]

llm_bangla_query = transcription_text
llm_response = generate_answer(llm_bangla_query)

with open("current_chatting.txt", "a", encoding="utf-8") as file:
    file.write("  -- " + llm_response + "\n\n")

#################################
### TTS LLM RESPONSE
#################################

from banglatts import BanglaTTS
import winsound, os

tts_text = llm_response

temp_audio = 'temp_talk.wav'

tts = BanglaTTS(save_location="save_model_location")
path = tts(tts_text, voice='female', filename=temp_audio) # voice can be male or female

winsound.PlaySound(temp_audio, winsound.SND_FILENAME)
os.remove(temp_audio)