__author__ = 'pavlomv'
# from flask_portal import app
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class FoodMenu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.PickleType)
    menu = db.Column(db.PickleType)
    menu_complex = db.Column(db.PickleType)

    def __init__(self, date, menu, menu_complex):
        self.date = date
        self.menu = menu
        self.menu_complex = menu_complex
