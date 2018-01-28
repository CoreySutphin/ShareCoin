from flask import Flask, request, render_template, redirect
from web3 import Web3, HTTPProvider
import requests
import oauth2
import json
import secrets
import base64
import urllib.parse

class access_token():
    def __int__(self, access_key, secret_key):
        self.key = access_key
        self.secret = secret_key

    def set_key(self, access_key):
        self.key = access_key

    def set_secret(self, secret_key):
        self.secret = secret_key

app = Flask(__name__)
my_access = access_token();
base_url = 'https://api.twitter.com/'

# Set up to interact with the Ropsten Ethereum test network
web3 = Web3(HTTPProvider('https://ropsten.infura.io/TUBXa5ntAP9rtqdhFQNE'))
with open('./static/contract_abi.json', 'r') as abi_definition:
    abi = json.load(abi_definition)
contract_address = '0xb021e99D2dAce09C0fd8e50234f55775Fa8F3627'
web3.eth.defaultAccount = "0xAbfD6e20bC0a7ea9b47C1310345625cc2Fd28b61"
shareCoinContract = web3.eth.contract(address=contract_address, abi=abi)

def oauth_req():
    request_token_url = base_url + 'oauth/request_token'
    access_token_url = base_url + 'oauth/access_token'
    consumer = oauth2.Consumer(secrets.consumer_key, secrets.consumer_secret)
    client = oauth2.Client(consumer)
    resp, content = client.request(request_token_url, 'GET')

    if resp['status'] != '200':
        raise Exception("Invalid response {}".format(resp['status']))

    request_token = dict(urllib.parse.parse_qsl(content.decode('UTF-8')))
    print(request_token)
    print("Request Token:")
    print("    - oauth_token        = %s" % request_token['oauth_token'])
    print("    - oauth_token_secret = %s" % request_token['oauth_token_secret'])
    my_access.set_key(request_token['oauth_token'])
    my_access.set_secret(request_token['oauth_token_secret'])
    return request_token['oauth_token']

def verify_user():
    key_secret = '{}:{}'.format(secrets.consumer_key, secrets.consumer_secret).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    auth_headers = {
        'Authorization' : 'Basic {}'.format(b64_encoded_key),
        'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type' : 'client_credentials'
    }


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def home():
    if hasattr(my_access, 'key'):
        return render_template('index.html', user_name='')
    else:
        return redirect('/')


@app.route('/login')
def login():
    oauth_req()
    authorize_url = base_url + 'oauth/authenticate'
    # print(access_token)
    return  redirect(authorize_url + '?oauth_token=' + my_access.key)

def get_tweets(user_handle):
    # search_headers = {
    #     'Authorization': 'Bearer {}'.format(TOKEN.key)
    # }
    # search_params = {
    #     'user_id' : user_handle,
    #     'exclude_replies' : False,
    # }
    search_headers = {
        'Authorization': 'Bearer {}'.format(TOKEN.key)
    }

    search_params = {
        'q': 'General Election',
        'result_type': 'recent',
        'count': 2
    }

    search_url = '{}1.1/search/tweets.json'.format(base_url)

    search_resp = requests.get(search_url, headers=search_headers, params=search_params)

    if search_resp.status_code == 200:
        print('Success search response was successful')
    else:
        print(search_resp.json())
        print('Status Code: {} \n  Message: {}'.format(search_resp.status_code, search_resp.json()['error']))
