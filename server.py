from flask import Flask, redirect, request, render_template, session, flash, jsonify, request_finished
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from datetime import timedelta, date, datetime

import requests
import json

from model import connect_to_db, db, User, Entry

app = Flask(__name__)
app.jinja_env.undefined = StrictUndefined
app.jinja_env.auto_reload = True

app.secret_key = "ABC"

@app.route("/")
def show_homepage():
    """Displays homepage"""

    return render_template("home.html")

@app.route("/login", methods=["POST"])
def log_in():
    """Logs in an existing user"""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("We couldn't find you in our records!")
        return redirect("/")

    if user.password != password:
        flash("Your password is incorrect. Please try again")
        return redirect("/")

    session["user_id"] = user.user_id

    return redirect(f"/today/{user.user_id}")


@app.route("/register", methods=["POST"])
def add_user():
    """Handles intake questions for new user"""

    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]

    user = User(name=name, email=email, password=password)


    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.user_id

    return redirect(f"/today/{user.user_id}")


@app.route("/today/<int:user_id>")
def show_today(user_id):
    """Displays today's journal"""

    user_id = session.get("user_id")
    user = User.query.filter_by(user_id=user_id).first()

    today = datetime.today()

    return render_template("today.html",
                                user_id=user_id,
                                user=user, 
                                today=today,)


@app.route("/entry", methods=["POST"])
def add_entry():
    """Adds an entry to the db"""

    user_id = session.get("user_id")
    mood = request.form.get("mood")
    grateful = request.form.get("grateful")
    resolution = request.form.get("resolutions")
    affirmation = request.form.get("affirmation")
    proud = request.form.get("proud")
    excited = request.form.get("excited")
    self_care = request.form.get("self-care")
    jam = request.form.get("jam")
    whine = request.form.get("whine")

    new_entry = Entry(user_id=user_id, mood=mood, grateful=grateful, resolution=resolution, affirmation=affirmation, proud=proud, excited=excited, self_care=self_care, jam=jam, whine=whine)

    user = (User.query.filter_by(user_id=user_id).first())

    user.streak +=1

    db.session.add(new_entry)
    db.session.commit()

    flash(f"Today's entry was added to your journal!")

    return redirect(f"/journal/{user_id}")

@app.route("/edit_entry", methods=["POST"])
def edit_entry():
    """Edit an existing entry and commit to db"""

    user_id = session.get("user_id")
    entry_id = request.form.get("entry-id")
    mood = request.form.get("mood")
    grateful = request.form.get("grateful")
    resolution = request.form.get("resolution")
    affirmation = request.form.get("affirmation")
    proud = request.form.get("proud")
    excited = request.form.get("excited")
    self_care = request.form.get("self-care")
    jam = request.form.get("jam")
    whine = request.form.get("whine")

    entry = (Entry.query.filter_by(entry_id=entry_id).first())

    entry.mood = mood
    entry.grateful = grateful
    entry.resolution = resolution
    entry.affirmation = affirmation
    entry.proud = proud
    entry.excited = excited
    entry.self_care = self_care
    entry.jam = jam
    entry.whine = whine 

    db.session.commit()

    flash(f"Entry was updated!")    

    return redirect(f"/journal/{user_id}")

@app.route("/change-avatar", methods=["POST"])
def change_avatar():
    """Updates the user's avatar on profile"""

    user_id = session.get("user_id")
    update = request.form.get("avatar")

    user = (User.query.filter_by(user_id=user_id).first())

    user.avatar = update

    db.session.commit()

    flash(f"Avatar saved!")    

    return redirect(f"/journal/{user_id}")


@app.route("/journal/<int:user_id>")
def show_entire_journal(user_id):
    """Displays all journal entries"""

    user_id = session.get("user_id")
    user = User.query.filter_by(user_id=user_id).first()

    
    response = requests.get("https://www.affirmations.dev/")
    affirmation=response.json()["affirmation"]


    entries = Entry.query.filter_by(user_id=user_id).all()
    entry_count = len(entries)

    def find_mood_stats(entries):
        """Displays count of moods reported in past entries"""
        mood_counts = {"unripe": 0, "sweet": 0, "sour": 0, "rotten": 0}

        for entry in entries:
            if entry.mood == "unripe":
                mood_counts["unripe"] += 1
            if entry.mood == "sweet":
                mood_counts["sweet"] += 1
            if entry.mood == "sour":
                mood_counts["sour"] += 1
            if entry.mood == "rotten":
                mood_counts["rotten"] += 1

        return mood_counts

    moods = find_mood_stats(entries)
    most_frequent_mood = max(moods, key=moods.get)

    return render_template("journal.html",
                            user=user,
                            entries=entries,
                            entry_count=entry_count,
                            moods=moods,
                            affirmation=affirmation)


@app.route("/logout")
def logout():
    """Logs out current user"""

    del session["user_id"]
    flash("Logged out")

    return redirect("/")


if __name__ == "__main__":
    app.debug = False

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    connect_to_db(app)

    app.run(host="0.0.0.0")
