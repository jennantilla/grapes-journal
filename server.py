from flask import Flask, redirect, request, render_template, session, flash, jsonify, request_finished
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

import requests
import json
from datetime import timedelta, date, datetime

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

    return redirect(f"/kits/{user.user_id}")


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
def show_kits(user_id):
    """Displays today's journal"""

    user_id = session.get("user_id")
    user = User.query.filter_by(user_id=user_id).first()

    return render_template("today.html",
                                user_id=user_id,
                                user=user)


@app.route("/entry", methods=["POST"])
def add_entry():
    """Adds an entry to the db"""
    user_id = session.get("user_id")
    grateful = request.form.get("grateful")
    resolution = request.form.get("resolutions")
    affirmation = request.form.get("affirmation")
    proud = request.form.get("proud")
    excited = request.form.get("excited")
    schedule = request.form.get("schedule")

    new_entry = Entry(user_id=user_id, grateful=grateful, resolution=resolution, affirmation=affirmation, proud=proud, excited=excited, schedule=schedule)

    db.session.add(new_entry)
    db.session.commit()

    flash(f"journal completed")

    return redirect(f"/journal/{user_id}")


@app.route("/journal/<int:user_id>")
def show_entire_journal(user_id):
    """Displays all journal entries"""

    user_id = session.get("user_id")
    user = User.query.filter_by(user_id=user_id).first()
    
    # get all entries belonging to a specific to user 
    entries = Entry.query.filter_by(user_id=user_id).all()

    return render_template("journal.html",
                            user=user,
                            entries=entries)



# @app.route("/edit-item", methods=["POST"])
# def edit_item():
#     """Edits an existing goal in the db"""
#     user_id = session.get("user_id")
#     kit_id = request.form.get("kit-id")
#     item_id = request.form.get("item-id")
#     description = request.form.get("description")
#     category = request.form.get("category")
#     quantity = request.form.get("quantity")
#     expiration = request.form.get("expiration")

#     kit_item = (Supply_Item.query.filter_by(item_id=item_id).first())

#     kit_item.item_description = description
#     kit_item.category = category
#     kit_item.expiration_date = expiration
#     kit_item.quantity = quantity
#     db.session.commit()

#     flash(f"{description} updated")

#     return redirect(f"/supplies/{user_id}")


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
