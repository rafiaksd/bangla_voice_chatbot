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
