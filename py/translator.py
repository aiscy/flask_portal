__author__ = 'pavlomv'

import requests
import requests.exceptions


def lang_support(lang):
    return {
        'sq': 'албанский',
        'en': 'английский',
        'ar': 'арабский',
        'hy': 'армянский',
        'az': 'азербайджанский',
        'be': 'белорусский',
        'bg': 'болгарский',
        'bs': 'боснийский',
        'vi': 'вьетнамский',
        'hu': 'венгерский',
        'nl': 'голландский',
        'el': 'греческий',
        'ka': 'грузинский',
        'da': 'датский',
        'he': 'иврит',
        'id': 'индонезийский',
        'it': 'итальянский',
        'is': 'исландский',
        'es': 'испанский',
        'ca': 'каталанский',
        'zh': 'китайский',
        'ko': 'корейский',
        'lv': 'латышский',
        'lt': 'литовский',
        'ms': 'малайский',
        'mt': 'мальтийский',
        'mk': 'македонский',
        'de': 'немецкий',
        'no': 'норвежский',
        'pl': 'польский',
        'pt': 'португальский',
        'ro': 'румынский',
        'ru': 'русский',
        'sr': 'сербский',
        'sk': 'словацкий',
        'sl': 'словенский',
        'th': 'тайский',
        'tr': 'турецкий',
        'uk': 'украинский',
        'fi': 'финский',
        'fr': 'французский',
        'hr': 'хорватский',
        'cs': 'чешский',
        'sv': 'шведский',
        'et': 'эстонский',
        'ja': 'японский'
    }.get(lang)


def get_lang_yandex():
    import sqlite3
    db = None
    try:
        request = requests.get('https://translate.yandex.net/api/v1.5/tr.json/getLangs?key=trnsl.1.1.20150428T093017Z.bad19a8dcde607d3.fe0f694c1c97ae0591b88a9d4fca8c07b93b8b8d&ui=ru').json().get('langs')
        db = sqlite3.connect('C:/Users/pavlomv/PycharmProjects/flask_miniportal/flask_miniportal.db')
        cursor = db.cursor()
        # cursor.executemany('INSERT INTO yandex_lang VALUES (?,?)', request.items())
        # db.commit()
        cursor.execute('SELECT quote_text, quote_author FROM quote_of_day ORDER BY quote_text')
        # cursor.execute('SELECT * FROM yandex_lang ORDER BY language_full')
        print(cursor.fetchone())
    finally:
        db.close()

def yandex_except():
    error_codes = {
        401: 'Неправильный ключ API',
        402: 'Ключ API заблокирован',
        403: 'Превышено суточное ограничение на количество запросов',
        404: 'Превышено суточное ограничение на объем переведенного текста',
        413: 'Превышен максимально допустимый размер текста',
        422: 'Текст не может быть переведен',
        501: 'Заданное направление перевода не поддерживается',
        503: 'Сервис перевода временно недоступен'}


def yandex_translate(key, text, dest_lang, source_lang, auto_lang=0):
    api_url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    if source_lang == '':  # В этом случае сервис пытается определить исходный язык автоматически.
        lang = dest_lang
        auto_lang = 1
    else:
        lang = '{src}-{dst}'.format(src=source_lang, dst=dest_lang)
    data = {
        'key': key,
        'text': text,  # TODO Для POST-запросов максимальный размер передаваемого текста составляет 10000 символов.
        'lang': lang,
        'format': 'plain',
        'options': auto_lang
        }
    translated_text = requests.post(api_url, data=data).json()
    return translated_text










if __name__ == '__main__':
    get_lang_yandex()