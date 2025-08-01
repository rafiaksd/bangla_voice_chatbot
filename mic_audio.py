import sounddevice as sd
import soundfile as sf

duration = 6  # seconds
sample_rate = 44100  # CD-quality

print("Recording...")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()  # Wait until recording is done
print("Done recording.")

mic_output_audio = "mic_input4.wav"
sf.write(mic_output_audio, audio, sample_rate)

print(f"🎙️🎙️ MIC AUDIO CREATED {mic_output_audio}")