import tarfile
from os import makedirs
from os.path import dirname, abspath

import requests

PREFIX = 'https://dl.google.com/android/repository/'
PATH = 'android/repository/'

FILES = [
    'repository2-1.xml',
    'addons_list-1.xml',
    'addons_list-2.xml',
    'addons_list-3.xml',
    'sys-img/android/sys-img2-1.xml',
    'sys-img/android-wear/sys-img2-1.xml',
    'sys-img/android-wear-cn/sys-img2-1.xml',
    'sys-img/android-tv/sys-img2-1.xml',
    'sys-img/google_apis/sys-img2-1.xml',
    'sys-img/google_apis_playstore/sys-img2-1.xml',
    'addon2-1.xml',
    'glass/addon2-1.xml',
    'extras/intel/addon2-1.xml'
]


def download_files(pwd):
    for afile in FILES:
        print('downloading ' + afile)
        try:
            r = requests.get(PREFIX + afile, stream=True, verify=False)
        except:
            pass

        while not r or r.status_code != 200:
            print('retry...')
            try:
                r = requests.get(PREFIX + afile, stream=True, verify=False)
            except:
                pass

        if r.status_code == 200:
            directory = dirname(abspath(pwd + PATH + afile))
            try:
                print('creating ' + directory)
                makedirs(directory)
                print('created directory ' + directory)
            except OSError:
                print(directory + ' was already there')

            print('writing...', end=' ')
            with open(pwd + PATH + afile, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            print('done')


def compress_files(pwd):
    tar = tarfile.open(pwd + 'update.tar.gz', 'w:gz')
    tar.add(pwd + 'android', 'android')
    tar.close()
