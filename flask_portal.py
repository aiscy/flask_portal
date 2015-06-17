# все импорты
import sqlite3
import os
import flask_sijax
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash, jsonify
from yandex_translate import YandexTranslate
# from py.sqlite_conn import connect_db

app = Flask(__name__)
app.config.from_pyfile('configuration.py')
yandex_translate = YandexTranslate(app.config['API_YANDEX_TRANSLATE_KEY'])
# app.config['SIJAX_STATIC_PATH'] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
# app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    app.logger.debug('Connected to db.')
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# @app.before_request
# def auth():
#     if not session.get('logged_in'):
#         if request.environ.get('REMOTE_USER'):
#             session['logged_in'] = True
#             flash('Вы успешно авторизировались')
#         else:
#             abort(401)


@app.route('/')
def index():
    db = get_db()
    cur = list(db.execute('SELECT quote_text, quote_author FROM quote_of_day').fetchone())
    # app.logger.debug(cur[0], cur[1])
    return render_template('index.html', quote_text=cur[0], quote_author=cur[1])


@app.route('/service/food_menu')
def food_menu():
    db = get_db()
    html = list(db.execute('SELECT html FROM food_menu').fetchone())
    app.logger.debug(html)
    return render_template('food_menu.html', menu=html[0])



@app.route('/service/_translate', methods=['POST'])
def process_translate():
    """Функция для перевода текста, соединение происходит через ajax"""
    lang = None
    text = request.form['text']
    dest_lang = request.form['destLang']
    source_lang = request.form['sourceLang']
    if source_lang and dest_lang:
        lang = '{src}-{dst}'.format(src=source_lang, dst=dest_lang)
        translated = yandex_translate.translate(text, lang)
        return jsonify({'text': translated.get('text')})
    else:  # если задан только конечный язык, яндекс попытается определить исходный
        lang = dest_lang
        translated = yandex_translate.translate(text, lang)
        return jsonify({'text': translated.get('text'),
                        'auto_lang': translated.get('lang').lower().split('-')[0]})


@app.route('/service/translate', methods=['GET'])
def translate():
    db = get_db()
    yandex_lang_list = list(db.execute('SELECT * FROM yandex_lang ORDER BY language_full'))
    return render_template('translate.html', yandex_lang_list=yandex_lang_list)


app.route('/service/visio')
def service_visio():
    return 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
