import os
import subprocess
import time
import threading
import signal
import random

from flask import Flask, render_template, request, redirect, jsonify
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from parser import parse
from utils import random_string


# Path of folder that contains our html
template_path = os.path.abspath("templates")
static_path = os.path.abspath("static")
db_path = os.path.abspath("cards.db")
app = Flask(
    __name__, template_folder=template_path, static_folder=static_path
)  # Initializing flask app

# create the extension
db = SQLAlchemy()

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"

# initialize the app with the extension
db.init_app(app)

os.system("/usr/bin/mkdir -p cards")


# Card database model
class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    uid = db.Column(db.String)
    atqa = db.Column(db.String)
    sak = db.Column(db.String)
    type = db.Column(db.String)
    ats = db.Column(db.String)

    def __init__(self, name: str):
        self.name = name


with app.app_context():
    db.create_all()


# ================================================= Start of routes ==============================================================#

@app.route("/")
def main():

    # Query SQLite DB and render index
    with app.app_context():
        cards = db.session.execute(db.select(Card).order_by(Card.name)).scalars().all()
        
    return render_template("index.html", cards=cards)


@app.route("/cancel-scan", methods=["POST"])
def cancel_scan():
    global cancel_flag
    cancel_flag = True
    return redirect("/", code=302)



@app.route("/scan-card", methods=["POST"])
def scan_card():
    global cancel_flag
    
    cancel_flag = False
    
    if not os.path.isfile("./bin/scan"):
        subprocess.run(["mkdir", "-p", "./bin"])
        subprocess.run(["gcc", "-o", "./bin/scan", "./nfc-tools/scan.c", "-lnfc"])

    while not cancel_flag:
        try:
            scan_result = subprocess.check_output(["./bin/scan"], timeout=2)
        except subprocess.TimeoutExpired:
            continue
        if scan_result:
            break

    if cancel_flag:
        cancel_flag = False
    else:
        return jsonify({"scan_result": scan_result.decode('utf-8')}), 200



@app.route("/save-card", methods=["POST"])
def save_card():
    data = request.get_json()

    new_card = Card(data.get('card_name'))
    
    info_list = data.get('scan_info').split('\n')

    if len(info_list) > 4:
        ats = True


    new_card.uid = info_list[0].split(':')[1].strip()
    new_card.atqa = info_list[1].split(':')[1].strip()
    new_card.sak = info_list[2].split(':')[1].strip()
    new_card.type = info_list[3].split(':')[1].strip()

    if ats:
        new_card.ats = info_list[4].split(':')[1].strip()

    with app.app_context():
        db.session.add(new_card)
        db.session.commit()


    return jsonify({"message": f"{data.get('card_name')} saved"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
