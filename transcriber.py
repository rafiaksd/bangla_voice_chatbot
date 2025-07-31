import time, winsound
from banglaspeech2text import Speech2Text

def get_time_lapsed(start_time, emojis="⏰⏱️"):
    now_time = time.time()
    time_elapse = now_time - start_time
    print(f"{emojis}   Time elapsed: {time_elapse:.2f} seconds\n")
    return round(time_elapse, 2)

transcribe_start_time = time.time()

stt = Speech2Text("large")

print(f"📜Transcription Started...")
transcription = stt.recognize("testbangla.mp3")

print("✅ Transcription done")
print(transcription)
with open("transcribed_text.txt", "w", encoding="utf-8") as file:
    file.write(transcription)

get_time_lapsed(transcribe_start_time, "✍️✍️")
winsound.Beep(1000,500)