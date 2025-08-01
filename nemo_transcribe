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

auido_file = "mic_input_dynamic.wav"
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

print("========================================")
print("========================================")
print(transcriptions)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(transcription_text)

os.remove(audio_converted)
print("🗑️🗑️🗑️  Cleaned temporary audio...")

get_time_lapsed(start_time)