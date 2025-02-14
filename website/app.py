import os
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__, template_folder="view")

AUDIO_FOLDER = "uploads"
os.makedirs(AUDIO_FOLDER, exist_ok=True)
app.config["AUDIO_FOLDER"] = AUDIO_FOLDER

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



@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=1234)
