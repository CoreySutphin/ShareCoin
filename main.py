from flask import Flask, request, render_template
from web3 import Web3, HTTPProvider
import requests
import oauth2 as oauth
import json
import secrets
import base64

app = Flask(__name__)

# Set up to interact with the Ropsten Ethereum test network
web3 = Web3(HTTPProvider('https://ropsten.infura.io/TUBXa5ntAP9rtqdhFQNE'))
with open('contract_abi.json', 'r') as abi_definition:
    abi = json.load(abi_definition)
contract_address = '0xb021e99D2dAce09C0fd8e50234f55775Fa8F3627'
web3.eth.defaultAccount = "0xAbfD6e20bC0a7ea9b47C1310345625cc2Fd28b61"

shareCoinContract = web3.eth.contract(address=contract_address, abi=abi)

key_secret = '{}:{}'.format(secrets.consumer_key, secrets.consumer_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

# ACCESS_KEY = secrets.access_token
# ACCESS_SECRET = secrets.access_token_secret

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

auth_headers = {
    'Authorization' : 'Basic {}'.format(b64_encoded_key),
    'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8'
}

auth_data = {
    'grant_type' : 'client_credentials'
}

def oauth_req():
    # consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    # access_token = oauth.Token(key=ACCESS_KEY, secret=ACCESS_SECRET)
    # client = oauth.Client(consumer, access_token)
    # timeline_endpoint = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
    # response, data = client.request(timeline_endpoint, method="GET", body=b"", headers=None)
    # print (client)
    # print(access_token.secret)
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    if auth_resp.status_code == '200':
        print(auth_resp.json().keys())
    else:
        print('Status Code: {} \n Error Code: {} Message: {} \n Key : {}'.format(auth_resp.status_code, auth_resp.json()['errors'][0]['code'], auth_resp.json()['errors'][0]['message'], b64_encoded_key))
    return

# home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', 'abcdefg', 'hijklmnop' )

@app.route('/')
def index():
    return  render_template('login.html', active="login")

@app.route('/login')
def login():
    tweets = oauth_req()
    print(tweets)
    return  render_template('login.html', active="login")
