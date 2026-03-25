from __future__ import annotations

import sqlite3
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from flask import Flask, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "tracker.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-secret-key-change-me"


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_: Any) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    db = sqlite3.connect(DB_PATH)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            prompt TEXT NOT NULL,
            answer TEXT NOT NULL,
            tag TEXT NOT NULL,
            confidence INTEGER NOT NULL CHECK(confidence BETWEEN 1 AND 5),
            next_review_date TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """
    )
    db.commit()
    db.close()


def current_user_id() -> int | None:
    return session.get("user_id")


def require_auth() -> int:
    user_id = current_user_id()
    if user_id is None:
        raise PermissionError
    return user_id


def compute_next_review(confidence: int) -> str:
    spacing = {1: 1, 2: 2, 3: 4, 4: 7, 5: 14}
    return (date.today() + timedelta(days=spacing[confidence])).isoformat()


@app.route("/")
def home() -> str:
    if current_user_id() is None:
        return render_template("landing.html")
    return redirect(url_for("dashboard"))


@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if not username or not password:
            flash("Username and password are required.")
            return render_template("register.html")

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            flash("Account created. Please sign in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists.")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("dashboard"))
        flash("Invalid credentials.")
    return render_template("login.html")


@app.route("/logout")
def logout() -> Any:
    session.clear()
    return redirect(url_for("home"))


@app.route("/dashboard")
def dashboard() -> str:
    try:
        user_id = require_auth()
    except PermissionError:
        return redirect(url_for("login"))

    db = get_db()
    totals = db.execute(
        """
        SELECT COUNT(*) AS total,
               SUM(CASE WHEN date(next_review_date) <= date('now') THEN 1 ELSE 0 END) AS due,
               ROUND(AVG(confidence), 2) AS avg_confidence
        FROM cards WHERE user_id = ?
        """,
        (user_id,),
    ).fetchone()

    by_tag = db.execute(
        """
        SELECT tag, COUNT(*) AS count
        FROM cards WHERE user_id = ?
        GROUP BY tag
        ORDER BY count DESC
        """,
        (user_id,),
    ).fetchall()

    return render_template("dashboard.html", totals=totals, by_tag=by_tag)


@app.route("/cards")
def cards() -> str:
    try:
        user_id = require_auth()
    except PermissionError:
        return redirect(url_for("login"))

    tag_filter = request.args.get("tag", "").strip()
    query = "SELECT * FROM cards WHERE user_id = ?"
    params: list[Any] = [user_id]

    if tag_filter:
        query += " AND tag = ?"
        params.append(tag_filter)

    query += " ORDER BY date(next_review_date) ASC, updated_at DESC"

    db = get_db()
    all_cards = db.execute(query, params).fetchall()
    tags = db.execute("SELECT DISTINCT tag FROM cards WHERE user_id = ? ORDER BY tag", (user_id,)).fetchall()
    return render_template("cards.html", cards=all_cards, tags=tags, selected_tag=tag_filter)


@app.route("/cards/new", methods=["GET", "POST"])
def create_card() -> Any:
    try:
        user_id = require_auth()
    except PermissionError:
        return redirect(url_for("login"))

    if request.method == "POST":
        confidence = int(request.form["confidence"])
        db = get_db()
        db.execute(
            """
            INSERT INTO cards (user_id, title, prompt, answer, tag, confidence, next_review_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                request.form["title"].strip(),
                request.form["prompt"].strip(),
                request.form["answer"].strip(),
                request.form["tag"].strip().lower() or "general",
                confidence,
                compute_next_review(confidence),
            ),
        )
        db.commit()
        flash("Card created.")
        return redirect(url_for("cards"))

    return render_template("card_form.html", mode="create", card=None)


@app.route("/cards/<int:card_id>/edit", methods=["GET", "POST"])
def edit_card(card_id: int) -> Any:
    try:
        user_id = require_auth()
    except PermissionError:
        return redirect(url_for("login"))

    db = get_db()
    card = db.execute("SELECT * FROM cards WHERE id = ? AND user_id = ?", (card_id, user_id)).fetchone()
    if not card:
        flash("Card not found.")
        return redirect(url_for("cards"))

    if request.method == "POST":
        confidence = int(request.form["confidence"])
        db.execute(
            """
            UPDATE cards
            SET title = ?, prompt = ?, answer = ?, tag = ?, confidence = ?,
                next_review_date = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (
                request.form["title"].strip(),
                request.form["prompt"].strip(),
                request.form["answer"].strip(),
                request.form["tag"].strip().lower() or "general",
                confidence,
                compute_next_review(confidence),
                card_id,
                user_id,
            ),
        )
        db.commit()
        flash("Card updated.")
        return redirect(url_for("cards"))

    return render_template("card_form.html", mode="edit", card=card)


@app.route("/cards/<int:card_id>/delete", methods=["POST"])
def delete_card(card_id: int) -> Any:
    try:
        user_id = require_auth()
    except PermissionError:
        return redirect(url_for("login"))

    db = get_db()
    db.execute("DELETE FROM cards WHERE id = ? AND user_id = ?", (card_id, user_id))
    db.commit()
    flash("Card deleted.")
    return redirect(url_for("cards"))


@app.route("/review", methods=["GET", "POST"])
def review() -> Any:
    try:
        user_id = require_auth()
    except PermissionError:
        return redirect(url_for("login"))

    db = get_db()
    if request.method == "POST":
        card_id = int(request.form["card_id"])
        confidence = int(request.form["confidence"])
        db.execute(
            """
            UPDATE cards
            SET confidence = ?, next_review_date = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
            """,
            (confidence, compute_next_review(confidence), card_id, user_id),
        )
        db.commit()
        flash("Review saved.")
        return redirect(url_for("review"))

    due_cards = db.execute(
        """
        SELECT * FROM cards
        WHERE user_id = ? AND date(next_review_date) <= date('now')
        ORDER BY date(next_review_date) ASC
        """,
        (user_id,),
    ).fetchall()

    return render_template("review.html", cards=due_cards)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
