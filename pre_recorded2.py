
from gtts import gTTS
import os
mytext = 'Check your Balance'
language = 'en'
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("pre_recorded2.mp3")
os.system("start pre_recorded2.mp3")