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
    import re
    from grab import Grab
    from lxml import html
    from lxml.html import clean
    from lxml.html import builder as E

    db = None
    g = Grab()
    g.go('http://www.privet-bufet.ru/article/menyu-na-segodnya')
    request = g.doc.select('//div[@class="panda-article"]').html()
    doc = html.document_fromstring(request)
    cleaner = clean.Cleaner(style=True, remove_tags=['p', 'em'])
    # style:
    # Removes any style tags or attributes.
    # remove_tags:
    # A list of tags to remove. Only the tags will be removed, their content will get pulled up into the parent tag.
    # Оставляем только таблицу с меню на завтра
    doc = cleaner.clean_html(doc)
    html_new = html.tostring(
        E.DIV(E.TABLE(E.CLASS("table table-striped table-hover food_menu"), doc.cssselect('tbody')[-1])),
        encoding='unicode')
    try:
        db = sqlite3.connect(app.config['DATABASE'])
        cursor = db.cursor()
        cursor.executemany('INSERT OR REPLACE INTO food_menu (id, html) VALUES (?, ?)',
                           [(1, re.sub(r'\s{2,}', ' ', html_new))])
        db.commit()
    finally:
        db.close()


@manager.command
def get_picture_of_day():
    """Получаем картинку дня для фона главной страницы"""
    import requests
    import random

    data = {'username': app.config['API_PIXABAY_USERNAME'],
            'key': app.config['API_PIXABAY_KEY'],
            'q': 'пейзаж',
            'image_type': 'photo',
            'orientation': 'horizontal',
            'safesearch': 'true',
            'min_width': 1024,
            'order': 'popular',
            'per_page': 3
            }
    r = requests.get('http://pixabay.com/api/', params=data)
    list_url = []
    for item in r.json()['hits']:
        if 'birthday' not in item['tags']:
            list_url.append(item['imageURL'])
    file_image_of_day = requests.get(random.choice(list_url))
    with open(app.config['ROOT_DIR'] + r'static/img/index_bg.jpg', 'wb') as file:
        file.write(file_image_of_day.content)


@manager.command
def get_yandex_lang():
    """Получаем список доступных для перевода языков с Яндекса"""
    import sqlite3
    import requests

    db = None
    try:
        r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/getLangs?key={}&ui=ru') \
            .json().get('langs').format(app.config['API_YANDEX_TRANSLATE_KEY'])
        db = sqlite3.connect(app.config['DATABASE'])
        cursor = db.cursor()
        cursor.executemany('INSERT INTO yandex_lang VALUES (?,?)', r.items())
        db.commit()
        # cursor.execute('SELECT quote_text, quote_author FROM quote_of_day ORDER BY quote_text')
        # cursor.execute('SELECT * FROM yandex_lang ORDER BY language_full')
    finally:
        db.close()


if __name__ == '__main__':
    manager.run()
