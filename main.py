# все импорты
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# конфигурация
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# создаём наше маленькое приложение :)
app = Flask(__name__)
app.config.from_object(__name__)

# Загружаем конфиг по умолчанию и переопределяем в конфигурации часть
# значений через переменную окружения
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Соединяет с указанной базой данных."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

if __name__ == '__main__':
    app.run()