import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def connectDB():
    db = sqlite3.connect("finance.db")
    db.row_factory = sqlite3.Row
    return db


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    user_id = session["user_id"]
    db = connectDB()

    userInfo = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    userTransactionInfo = db.execute("SELECT * FROM transactions WHERE user_id =  ? ", (user_id,)).fetchall()


    db.close()
    return render_template("index.html", userInfo=userInfo, userTransactionInfo = userTransactionInfo)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("s_symbol")
        if not symbol:
            return apology("Symbol cannot be blank.")

        stock = lookup(symbol)
        if not stock:
            return apology("Invalid symbol.")
        
        share_price = stock["price"]

        try:
            shares = int(request.form.get("s_amount"))
            if shares <= 0:
                raise ValueError
        except ValueError:
            return apology("Invalid number of shares")
        
        total = share_price * shares

        db = connectDB()
        user_id = session["user_id"]
        user = db.execute("SELECT cash FROM users WHERE id = ?", (user_id,)).fetchone()

        if not user:
            db.close()
            return apology("User not found.")
        
        cash = user["cash"]

        if cash < total:
            db.close()
            return apology("Insufficient funds")
        
        db.execute("UPDATE users SET cash = cash - ? WHERE id = ?", (total, user_id))
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)", (user_id, symbol, shares, share_price))
        db.commit()
        db.close

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        db = connectDB()
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        db.close()

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        s = request.form.get("s_symbol")

        results = lookup(s)

        if results:
            return render_template("/quoted.html", stock_quote=results)
        else:
            flash("Invalid symbol.")

            return redirect("/quote")
        
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if(request.form.get("password") != request.form.get("password-c") or request.form.get("username") == "" or request.form.get("password") == "" or request.form.get("password-c") == ""):
            return apology("Passwords do not match!")

        db = connectDB()
        uname = request.form.get("username")
        hashedPassword = generate_password_hash(request.form.get("password"), method='scrypt', salt_length=16)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (uname, hashedPassword))
        db.commit()
        db.close()

        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
