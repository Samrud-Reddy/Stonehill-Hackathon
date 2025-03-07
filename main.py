import gemini_apicall
import json
from website.app import app
import asyncio
from urllib.parse import urlencode
import os
from flask import Flask, render_template, request, jsonify, session, redirect, send_from_directory, json
import requests
from dotenv import load_dotenv
import text_to_speech
import speech_to_text
import gemini_webapi

load_dotenv()
API_KEY = os.getenv('PEOPLE_API_KEY')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

UPI_API = "http://127.0.0.1:5000/"

redirect_uri = "http://127.0.0.1:1234/login/callback"
scope = "email profile https://www.googleapis.com/auth/contacts.readonly"

contacts_list = {}
jwt_token = ""
phone = ""
AUDIO_FOLDER = "audio"
os.makedirs(AUDIO_FOLDER, exist_ok=True)
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER

def string_to_json(string_data: str):
    # Remove surrounding markdown and unnecessary whitespace
    app.logger.info(string_data)
    cleaned_string = string_data.strip().strip('"')
    
    # Extract JSON part
    json_start = cleaned_string.find('{')
    json_end = cleaned_string.rfind('}') + 1
    json_string = cleaned_string[json_start:json_end]
    
    json_data = json.loads(json_string)
    return json_data

@app.route('/login')
def login():
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"client_id={CLIENT_ID}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"scope={scope}&"
    )
    return redirect(google_auth_url)

@app.route('/login/callback')
def authorized():
    if 'code' not in request.args:
        return "Authorization failed!", 400

    # Exchange authorization code for an access token
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": request.args["code"],
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    response = requests.post(token_url, data=data)
    token_info = response.json()

    if "access_token" not in token_info:
        return "Failed to obtain access token\n"+str(token_info), 400

    access_token = token_info["access_token"]
    session["access_token"] = access_token

    contacts_url = "https://people.googleapis.com/v1/people/me/connections"
    params = {"personFields": "names,phoneNumbers"}
    headers = {"Authorization": f"Bearer {access_token}"}

    contacts_response = requests.get(contacts_url, headers=headers, params=params)
    contacts = contacts_response.json()

    for person in contacts.get("connections", []):
        contacts_list[str(person.get("names", [])[0].get("displayName", "Unknown"))] = str(person.get("phoneNumbers", [{}])[0].get("value", "No Phone"))


    return redirect("/")

@app.route("/upload", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        filepath = os.path.join(app.config["AUDIO_FOLDER"], file.filename)
        file.save(filepath)
        return jsonify({"message": "File uploaded successfully", "path": filepath}), 200
    return 


@app.route('/get-data', methods=["POST"])
def get_data():
    data = request.form  # Gets data sent via x-www-form-urlencoded (default for $.ajax)
    global phone
    phone = data.get('phone')
    upi = data.get('upi_id')
    pwd = data.get('pwd')

    params = {
                "phone_number": phone,
                "upi_id": upi,
                "upi_pin": pwd,
            }

    token = requests.post(UPI_API+"/api/user/loginUser", params=urlencode(params))
    token = token.json()["detail"]
    global jwt_token
    jwt_token = token
    return ""

@app.route('/verification')
def verification():
    return render_template("login.html")

@app.route('/audio/<filename>')
def audio(filename):
    return send_from_directory("../"+AUDIO_FOLDER, filename)

@app.route('/balance')
def balance():
    params = {
            "phone_number": phone,
            }

    body = requests.post(UPI_API+"/api/user/checkBalance", params=urlencode(params))
    balance = body.json()["balance"]

    file = text_to_speech.balance(balance)
    to_return = {"file": file}
    return json.dumps(to_return)

@app.route('/payment-audio')
def payment_audio():
    text = speech_to_text.stt("audio/payments.webm") 
    app.logger.info(text)
    
    out = asyncio.run(gemini_apicall.main(text))

    to_return = string_to_json(out)

    if to_return["type"] == "phone":
        file = text_to_speech.confirm_number(to_return["amount"], to_return["recipient"])
    elif to_return["type"] == "contact":
        file = text_to_speech.confirm_contact(to_return["amount"], to_return["recipient"])
    else:
        file = ""

    to_return["audio_file"] = file

    return json.dumps(to_return)

@app.route('/pay', methods=["POST"])
def pay():
    data = request.get_json()
    app.logger.info(data)
    return jsonify({"message": "Data received successfully", "data": data}), 200 

@app.route('/')
def home():
    if "access_token" in session and jwt_token != "":
        return render_template("mic_page.html")
    else:
        return redirect("/verification")
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=1234)
