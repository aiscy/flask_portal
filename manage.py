__author__ = 'pavlomv'
from flask_script import Manager
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
    from grab import Grab
    from lxml import html
    from lxml.html import clean
    from models import FoodMenu, db
    import json

    g = Grab()
    g.go('http://www.privet-bufet.ru/article/menyu-na-segodnya')
    request = g.doc.select('//div[@class="panda-article"]/table[2]').html()
    doc = html.document_fromstring(request)

    cleaner = clean.Cleaner(style=True, remove_tags=['p', 'em'])
    doc = cleaner.clean_html(doc)
    table = []
    for row in doc.cssselect("tr"):
        tds = row.cssselect("td")
        table.append([tds[0].text_content(), tds[1].text_content(), tds[2].text_content()])
    for i in table:
        for j in i:
            k = i.index(j)
            i.remove(j)
            i.insert(k, ' '.join(j.split()))

    date = table.pop(0)[0]
    menu = []
    menu_complex = []
    for i in table:
        # print(i[0])
        if i[0] == 'Комплекс':
            for j in table[table.index(i):]:
                if j[2] != '':
                    # menu_complex_price = j[2].split('-')[0]
                    menu_complex = dict(category=j[0], content=[], price=j[2].split('-')[0])
                    continue
                menu_complex['content'].append(j[0])
            break
        if (i[1] and i[2]) == '' and i[0] != '':
            category = i[0]
            menu.append(dict(category=category, content=[]))
            continue
        elif i[0] == '':
            continue
        menu[-1]['content'].append({'name': i[0], 'weight': i[1], 'price': i[2].split('-')[0]})

    db.session.add(FoodMenu(date, menu, menu_complex))
    db.session.commit()


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
