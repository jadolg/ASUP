from flask import Flask, send_from_directory, request, jsonify

from downloadxml import download_files, compress_files
from files_management import get_files, save_files

app = Flask(__name__)
DOWNLOAD_PATH = '/home/akiel/Desktop/SDKUPDATE/'


@app.route('/')
def generate_and_download():
    download = download_files(DOWNLOAD_PATH)
    if download.get('errors') == 0:
        compress_files(DOWNLOAD_PATH)
        return send_from_directory(DOWNLOAD_PATH, 'update.tar.gz', as_attachment=True)
    else:
        return 'Error downloading ' + ', '.join(download.get('error_files'))


@app.route('/add', methods=['POST', ])
def add_file():
    files = get_files()
    if 'path' in request.form and request.form['path'] not in files:
        files.append(request.form['path'])
        save_files(files)
        return jsonify({'success': True, 'files': files})
    else:
        return jsonify({'success': False, 'files': files, 'msg': 'path param missing or path already in files'})


@app.route('/delete', methods=['POST', ])
def delete_file():
    files = get_files()
    if 'path' in request.form and request.form['path'] in files:
        files.remove(request.form['path'])
        save_files(files)
        return jsonify({'success': True, 'files': files})
    else:
        return jsonify({'success': False, 'files': files, 'msg': 'path param missing or path not in files'})


if __name__ == '__main__':
    app.run()
