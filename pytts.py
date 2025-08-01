from banglatts import BanglaTTS
import winsound, os

temp_audio = 'temp_talk.wav'

tts = BanglaTTS(save_location="save_model_location")
path = tts("আমি বাংলায় কথা বলতে পারি।", voice='female', filename=temp_audio) # voice can be male or female

winsound.PlaySound(temp_audio, winsound.SND_FILENAME)
os.remove(temp_audio)