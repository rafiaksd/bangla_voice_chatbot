from gtts import gTTS
import os

queries = [
    "অনুপমের লালন-পালন কে করেছেন?", 
    "অনুপমের মা কোন ঘরের মেয়ে?",
    "অনুপম মনে করে তার পূর্ণ বয়স হয়নি কেন?",
    "অনুপমের লজ্জার কারণ কী ছিল ছেলেবেলায়?",
    "অনুপমের ভাষায় সুপুরুষ কাকে বলা হয়েছে?",
]

text = "আপনি কেমন আছেন?"  # Your Bengali text here
tts = gTTS(text=text, lang='bn')
tts.save("output.mp3")

# Play the audio (optional)
os.system("start output.mp3")  # For Windows
# os.system("afplay output.mp3")  # For macOS
# os.system("mpg123 output.mp3")  # For Linux
