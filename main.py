from flask import Flask, request, render_template
import oauth2
import secrets


app = Flask(__name__)
def oauth_req(url, key, secret, http_method="GET", post_body='', http_headers=None):
    consumer = oauth2.Consumer(key=secrets.consumer_key, secret=secrets.consumer_secret)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

# home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', 'abcdefg', 'hijklmnop' )

@app.route('/')
def index():
    return  render_template('index.html', active="index")
