__author__ = 'Maxim'
from flask.ext.frozen import Freezer
from flask_portal import app

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()