import speech_recognition as sr
from banglaspeech2text import Speech2Text

stt = Speech2Text("large")

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    output = stt.recognize(audio)

print(output)