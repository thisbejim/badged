import sys
import os
from flask import Flask, render_template, Markup, request, redirect, url_for
from geopy.geocoders import Nominatim
import logging
import pyrebase
import time

# App Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'static/uploads/'


# Set allowable MIME Types for upload
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
app.config['SITE'] = "http://0.0.0.0:5000/"
app.config['DEBUG'] = True


# List all assets
@app.route('/')
def index():

    # get new articles
    return render_template('index.html')

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
            print(request.form['email'])
            print(request.form['handle'])
            return redirect(url_for('index'))

    # get new articles
    return render_template('check.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)