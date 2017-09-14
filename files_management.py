import os

import sys

APP_ROUTE = os.path.dirname(sys.argv[0]) + os.path.sep


def get_files():
    return [file for file in open(APP_ROUTE + 'files', 'r').read().split('\n') if file != '']


def save_files(files):
    f = open(APP_ROUTE + 'files', 'w')
    for line in files:
        if line != '':
            f.write(line.strip() + '\n')
    f.close()
