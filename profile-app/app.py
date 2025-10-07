from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
cursor = db.cursor()

# Create database if not exists
cursor.execute("CREATE DATABASE IF NOT EXISTS codenera")
cursor.execute("USE codenera")

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users_profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
)
""")
db.commit()
cursor.close()

# Reconnect with dictionary cursor
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="codenera"
)
cursor = db.cursor(dictionary=True)

# -----------------------------
# ROUTES (same as before)
# -----------------------------
@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("profile", user_id=session["user_id"]))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        try:
            cursor.execute(
                "INSERT INTO users_profile (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            db.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except mysql.connector.Error as err:
            print("Database Error:", err)
            flash("User already exists or an error occurred!", "danger")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users_profile WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful!", "success")
            return redirect(url_for("profile", user_id=user["id"]))
        else:
            flash("Invalid credentials, please try again.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))

@app.route("/profile/<int:user_id>")
def profile(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for("login"))

    cursor.execute("SELECT username, email FROM users_profile WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    return render_template("profile.html", user=user)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
