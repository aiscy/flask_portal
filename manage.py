__author__ = 'pavlomv'
from flask_script import Manager
from flask_portal import app

manager = Manager(app)

# TEST

@manager.command
def get_quote_of_day():
    """Получаем цитату дня для вывода на сайте"""
    import requests
    from models import QuoteOfDay, db

    r = requests.get(url='http://api.forismatic.com/api/1.0/',
                     params=dict(method='getQuote',
                                 format='json',
                                 lang='ru')).json()
    req = QuoteOfDay.query.get(1)
    if req:
        req.quote_text, req.quote_author = r.get('quoteText'), r.get('quoteAuthor')
    else:
        db.session.add(QuoteOfDay(r.get('quoteText'), r.get('quoteAuthor')))
    db.session.commit()


@manager.command
def get_food_menu():
    """Получаем обеденное меню, созданное из doc, где текст выровнен пробелами, и приводим в нормальный вид"""
    import datetime
    import re
    from grab import Grab
    from lxml import html
    from lxml.html import clean
    from models import FoodMenu, db

    g = Grab()
    g.go('http://www.privet-bufet.ru/article/menyu-na-segodnya')
    # Если дата в таблице1==сегодняшней, то парсим таблицу2, иначе таблицу1
    date_table1 = re.search(r'\d+.\d+.\d+',
                            g.doc.select('//div[@class="panda-article"]/table[1]/tbody/tr[1]/td[1]/p').text()).group()
    if datetime.datetime.strptime(date_table1, '%d.%m.%y') == datetime.datetime.now().date():
        xpath = '//div[@class="panda-article"]/table[2]'
    else:
        xpath = '//div[@class="panda-article"]/table[1]'
    request = g.doc.select(xpath).html()
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
        if i[0] == 'Комплекс':
            for j in table[table.index(i):]:
                if j[2] != '':
                    menu_complex = dict(category=j[0], content=[], price=int(j[2].split('-')[0]), count=0)
                    continue
                menu_complex['content'].append(j[0])
            break
        if (i[1] and i[2]) == '' and i[0] != '':
            category = i[0]
            menu.append(dict(category=category, content=[]))
            continue
        elif i[0] == '':
            continue
        menu[-1]['content'].append(dict(name=i[0], weight=i[1], price=int(i[2].split('-')[0]), count=0))
    r = FoodMenu.query.get(1)
    if r:
        r.date, r.menu, r.menu_complex = date, menu, menu_complex
    else:
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
    import requests
    from models import YandexLang, db

    url = 'https://translate.yandex.net/api/v1.5/tr.json/getLangs?key={}&ui=ru' \
        .format(app.config['API_YANDEX_TRANSLATE_KEY'])
    r = requests.get(url).json().get('langs')
    for key, value in r.items():
        db.session.add(YandexLang(key, value))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
