import tarfile
from os import makedirs
from os.path import dirname, abspath

import requests

from files_management import get_files

PREFIX = 'https://dl.google.com/android/repository/'
PATH = 'android/repository/'


def download_files(pwd):
    files = get_files()
    error_files = []
    for afile in files:
        print('downloading ' + afile)
        r = requests.get(PREFIX + afile, stream=True, verify=False)

        if r.status_code == 200:
            directory = dirname(abspath(pwd + PATH + afile))
            try:
                makedirs(directory)
            except OSError:
                pass

            print('writing...', end=' ')
            with open(pwd + PATH + afile, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
            print('done')
        else:
            error_files.append(afile)

    return {'errors': len(error_files), 'error_files': error_files}


def compress_files(pwd):
    tar = tarfile.open(pwd + 'update.tar.gz', 'w:gz')
    tar.add(pwd + 'android', 'android')
    tar.close()
