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
from glob import glob
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
            hdfs = subprocess.call("hdfs dfs -copyFromLocal -f /var/www/html/cloud_computing/front_code/test.txt /test_vector.txt", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            hdfs = subprocess.call("/opt/spark-2.1.0-bin-hadoop2.6/bin/spark-submit --master local /home/hduser/toLibSVM.py", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            hdfs = subprocess.call("/opt/spark-2.1.0-bin-hadoop2.6/bin/spark-submit --master local /home/hduser/LogisRegT.py", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            hdfs = subprocess.call("hdfs dfs -copyToLocal /predictionT/part-00000 /home/hduser", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            label = subprocess.Popen(["cat", "/home/hduser/part-00000"], stdout=subprocess.PIPE).stdout.read()
            labelnum = int(label.decode("utf-8").split('.')[0])
            name = subprocess.Popen(["grep","-E","^%s"%labelnum, "pic.log"], stdout=subprocess.PIPE).stdout.read()
            fullname = name.decode("utf-8").split(' ')[1:3]
            fullname = ' '.join(fullname)
            folder = "app/static/thumbnails_features_deduped_publish/" + fullname
            import random
            path = url_for('static',filename=random.choice(glob(folder +"/*"))[11:])
            label = folder.split('/')[-1]
            hdfs = subprocess.call("hdfs dfs -rm -r /predictionT", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            hdfs = subprocess.call("hdfs dfs -rm /test_vector.txt", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            hdfs = subprocess.call("rm -rf /home/hduser/part-00000", shell=True, stdout=subprocess.PIPE, universal_newlines=True)
            return jsonify(path=path, label=label)
