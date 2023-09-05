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


# Globals
cancel_flag = False
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


# def scan_thread(event):
#     global cancel
#     global read_error
#
#     # subprocess.run(["rm", "-fr", f"/tmp/card{random_string(4)}"])
#     read = False
#
#     r = random_string(4)
#
#     while not read and not cancel and not event.is_set():
#         result = subprocess.run(
#             ["./bin/nfc-mfclassic", "r", "a", "u", f"/tmp/card{r}"]
#         )
#
#         if result.returncode == 0:
#             if os.path.isfile(f"/tmp/card{r}"):
#                 read = True
#             else:
#                 read_error = True
#
#     if cancel:
#         cancel = False

# def scan_thread(exit_event):
#
#     if not os.path.isfile("./bin/scan"):
#         subprocess.run(["mkdir", "-p", "./bin"])
#         subprocess.run(["gcc", "-o", "./bin/scan", "./nfc-tools/scan.c"])
#
#     while not exit_event.is_set():
#         scan_result = subprocess.check_output(["./bin/scan"], timeout=5)
#
#     print(scan_result.decode('utf-8'))
#
#     return jsonify({"scan_result": scan_result.decode('utf-8')}), 200




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



# @app.route("/scan-card", methods=["POST"])
# def scan_card():
#
#     card_data = {
#         "UID": "de ad be ef",
#         "card_type": "Mifare Classic 1K"
#                  }
#
#     time.sleep(2)
#
#     return jsonify(card_data), 200

# @app.route("/scan-card", methods=["POST"])
# def scan_card():
#     event = threading.Event()
#     new_thread = threading.Thread(target=scan_thread, args=[event])
#     new_thread.start()
#     new_thread.join(30)
#
#     if new_thread.is_alive():
#         event.set()
#         return "timeout"
#         return jsonify({"message": "timeout"}), 408
#     
#     return jsonify({"message": "ok"}), 200


# @app.route("/scan-card", methods=["POST"])
# def scan_card():
#
#     exit_event = threading.Event()
#     new_thread = threading.Thread(target=scan_thread, args=[exit_event])
#     print(new_thread.name)
#     # new_thread.start()
#
#     return jsonify({"scan_result": "blaaah"}), 200

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
    return jsonify({"message": "totally saved fr"})


# @app.route("/save-card", methods=["POST"])
# def save_card():
#     name = request.form.get("name")
#     new_card = Card(name)
#
#     with open("/tmp/temp_card_data", "rb") as f:
#         data = f.read()
#
#     with open(f"./cards/{name}", "wb") as f:
#         f.write(data)
#
#     uid, card_type, strings = parse(data)
#     new_card.uid = uid
#     new_card.type = card_type
#     new_card.strings = strings
#
#     with app.app_context():
#         db.session.add(new_card)
#         db.session.commit()
#
#     return redirect("/", code=302)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
