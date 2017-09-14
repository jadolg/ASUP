from flask import Flask, send_from_directory

from downloadxml import download_files, compress_files

app = Flask(__name__)
PWD = '/home/akiel/Desktop/SDKUPDATE/'


@app.route('/')
def hello_world():
    download_files(PWD)
    compress_files(PWD)
    return send_from_directory(PWD, 'update.tar.gz', as_attachment=True)


if __name__ == '__main__':
    app.run()
