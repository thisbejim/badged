import sys
import os
from flask import Flask, render_template, Markup, request, redirect, url_for, jsonify
import json
import logging
import string
import random
import jwt
import time
import tweepy
import requests

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

# Setup twitter

auth = tweepy.OAuthHandler('9JTAk71PnJSxpPOWMz2vrHhWI', 'n1HPcrUAWeCNJzB2CUkc4j3HaakEEpSIhNKZTxX5QkOBp8R8Id')
auth.set_access_token('2866308042-wVjYMLidn7KVxrceOc0pqtTD0kZKxzuZ1loswtN', 'FGW5YluRrXn7l12fAwuVcUpwBMKI3C6YshIG7SxF9DlW4')
api = tweepy.API(auth)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# List all assets
@app.route('/')
def index():

    return render_template('index.html')

@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
            count = 0
            for status in tweepy.Cursor(api.user_timeline, user_id=request.form['handle']).items(400):
                print(status)
                count+=1
            print("count is HERE!")
            print(count)

            time_now = time.time()
            time_now = int(time_now)

            # Generate assertion
            assertion = {"uid": id_generator(),
                         "recipient": {"identity": request.form['email'], "type": "email", "hashed": False},
                         "badge": "https://badged.herokuapp.com/static/badges/badge.json",
                         "verify": {"url": "https://badged.herokuapp.com/static/public-key.pem", "type": "signed"},
                         "issuedOn": time_now}

            # Sign with private key
            with open('static/private-key.pem', 'r') as rsa_file:
                key = rsa_file.read()
            encoded = jwt.encode(assertion, key, algorithm='RS256',
                                 headers={'alg': 'RS256'})

            # Check a decode with public key
            with open('static/public-key.pem', 'r') as rsa_file:
                pub_key = rsa_file.read()
            decoded = jwt.decode(encoded, pub_key, algorithm=['RS256'])

            return encoded

    return render_template('check.html')



@app.route('/award/<assertion>')
def award(assertion):

    return render_template('award.html', assertion=assertion)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)