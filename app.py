from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from chatbot.chatbot import bot   # rule-based chatbot
import os
app = Flask(__name__)
app.secret_key = "testkey"   # needed for session

# ============================
# ROUTES
# ============================

# Redirect root to login
@app.route("/")
def root():
    return redirect(url_for("login"))

# -----------------------------
# LOGIN PAGE
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        account = request.form.get("account")
        password = request.form.get("password")

        if account == session.get("user_account") and password == session.get("user_password"):
            session["user_account"] = account
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid account or password."

    return render_template("login.html", error=error)

# -----------------------------
# SIGNUP PAGE
# -----------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        acc = request.form.get("accountNumber")
        bal = request.form.get("currentBalance")
        name = request.form.get("accountName")
        email = request.form.get("email")
        phone = request.form.get("phone")
        prev = request.form.get("prevTxn")
        txn = request.form.get("txnType")
        pwd = request.form.get("password")

        # SAVE to session
        session["user_account"] = acc
        session["user_name"] = name
        session["user_balance"] = bal
        session["user_email"] = email
        session["user_phone"] = phone
        session["user_prevTxn"] = prev
        session["user_txnType"] = txn
        session["user_password"] = pwd

        return redirect(url_for("login"))

    return render_template("signup.html")

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
@app.route("/dashboard")
def dashboard():
    #username = session.get("user_name", "User")
    return render_template("home.html")

# -----------------------------
# CHATBOT UI PAGE
# -----------------------------
@app.route("/chatbot")
def chatbot_page():
    return render_template("chatbot.html")

# -----------------------------
# CHATBOT API (POST)
# -----------------------------
@app.route("/get", methods=["POST"])
def chat():
    user_message = request.form["message"]
    reply = bot(user_message)
    return jsonify({"response": reply})

@app.route("/profile")
def profile():
    # 1) Require login
    if "user_account" not in session:
        return redirect(url_for("login"))

    # 2) Load what we already have in session
    name = session.get("user_name", "User")
    acc = session.get("user_account")
    balance = session.get("user_balance", "0")
    email = session.get("user_email", "Not Available")
    phone = session.get("user_phone", "Not Available")
    prev = session.get("user_prevTxn", "No recent transaction")
    txnType = session.get("user_txnType", "")

    # 3) Render profile page
    return render_template(
        "profile.html",
        name=name,
        acc=acc,
        email=email,
        phone=phone,
        balance=balance,
        prev=prev,
        txnType=txnType
    )


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
