import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

app = Flask(__name__)
app.jinja_env.filters["usd"] = usd
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
    if response is None:
        return response
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


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
    

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    user_id = session["user_id"]
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")
        db = connectDB()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        db.close()
        if not user or not check_password_hash(user["hash"], current_password):
            return apology("Current password is incorrect", 403)

        if not new_password or not confirm_password:
            return apology("New password cannot be blank", 403)
        if new_password != confirm_password:
            return apology("New passwords do not match", 403)

        hashed_password = generate_password_hash(new_password, method='scrypt', salt_length=16)
        
        db = connectDB()
        db.execute("UPDATE users SET hash = ? WHERE id = ?", (hashed_password, user_id))
        db.commit()
        db.close()

        flash("Password changed successfully!")
        return redirect("/")
    return render_template("change_password.html")


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    db = connectDB()
    try:
        userInfo = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        userShares = db.execute(
            "SELECT symbol, SUM(shares) AS total_shares "
            "FROM transactions WHERE user_id = ? GROUP BY symbol", 
            (user_id,)
        ).fetchall()
        portfolio_value = 0
        shares_info = []
        for share in userShares:
            stock = lookup(share["symbol"])
            if stock:
                if share["total_shares"] > 0:
                    total_value = stock["price"] * share["total_shares"]
                    portfolio_value += total_value
                    shares_info.append({
                        "symbol": share["symbol"],
                        "shares": share["total_shares"],
                        "price": stock["price"],
                        "total": total_value
                    })
            else:
                print(f"Stock {share['symbol']} not found.")
        grand_total = portfolio_value + userInfo["cash"]
        return render_template("index.html", userInfo=userInfo, userTransactionInfo=shares_info, grand_total=grand_total)
    except Exception as e:
        print(f"Error: {e}")
        return apology("Something went wrong. Please try again later.")
    finally:
        db.close()


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
        db.execute(
            "INSERT INTO buy_sell_transactions (user_id, symbol, shares, price, action) VALUES (?, ?, ?, ?, ?)",
            (user_id, symbol, shares, share_price, 'buy')
        )
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?, ?, ?, ?)",
            (user_id, symbol, shares, share_price) 
        )

        db.commit()
        db.close()
        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    db = connectDB()
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares_2_sell = request.form.get("shares")
        if not symbol:
            db.close()
            return apology("Invalid stock selected.")
        if not shares_2_sell or not shares_2_sell.isdigit():
            db.close()
            return apology("Invalid number of shares.")
        shares_2_sell = int(shares_2_sell)
        if shares_2_sell <= 0:
            db.close()
            return apology("Shares to sell must be a positive integer.")
        userShares = db.execute(
            "SELECT SUM(shares) AS total_shares "
            "FROM transactions WHERE user_id = ? AND symbol = ? "
            "GROUP BY symbol", (user_id, symbol)
        ).fetchone()
        if not userShares or userShares["total_shares"] < shares_2_sell:
            db.close()
            return apology("Not enough shares to sell.")
        stock = lookup(symbol)
        if not stock:
            db.close()
            return apology("Couldn't find stock.")
        sale_val = stock["price"] * shares_2_sell
        db.execute(
            "INSERT INTO buy_sell_transactions (user_id, symbol, shares, price, action) "
            "VALUES (?, ?, ?, ?, ?)", 
            (user_id, symbol, -shares_2_sell, stock["price"], 'sell')  # Insert sell action into buy_sell_transactions
        )
        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) "
            "VALUES (?, ?, ?, ?)", 
            (user_id, symbol, -shares_2_sell, stock["price"])  # Negative shares for sell in transactions
        )
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?", 
            (sale_val, user_id)
        )

        db.commit()
        db.close()
        return redirect("/")
    else:
        userTransactionInfo = db.execute(
            "SELECT symbol, SUM(shares) AS total_shares "
            "FROM transactions WHERE user_id = ? "
            "GROUP BY symbol HAVING total_shares > 0",
            (user_id,)
        ).fetchall()
        db.close()
        return render_template("sell.html", userTransactionInfo=userTransactionInfo)


@app.route("/history")
@login_required
def history():
    """Show the history of transactions"""
    db = connectDB()
    try:
        user_transactions = db.execute(
            "SELECT symbol, shares, price, action, timestamp FROM buy_sell_transactions WHERE user_id = ? ORDER BY timestamp DESC",
            (session["user_id"],)
        ).fetchall()
        transaction_history = []
        for transaction in user_transactions:
            transaction_history.append({
                "symbol": transaction["symbol"],
                "shares": abs(transaction["shares"]), 
                "price": transaction["price"],
                "action": transaction["action"],
                "timestamp": transaction["timestamp"] 
            })
        return render_template("history.html", transactions=transaction_history)
    except Exception as e:
        print(f"Error: {e}")
        return apology("Something went wrong. Please try again later.")
    finally:
        db.close()


