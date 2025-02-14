import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify, session, redirect


app = Flask(__name__, template_folder="view")

app.secret_key = os.urandom(24)

