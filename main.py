from flask import Flask, request, render_template, redirect, url_for, session, g, flash
from flask_social import Social
from flask_oauth import OAuth
import secrets.py import *


app = Flask(__name__)
DEBUG = True
app.debug = DEBUG
app.secret_key = access_token_secret

oauth = OAuth()

twitter = oauth.remote_app('twitter',
                    base_url='https://api.twitter.com/1/',
                    request_token_url='https://api.twitter.com/oauth/request_token',
                    access_token_url='https://api.twitter.com/oauth/access_token',
                    authorize_url='https://api.twitter.com/oauth/authenticate',
                    consumer_key = "D1Z6wJrdWHjlEOBb3r3Cmdqer",
                    consumer_secret = " YgiPCKIRbdhKvQ3JtzzXGj0W4MaprBnhWaNoneWZ0bSmUzgFHk"
                     )

# app.config['SOCIAL_TWITTER'] = {
#     'consuer_key' : ,
#     'consumer_secret' : "YgiPCKIRbdhKvQ3JtzzXGj0W4MaprBnhWaNoneWZ0bSmUzgFHk"
# }

@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')
app.config['SECURITY_POST_LOGIN'] = '/profile'

@app.route('/')
def index():
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))
    access_token = access_token[0]
    return  render_template('index.html', active="index")

@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized', next=request.args.get('next') or request.referrer or None))

@app.route('/logout')
def logout():
    session.pop('screen_name', None)
    flash('You were signed out')
    return redirect(request.referrer or url_for('index'))

@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'you denied the request to sign in.')
        return redirect(next_url)

    access_token = resp['oauth_token']
    session['access_token'] = access_token
    session['screen_name'] = resp['screen_name']

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    return redirec(url_for('index'))

if __name__ == '__main__':
    app.run()
