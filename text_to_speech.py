from gtts import gTTS
import converter
import os

def generate_tts(text, filepath):
    language = 'en'
    myobj = gTTS(text=text, lang=language, slow=False)
    path = "audio/"+filepath
    myobj.save(path)
    converter.convert_mp3_to_webm(path)

#Static
def enter_pin():
    text = f"Tap out your pin, Tap x number of times where is x is the digits of pin, give a 1 second break between digits"
    generate_tts(text, "enter_pin.mp3") 
    return "enter_pin.webm"

#Static
def generate_choose():
    text = "Tap once to check balance, tap twice to send money"
    generate_tts(text, "generate_choose.mp3") 
    return "generate_choose.webm"

#Static
def how_to_use_mic():
    text = "Press and hold the mic to start speaking, release to send message"
    generate_tts(text, "how_to_use_mic") 
    return "how_to_use_mic.webm"

#Static
def payment_complete():
    text = "Payment succsessfull"
    generate_tts(text, "payment_complete") 
    return "payment_complete.webm"

#Static
def upi_instructions():
    text = "Enter your UPI by tapping out the your digits"
    generate_tts(text, "upi_instructions") 
    return "upi_instructions.webm"

def balance(price):
    text = f"Your Balance is {price}"
    generate_tts(text, "balance.mp3") 
    return "balance.webm"

def confirm_number(price, number):
    text = f"Are you sure you want to pay {price} rupees to {number}. Tap once for yes Tap twice for no."
    generate_tts(text, "confirm_number.mp3") 
    return "confirm_number.webm"

def confirm_upi_id(price, upi_id):
    text = f"Are you sure you want to pay {price} to {upi_id}. Tap once for yes Tap twice for no."
    generate_tts(text, "confirm_upi_id.mp3") 
    return "confirm_upi_id.webm"

def confirm_contact(price, contact_number):
    text = f"Are you sure you want to pay {price} rupees to {contact_number}. Tap once for yes Tap twice for no."
    generate_tts(text, "confirm_contact.mp3") 
    return "confirm_contact.webm"

enter_pin()
generate_choose()
how_to_use_mic()
payment_complete()
upi_instructions()
