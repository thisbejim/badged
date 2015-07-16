import sys
import os
from flask import Flask, render_template, Markup, request, redirect, url_for, jsonify
import json
import logging
import string
import random
import jwt
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


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# List all assets
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/award', methods=['GET', 'POST'])
def award():
    if request.method == 'POST':
            time_now = time.time()
            time_now = int(time_now)

            assertion = {"uid": id_generator(),
                         "recipient": {"identity":request.form['email'],"type":"email", "hashed": False},
                         "badge": "https://badged.herokuapp.com/static/badges/badge.json",
                         "verify": {"url": "https://badged.herokuapp.com/static/public-key.pem", "type": "signed"},
                         "issuedOn": time_now}

            with open('static/private-key.pem', 'r') as rsa_file:
                priv_key = rsa_file.read()
            encoded = jwt.encode(assertion, priv_key, algorithm='RS256',
                                 headers={'alg': 'RS256'})

            print(encoded)
            with open('static/public-key.pem', 'r') as rsa_file:
                priv_key = rsa_file.read()
            decoded = jwt.decode(encoded, priv_key, algorithm=['RS256'])
            print(decoded)
            return redirect(url_for('index'))

    # get new articles
    return render_template('check.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)