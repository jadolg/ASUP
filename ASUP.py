from flask import Flask, send_from_directory, request, jsonify
from flask.templating import render_template

from downloadxml import download_files, compress_files
from files_management import get_files, save_files, APP_ROUTE

app = Flask(__name__)
DOWNLOAD_PATH = APP_ROUTE + 'sdk_update/'


@app.route('/')
def generate_and_download():
    download = download_files(DOWNLOAD_PATH)
    if download.get('errors') == 0:
        compress_files(DOWNLOAD_PATH)
        return send_from_directory(DOWNLOAD_PATH, 'update.tar.gz', as_attachment=True)
    else:
        return jsonify(
            {'success': False, 'error_files': download.get('error_files'), 'msg': 'Failed to download files'})


@app.route('/add', methods=['POST', ])
def add_file():
    files = get_files()
    if 'path' in request.form and request.form['path'] not in files:
        files.append(str(request.form['path']).replace('/android/repository/', '', 1))
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


@app.route('/list', methods=['GET', ])
def list_files():
    return jsonify({'success': True, 'files': get_files()})


@app.route('/help', methods=['GET', ])
def get_help():
    return render_template('help.html')


if __name__ == '__main__':
    app.run()
