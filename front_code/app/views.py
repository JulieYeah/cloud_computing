from flask import (
    Flask,
    request,
    render_template,
    send_from_directory,
    url_for,
    jsonify
)
from werkzeug import secure_filename
import os
import subprocess

basedir = os.path.abspath(os.path.dirname(__file__))

from app import app
from logging import Formatter, FileHandler
handler = FileHandler(os.path.join(basedir, 'log.txt'), encoding='utf8')
handler.setFormatter(
    Formatter("[%(asctime)s] %(levelname)-8s %(message)s", "%Y-%m-%d %H:%M:%S")
)
app.logger.addHandler(handler)


app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'js_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/js', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    elif endpoint == 'css_static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     'static/css', filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/css/<path:filename>')
def css_static(filename):
    return send_from_directory(app.root_path + '/static/css/', filename)


@app.route('/js/<path:filename>')
def js_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files['file']
        if files:
            path = url_for('static', filename='img/input.jpg')
            files.save('app/static/img/input.jpg')
            output = subprocess.call("python input.py", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
         #   hdfs = subprocess.call("hdfs dfs -copyFromLocal test.txt /test_vector.txt -f", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            return jsonify(result=path)
