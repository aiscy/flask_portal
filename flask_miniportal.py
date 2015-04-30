# все импорты
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from py.translator import yandex_translate, lang_support

app = Flask(__name__)
app.config.from_pyfile('configuration.py')


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/servicedesk')
def servicedesk():
    db = get_db()
    cur = db.execute('select id, title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)



@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    if request.form['title'] == '' or request.form['text'] == '':
        flash('Введите заголовок и текст заявки')
    else:
        db = get_db()
        db.execute('insert into entries (title, text) values (?, ?)',
                    [request.form['title'], request.form['text']])
        db.commit()
        flash('Добавлена новая заявка')
    return redirect(url_for('servicedesk'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('Вы успешно авторизировались')
            return redirect(url_for('servicedesk'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('servicedesk'))


@app.route('/_translate', methods=['POST'])
def process_translate():
    print(request.form)
    translated = yandex_translate(key=app.config['TRANSLATE_YANDEX'],
                                            text=request.form['text'],
                                            dest_lang=request.form['destLang'],
                                            source_lang=request.form['sourceLang'])
    try:
        return jsonify({'text': translated['text'],
                        'auto_lang': lang_support(translated.get('detected')['lang'])
                        })
    except TypeError:
        return jsonify({'text': translated['text']})


@app.route('/translate', methods=['GET'])
def translate():
    return render_template('translate.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)