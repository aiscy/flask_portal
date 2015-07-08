import sqlite3
# import flask_sijax
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify, Response
from sqlalchemy import desc
from yandex_translate import YandexTranslate
from models import FoodMenu, YandexLang, QuoteOfDay, db


app = Flask(__name__)
app.config.from_pyfile('configuration.py')
db.init_app(app)
yandex_translate = YandexTranslate(app.config['API_YANDEX_TRANSLATE_KEY'])
# app.config['SIJAX_STATIC_PATH'] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
# app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'


@app.before_request
def auth():
    if not session.get('logged_in'):
        if request.environ.get('REMOTE_USER'):
            session['user_name'] = request.environ.get('REMOTE_USER')
            session['logged_in'] = True
            flash('Вы успешно авторизировались')
        else:
            if app.debug:
                session['user_name'] = 'DebugUser'
                session['logged_in'] = True
                flash('Вы авторизировались как {}'.format(session.get('user_name')))
            else:
                abort(401)


@app.route('/')
def index():
    req = QuoteOfDay.query.get(1)
    return render_template('index.html', quote_text=req.quote_text, quote_author=req.quote_author)


@app.route('/service/food_menu/')
def food_menu():
    return render_template('food_menu.html')


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


@app.route('/service/translate/', methods=['GET'])
def translate():
    req = YandexLang.query.with_entities(YandexLang.language_code, YandexLang.language_full) \
        .order_by(YandexLang.language_full).all()
    return render_template('translate.html', yandex_lang_list=req)


# Набросок RESTful API
@app.route('/api/v1/service/foodmenu', methods=['GET'])
def food_menu_json():
    req = FoodMenu.query.get(1)
    return jsonify(dict(
        code=200,
        date=req.date,
        menu=req.menu,
        menu_complex=req.menu_complex))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
