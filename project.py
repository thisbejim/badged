import sys
import os
from flask import Flask, render_template, session, request, redirect, url_for
import logging
import string
import random
import jwt
import time
import tweepy
from flask_oauthlib.client import OAuth

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

# Twitter auth
oauth = OAuth(app)

twitter = oauth.remote_app(
    'twitter',
    consumer_key='cnZagtGnF7tdjBa0MS6LRfolp',
    consumer_secret='EDUP9tHatKeNwKUTQnlOHyscz5kBXyQWyXqkVANZFFxVYoNsx7',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
)

# Tweepy auth
auth = tweepy.OAuthHandler('cnZagtGnF7tdjBa0MS6LRfolp', 'EDUP9tHatKeNwKUTQnlOHyscz5kBXyQWyXqkVANZFFxVYoNsx7')
auth.set_access_token('3288370520-s3VODM1m5rb7onKwNfGzr0ls3DsLDIA4UCWibmj', 'zls7BCfEtf3YtoxiLAZtrFcKBnS1j5TgryEgcLWLNjwT7')
api = tweepy.API(auth)

# global
base_url = "https://badged.herokuapp.com/"
asset_url = "https://badged.herokuapp.com/static/"


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def decode_assertion(assertion):
    with open('static/public-key.pem', 'r') as rsa_file:
        pub_key = rsa_file.read()
        decoded = jwt.decode(assertion, pub_key, algorithm=['RS256'])
        return decoded


def build_assertion(email, badge_url):
    time_now = time.time()
    time_now = int(time_now)
    assertion = {"uid": id_generator(),
                 "recipient": {"identity": email.lower(), "type": "email", "hashed": False},
                 "badge": badge_url,
                 "verify": {"url": "https://badged.herokuapp.com/static/public-key.pem", "type": "signed"},
                 "issuedOn": time_now}

    # Sign with private key
    with open('static/private-key.pem', 'r') as rsa_file:
        key = rsa_file.read()
    encoded = jwt.encode(assertion, key, algorithm='RS256', headers={'alg': 'RS256'})
    # Check a decode with public key
    with open('static/public-key.pem', 'r') as rsa_file:
        pub_key = rsa_file.read()
        decoded = jwt.decode(encoded, pub_key, algorithm=['RS256'])

    return encoded.decode("utf-8")

# routes
@app.route('/')
def index():
    # initial load value
    if 'user_handle' in session:
        handle = session['user_handle']
    else:
        handle = None
    return render_template('index.html', handle=handle)


@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
            assertions = []
            count = 0
            for status in tweepy.Cursor(api.user_timeline, id=request.form['handle']).items(100):
                count += 1
                if "#securework" in status.text:
                    badge = {}
                    badge["img"] = "badges/securework/securework.png"
                    badge["assertion"] = build_assertion(request.form['email'],
                                         "https://badged.herokuapp.com/static/badges/securework/badge.json")
                    badge["tweet"] = status.text
                    assertions.append(badge)
                    try:
                        new_status = "@{0} just earned the #securework badge.".format(request.form['handle'])
                        api.update_status(status=new_status)
                    except:
                        print("Tweet failed: Either duplicate or rate limit.")
                if "#highered" in status.text:
                    badge = {}
                    badge["img"] = "badges/highered/highered.png"
                    badge["assertion"] = build_assertion(request.form['email'],
                                         "https://badged.herokuapp.com/static/badges/highered/badge.json")
                    badge["tweet"] = status.text
                    assertions.append(badge)
                    try:
                        new_status = "@{0} just earned the #highered badge.".format(request.form['handle'])
                        api.update_status(status=new_status)
                    except Exception as e:
                        print(e)
                        print("Tweet failed: Either duplicate or rate limit.")
                if "#rpl" in status.text:
                    badge = {}
                    badge["img"] = "badges/rpl/rpl.png"
                    badge["assertion"] = build_assertion(request.form['email'],
                                         "https://badged.herokuapp.com/static/badges/rpl/badge.json")
                    badge["tweet"] = status.text
                    assertions.append(badge)
                    try:
                        new_status = "@{0} just earned the #rpl badge.".format(request.form['handle'])
                        api.update_status(status=new_status)
                    except:
                        print("Tweet failed: Either duplicate or rate limit.")
                if "#lifelonglearning" in status.text:
                    badge = {}
                    badge["img"] = "badges/lifelonglearning/lifelonglearning.png"
                    badge["assertion"] = build_assertion(request.form['email'],
                                         "https://badged.herokuapp.com/static/badges/lifelonglearning/badge.json")
                    badge["tweet"] = status.text
                    assertions.append(badge)
                    try:
                        new_status = "@{0} just earned the #lifelonglearning badge.".format(request.form['handle'])
                        api.update_status(status=new_status)
                    except:
                        print("Tweet failed: Either duplicate or rate limit.")
                if "#auspol" in status.text:
                    badge = {}
                    badge["img"] = "badges/auspol/auspol.png"
                    badge["assertion"] = build_assertion(request.form['email'],
                                         "https://badged.herokuapp.com/static/badges/auspol/badge.json")
                    badge["tweet"] = status.text
                    assertions.append(badge)
                    try:
                        new_status = "@{0} just earned the #auspol badge.".format(request.form['handle'])
                        api.update_status(status=new_status)
                    except:
                        print("Tweet failed: Either duplicate or rate limit.")
            print(count)
            session['assertions'] = assertions
            return "200"

    return render_template('check.html')

@app.route('/error/')
def error():
    return render_template('error.html')

@app.route('/award/')
def award():
    assertions = session['assertions']
    return render_template('award.html', assertions=assertions)

@app.route('/twitter')
def twitter_auth():
    callback_url = url_for('authorized')
    return twitter.authorize(callback=callback_url)

@twitter.tokengetter
def get_twitter_token():
    if 'twitter_oauth' in session:
        resp = session['twitter_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']

@app.route('/authorized')
def authorized():
    resp = twitter.authorized_response()

    if resp is None:
        return redirect(url_for('error'))

    session['user_handle'] = resp['screen_name']

    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_handle', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)