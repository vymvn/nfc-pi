import os
import subprocess
import time
import threading
import signal

from flask import Flask, render_template, request, redirect
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from parser import parse


# Globals
cancel = False
read_error = False


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
    type = db.Column(db.String)
    uid = db.Column(db.String)
    strings = db.Column(db.String)
    dump_file = f"cards/{name}"

    def __init__(self, name: str):
        self.name = name


with app.app_context():
    db.create_all()


def scan_thread(event):
    global cancel
    global read_error

    subprocess.run(["rm", "-fr", "/tmp/temp_card_data"])
    read = False

    while not read and not cancel and not event.is_set():
        result = subprocess.run(
            ["./bin/nfc-mfclassic", "r", "a", "u", "/tmp/temp_card_data"]
        )
        if result.returncode == 0:
            if os.path.isfile("/tmp/temp_card_data"):
                read = True
            else:
                read_error = True
    if cancel:
        cancel = False


@app.route("/")
def main():

    with app.app_context():
        cards = db.session.execute(db.select(Card).order_by(Card.name)).scalars().all()
        
    return render_template("index.html", cards=cards)


@app.route("/cancel-scan", methods=["POST"])
def cancel_scan():
    global cancel
    cancel = True
    return redirect("/", code=302)


@app.route("/scan-card", methods=["POST"])
def scan_card():
    event = threading.Event()
    new_thread = threading.Thread(target=scan_thread, args=[event])
    new_thread.start()
    new_thread.join(30)
    if new_thread.is_alive():
        event.set()
        return "timeout"
    
    return "ok"



@app.route("/save-card", methods=["POST"])
def save_card():
    name = request.form.get("name")
    new_card = Card(name)
    with open("/tmp/temp_card_data", "rb") as f:
        data = f.read()
    with open(f"./cards/{name}", "wb") as f:
        f.write(data)
    uid, card_type, strings = parse(data)
    new_card.uid = uid
    new_card.type = card_type
    new_card.strings = strings

    with app.app_context():
        db.session.add(new_card)
        db.session.commit()

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)