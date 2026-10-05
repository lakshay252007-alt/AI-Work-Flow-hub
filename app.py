from flask import Flask, render_template, send_from_directory, request
import sqlite3
from werkzeug.security import generate_password_hash
def init_db():
    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
app = Flask(
    __name__,
    template_folder="Frontend",
static_folder="Frontend/FrontenndCss",
    static_url_path="/FrontenndCss"
)


@app.route("/", methods=["GET", "POST"])
def home():

    search_query = ""

    if request.method == "POST":
        search_query = request.form.get("search")

        print("User searched:", search_query)

    return render_template("index.html", search_query=search_query)
@app.route("/search", methods=["POST"])
def search():

    search_query = request.form.get("search")

    return render_template(
        "search_results.html",
        search_query=search_query
    )


@app.route("/login")
def login():
    return render_template("Login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        if password != confirm_password:
            return "Passwords do not match"

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            conn.close()
            return "Email already registered"

        conn.close()

        return "Account created successfully!"

    return render_template("signup.html")
@app.route("/video/<path:filename>")
def video(filename):
    return send_from_directory("Frontend", filename)
if __name__ == "__main__":
    init_db()
    app.run(debug=True)