__author__ = 'pavlomv'
# Скрипт для локального запуска портала с использованием интерпретатора с ПК testkomp
import os


def main():
    os.system(r'\\testkomp\python34$\python.exe ' +
              os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'flask_portal.py'))


if __name__ == '__main__':
    main()