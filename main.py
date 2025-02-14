from website.app import app
import os
from flask import Flask, render_template, request, jsonify, session, redirect
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('PEOPLE_API_KEY')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


redirect_uri = "http://127.0.0.1:1234/login/callback"
scope = "email profile https://www.googleapis.com/auth/contacts.readonly"

contacts_list = {}
AUDIO_FOLDER = "uploads"
os.makedirs(AUDIO_FOLDER, exist_ok=True)
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER

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
    phone = data.get('phone')
    upi = data.get('upi_id')
    pwd = data.get('pwd')

    return jsonify({"message": "Received phone number", "phone": phone})

@app.route('/verification')
def verification():
    return render_template("login.html")

@app.route('/')
def home():
    if "access_token" in session:
        return render_template("mic_page.html")
    else:
        return redirect("/verification")
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=1234)
