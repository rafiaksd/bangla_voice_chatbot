from faster_whisper import WhisperModel

model = WhisperModel("large-v3")

segments, info = model.transcribe("temp_talk.mp3")
for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

