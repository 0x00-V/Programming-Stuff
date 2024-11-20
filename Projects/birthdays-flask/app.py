import os
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

def dbConn():
    db = sqlite3.connect("birthdays.db")
    db.row_factory = sqlite3.Row
    return db

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    ## Too lazy to add more input validation. But this works
    if request.method == "POST":
        name = request.form.get("name")
        if not name:
            redirect("/")
        month = request.form.get("month")
        if not month:
            redirect("/")
        day = request.form.get("day")
        if not day:
            redirect("/")

        db = dbConn()
        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", (name, month, day))
        db.commit()
        db.close()
        return redirect("/")
    else:
        db = dbConn()
        bds = db.execute("SELECT * FROM birthdays")
        results = bds.fetchall()
        db.close()
        print(results)
        return render_template("index.html", birthdays=results)
        


