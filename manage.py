__author__ = 'pavlomv'
from flask.ext.script import Manager
from flask_portal import app

manager = Manager(app)

# TEST

@manager.command
def get_quote_of_day():
    """
    Получаем цитату дня для вывода на сайте
    """
    db = None
    import requests
    import sqlite3
    request = requests.get(url='http://api.forismatic.com/api/1.0/',
                           params=dict(method='getQuote',
                                       format='json',
                                       lang='ru')).json()
    try:
        db = sqlite3.connect(app.config['DATABASE'])
        cursor = db.cursor()
        cursor.executemany('INSERT OR REPLACE INTO quote_of_day (id, quote_text, quote_author) VALUES (?, ?, ?)',
                           [(1, request.get('quoteText'), request.get('quoteAuthor'))])
        db.commit()
    finally:
        db.close()


@manager.command
def get_food_menu():
    """
    Грабим обеденное меню:D и записываем результат в базу
    """
    import sqlite3
    from grab import Grab
    from lxml import html
    from lxml.html import clean
    from lxml.html import builder as E

    db = None
    g = Grab()
    g.go('http://www.privet-bufet.ru/article/menyu-na-segodnya')
    request = g.doc.select('//div[@class="panda-article"]').html()
    doc = html.document_fromstring(request)  # Оставляем только две таблицы с меню
    cleaner = clean.Cleaner(style=True)
    doc = cleaner.clean_html(doc)
    table1 = E.TABLE(E.CLASS("table table-striped table-condensed"), doc.cssselect('tbody')[0])
    table2 = E.TABLE(E.CLASS("table table-striped table-condensed"), doc.cssselect('tbody')[0])
    html_new = html.tostring(E.DIV(table1, table2))  # Соединяем таблицы меню на сегодня и на завтра
    try:
        db = sqlite3.connect(app.config['DATABASE'])
        cursor = db.cursor()
        cursor.executemany('INSERT OR REPLACE INTO food_menu (id, html) VALUES (?, ?)',
                           [(1, html_new.decode('utf-8'))])
        db.commit()
    finally:
        db.close()



if __name__ == '__main__':
    manager.run()
