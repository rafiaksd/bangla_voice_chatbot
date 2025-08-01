import logging
logging.disable(logging.CRITICAL)

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
### TRANSCRIBE BANGLA
########################

from banglaspeech2text import Speech2Text

stt = Speech2Text("large")
print("📦📦  loaded stt")

audio = mic_output_audio

print("✍️✍️  transcribing started...")
tts_output = stt.recognize(audio)

print(tts_output)
with open("transcribed_text.txt", "w", encoding="utf-8") as file:
    file.write(tts_output)

#################################
### TTS LLM RESPONSE
#################################

from banglatts import BanglaTTS
import winsound, os

tts_text = tts_output

temp_audio = 'temp_talk.wav'

tts = BanglaTTS(save_location="save_model_location")
path = tts(tts_text, voice='female', filename=temp_audio) # voice can be male or female

winsound.PlaySound(temp_audio, winsound.SND_FILENAME)
os.remove(temp_audio)