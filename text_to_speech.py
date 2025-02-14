import pyttsx3
def tts(number):
    contact_number=[f"Is this your contact number { number}"]
    engine = pyttsx3.init()
    engine.setProperty('rate', 115) 
    engine.setProperty('volume',1.0)  
    voices = engine.getProperty('voices')      
    engine.setProperty('voice', voices[1].id) 
    engine.say(contact_number)
    engine.runAndWait()
