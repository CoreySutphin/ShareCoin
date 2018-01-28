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
with open('./static/contract_abi.json', 'r') as abi_definition:
    abi = json.load(abi_definition)
contract_address = '0xb021e99D2dAce09C0fd8e50234f55775Fa8F3627'
web3.eth.defaultAccount = "0xAbfD6e20bC0a7ea9b47C1310345625cc2Fd28b61"

shareCoinContract = web3.eth.contract(address=contract_address, abi=abi)

key_secret = '{}:{}'.format(secrets.consumer_key, secrets.consumer_secret).encode('ascii')
b64_encoded_key = base64.b64encode(key_secret)
b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
auth_url = '{}oauth2/token'.format(base_url)

class access_token():

    def __int__(self, access_key):
        self.key = access_key

    def set_key(self, access_key):
        self.key = access_key

TOKEN = access_token();

def oauth_req():
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
    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    if auth_resp.status_code == 200:
        print('Success token received')
        return auth_resp.json()['access_token']
    else:
        print('Token was not received')
        print('Status Code: {} \n Error Code: {} Message: {} \n Key : {}'.format(auth_resp.status_code, auth_resp.json()['errors'][0]['code'], auth_resp.json()['errors'][0]['message'], b64_encoded_key))
    return

@app.route('/')
def index():
    return  render_template('index.html', active="login")

@app.route('/login')
def login():
    TOKEN.set_key(oauth_req())
    # print(access_token)
    get_tweets('What3v3rTrevor')
    return  render_template('login.html', active="login.html")

@app.route('/home_page')
def home_page():
    return render_template('bounty.html')

@app.route('/bounty', methods=["POST"])
def bounty:
    return render_template("home_page.html")


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
        print(search_resp.json())
    else:
        print(search_resp.json())
        print('Status Code: {} \n  Message: {}'.format(search_resp.status_code, search_resp.json()['error']))
