__author__ = 'pavlomv'
from flask.ext.script import Manager
from flask_miniportal import app

manager = Manager(app)

@manager.command
def get_quote_of_day():
    db = None
    import requests
    import sqlite3
    request = requests.get(url='http://api.forismatic.com/api/1.0/',
                           params=dict(method='getQuote',
                                       format='json',
                                       lang='ru')).json()
    try:
        db = sqlite3.connect('C:/Users/pavlomv/PycharmProjects/flask_miniportal/flask_miniportal.db')
        cursor = db.cursor()
        cursor.executemany('INSERT OR REPLACE INTO quote_of_day (id, quote_text, quote_author) VALUES (?, ?, ?)',
                           [(1, request.get('quoteText'), request.get('quoteAuthor'))])
        db.commit()
    finally:
        db.close()


if __name__ == '__main__':
    manager.run()
