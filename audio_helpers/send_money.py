import converter
from gtts import gTTS
import os

mytext='Send money'
language = 'en'
myobj= gTTS(text=mytext, lang=language, slow=False)
myobj.save("pre_recorded1.mp3")

converter.convert_mp3_to_webm("pre_recorded1.mp3", "pre_recorded1.webm")
