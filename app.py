from flask import Flask, render_template, request, redirect, session, jsonify
from sheets import (
    get_available_hours,
    add_booking,
    get_all_bookings,
    delete_booking,
    check_login
)

app = Flask(__name__)
app.secret_key = "scoala_auto_secret"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get-hours", methods=["POST"])
def get_hours():
    date = request.json["date"]
    hours = get_available_hours(date)
    return jsonify(hours)

@app.route("/book", methods=["POST"])
def book():
    nume = request.form["nume"]
    prenume = request.form["prenume"]
    telefon = request.form["telefon"]
    data = request.form["data"]
    ora = request.form["ora"]

    add_booking(
        nume,
        prenume,
        telefon,
        data,
        ora
    )

    return redirect("/")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login-post", methods=["POST"])
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    if check_login(username, password):
        session["logged"] = True
        return redirect("/dashboard")

    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged"):
        return redirect("/login")

    bookings = get_all_bookings()

    return render_template(
        "dashboard.html",
        bookings=bookings
    )

@app.route("/delete/<int:row>")
def delete(row):
    if not session.get("logged"):
        return redirect("/login")

    delete_booking(row)

    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)