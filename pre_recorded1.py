from gtts import gTTS
import os
mytext='Send money'
language = 'en'
myobj= gTTS(text=mytext, lang=language, slow=False)
myobj.save("pre_recorded1.mp3")
os.system("start pre_recorded1.mp3")