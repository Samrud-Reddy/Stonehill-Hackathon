from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__, template_folder="view")

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=1234)
