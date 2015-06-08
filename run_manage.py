__author__ = 'pavlomv'
# Скрипт для flask-script
import os


def main():
    os.system(r'\\testkomp\python34$\python.exe ' +
              os.path.join(os.path.dirname(os.path.realpath(__file__)),
                           'manage.py ') + input('Input the command\n'))


if __name__ == '__main__':
    main()