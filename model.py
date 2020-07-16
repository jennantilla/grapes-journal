from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of app"""

    __tablename__= "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(50), nullable=False)


class Entry(db.Model):
    """User's prep kits"""

    __tablename__ = "user_entries"

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), index=True)
    date = db.Column(db.DateTime, default=datetime.now)
    mood = db.Column(db.String(100))
    grateful = db.Column(db.String(1000))
    resolution = db.Column(db.String(1000))
    affirmation = db.Column(db.String(1000))
    proud = db.Column(db.String(1000))
    excited = db.Column(db.String(1000))
    simplify = db.Column(db.String(1000))

    # Define relationship to User
    user = db.relationship("User", backref=db.backref("user_entries"))


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///grapes"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    print("Connected to DB.")


