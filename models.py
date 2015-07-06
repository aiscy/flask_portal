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

class QuoteOfDay(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_text = db.Column(db.Text)
    quote_author = db.Column(db.Text)

    def __init__(self, quote_text, quote_author):
        self.quote_text = quote_text
        self.quote_author = quote_author

class YandexLang(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    language_code = db.Column(db.String(2))
    language_full = db.Column(db.Text)

    def __init__(self, language_code, language_full):
        self.language_code = language_code
        self.language_full = language_full
