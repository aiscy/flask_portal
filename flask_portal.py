# все импорты
import sqlite3
import os
import flask_sijax
from flask import Flask, request, session, g, redirect, url_for, \
                  abort, render_template, flash, jsonify
from py.translator import yandex_translate, lang_support

app = Flask(__name__)
app.config.from_pyfile('configuration.py')
app.config['SIJAX_STATIC_PATH'] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
# app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'


# class login_required(object):
#     def __init__(self, view):
#         self.view = view
#         self.__name__ = view.__name__
#
#     def __call__(self, *args, **kwargs):
#         if not self.is_authenticated():
#             return redirect(url_for('login') + '?next=' + request.path)
#         return self.view(*args, **kwargs)
#
#     def is_authenticated(self):
#         if request.environ.get('REMOTE_USER', None):
#             return True
#         return False


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


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


@app.before_request
def auth():
    if not session.get('logged_in'):
        if request.environ.get('REMOTE_USER'):
            session['logged_in'] = True
            flash('Вы успешно авторизировались')
        else:
            abort(401)


@app.route('/')
def index():
    db = get_db()
    cur = list(db.execute('SELECT quote_text, quote_author FROM quote_of_day').fetchone())
    # app.logger.debug(cur[0], cur[1])
    return render_template('index.html', quote_text=cur[0], quote_author=cur[1])


@app.route('/food_menu')
def food_menu():
    db = get_db()
    html = list(db.execute('SELECT html FROM food_menu').fetchone())
    app.logger.debug(html)
    return render_template('food_menu.html', menu=html[0])


# @app.route('/add', methods=['POST'])
# def add_entry():
#     # if not session.get('logged_in'):
#     #     abort(401)
#     if request.form['title'] == '' or request.form['text'] == '':
#         flash('Введите заголовок и текст заявки')
#     else:
#         db = get_db()
#         db.execute('insert into entries (title, text) values (?, ?)',
#                     [request.form['title'], request.form['text']])
#         db.commit()
#         flash('Добавлена новая заявка')
#
#     return redirect(url_for('servicedesk'))


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     print(request.environ.items())
#     if request.method == 'POST':
#         if request.form['username'] != app.config['USERNAME']:
#             error = 'Invalid username'
#         elif request.form['password'] != app.config['PASSWORD']:
#             error = 'Invalid password'
#         else:
#             session['logged_in'] = True
#             flash('Вы успешно авторизировались')
#             return redirect(url_for('servicedesk'))
#     return render_template('login.html', error=error)
#
#
# @app.route('/logout')
# def logout():
#     session.pop('logged_in', None)
#     flash('You were logged out')
#     return redirect(url_for('servicedesk'))


@app.route('/_translate', methods=['POST'])
def process_translate():
    # app.debug(request.form)
    translated = yandex_translate(key=app.config['TRANSLATE_YANDEX'],
                                  text=request.form['text'],
                                  dest_lang=request.form['destLang'],
                                  source_lang=request.form['sourceLang'])
    try:  # TODO временное решение :)
        return jsonify({'text': translated['text'],
                        'auto_lang': lang_support(translated.get('detected')['lang'])
                        })
    except TypeError:
        return jsonify({'text': translated['text']})


@app.route('/translate', methods=['GET'])
def translate():
    db = get_db()
    yandex_lang_list = list(db.execute('SELECT * FROM yandex_lang ORDER BY language_full'))
    return render_template('translate.html', yandex_lang_list=yandex_lang_list)


app.route('/service_visio')
def service_visio():
    return 1


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
