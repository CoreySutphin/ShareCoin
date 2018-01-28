from flask import Flask, request, render_template, redirect
from web3 import Web3, HTTPProvider
import requests
import oauth
import oauth2
import json
import secrets
import base64
import boto3

app = Flask(__name__)

#connection string for DynamoDB 
dynamodb = boto3.resource('dynamodb', region_name ='us-east-1')
table = dynamodb.Table('ShareBlocks')
import urllib.parse

app = Flask(__name__)

# Set up to interact with the Ropsten Ethereum test network
web3 = Web3(HTTPProvider('https://ropsten.infura.io/TUBXa5ntAP9rtqdhFQNE'))
with open('./static/contract_abi.json', 'r') as abi_definition:
    abi = json.load(abi_definition)
contract_address = '0xb021e99D2dAce09C0fd8e50234f55775Fa8F3627'
web3.eth.defaultAccount = "0xAbfD6e20bC0a7ea9b47C1310345625cc2Fd28b61"

shareCoinContract = web3.eth.contract(address=contract_address, abi=abi)

# key_secret = '{}:{}'.format(secrets.consumer_key, secrets.consumer_secret).encode('ascii')
# b64_encoded_key = base64.b64encode(key_secret)
# b64_encoded_key = b64_encoded_key.decode('ascii')

base_url = 'https://api.twitter.com/'
# auth_url = '{}oauth2/token'.format(base_url)

class access_token():

    def __int__(self, access_key):
        self.key = access_key

    def set_key(self, access_key):
        self.key = access_key

my_access = access_token();

def oauth_req():
    # key_secret = '{}:{}'.format(secrets.consumer_key, secrets.consumer_secret).encode('ascii')
    # b64_encoded_key = base64.b64encode(key_secret)
    # b64_encoded_key = b64_encoded_key.decode('ascii')
    request_token_url = base_url + 'oauth/request_token'
    access_token_url = base_url + 'oauth/access_token'


    consumer = oauth2.Consumer(secrets.consumer_key, secrets.consumer_secret)
    client = oauth2.Client(consumer)

    # auth_headers = {
    #     'Authorization' : 'Basic {}'.format(b64_encoded_key),
    #     'Content-Type' : 'application/x-www-form-urlencoded;charset=UTF-8'
    # }
    #
    # auth_data = {
    #     'grant_type' : 'client_credentials'
    # }
    resp, content = client.request(request_token_url, 'GET')

    if resp['status'] != '200':
        raise Exception("Invalid response {}".format(resp['status']))

    request_token = dict(urllib.parse.parse_qsl(content.decode('UTF-8')))
    print(request_token)
    print("Request Token:")
    print("    - oauth_token        = %s" % request_token['oauth_token'])
    print("    - oauth_token_secret = %s" % request_token['oauth_token_secret'])
    return request_token['oauth_token']

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/home')
def home():
    if my_access.key:
        return render_template('index.html', user_name='')
    else:
        return redirect('/index')


@app.route('/login')
def login():
    authorize_url = base_url + 'oauth/authenticate'
    my_access.set_key(oauth_req())
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
