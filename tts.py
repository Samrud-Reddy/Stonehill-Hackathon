import pyttsx3
from gemini_apicall import response1
import json

json_str = response1
data = json.loads(json_str)
confirm_msg = "\nTap once to confirm. Tap twice to cancel."

amt = "The amount you are paying is: " + data["amount"]
phone_num = "\nThe person you are paying is: " + data["recipient_value"]


with open("file.txt", "w") as file:
    file.write(amt)
    file.write(phone_num)
    file.write(confirm_msg)


engine = pyttsx3.init()

with open('file.txt', 'r') as file:
    text = file.read()

engine.say(text)
engine.runAndWait()