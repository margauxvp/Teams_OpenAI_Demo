# Importing required packages
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from functools import wraps
from flask import request, jsonify
from bs4 import BeautifulSoup
import hmac
import base64
import os
import requests
import json
import openai
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# Initializing a Flask app instance
app = Flask(__name__)

# Setting up Azure Key Vault connection
KVUri = f"https://openaibot-kv.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

# Setting API Key and API endpoint for OpenAI
openai.api_key = client.get_secret("teamsappsecret").value
openai.api_base =  "https://openaijorge2.openai.azure.com/" 
openai.api_type = 'azure'
openai.api_version = '2022-12-01' 

# Specifying deployment ID for OpenAI engine
deployment_id='teams-davinci003' 

def verify_hmac(*auth):
    def decorator_verify_hmac(f):
        @wraps(f)
        def wrapper_verify_hmac(*args, **kwargs):
            req_body = request.data
            auth_verify = hmac.new(base64.decodebytes(bytes(auth[0],'utf-8')),req_body,'sha256')
            auth_header = request.environ['HTTP_AUTHORIZATION']
            auth_string = base64.b64encode(auth_verify.digest()).decode()
            full_string = "HMAC "+ auth_string
            if auth_header != full_string:
                return jsonify({"type": "message","text": "ERROR: User unauthorized!"})
            return f(*args,**kwargs)
        return wrapper_verify_hmac
    return decorator_verify_hmac

def decorator_verify_hmac(f):
    req_body = request.data
    auth_verify = hmac.new(base64.decodebytes(bytes(auth[0],'utf-8')),req_body,'sha256')
    auth_header = request.environ['HTTP_AUTHORIZATION']
    auth_string = base64.b64encode(auth_verify.digest()).decode()
    full_string = "HMAC "+ auth_string
    if auth_header != full_string:
        return jsonify({"type": "message","text": "ERROR: User unauthorized!"})

# Defining a POST endpoint for the '/' route
@app.route('/')
def index():
   print('Request for index page received')
   return "<h1>Hello Azure!</h1>"

# Defining a POST endpoint for the '/gpt3' route
@app.route('/gpt3', methods=['POST'])
def function_name():
   # Authenticate
    security_token = b"FQHak9CmIyFiAcpr+zvzH96QzkH9gjknCNOte6buF+I="
    request_data = request.get_data()
    digest = hmac.new(base64.b64decode(security_token), msg=request_data, digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()

    # Extracting message from the POST request data
    html_message = str(request.data)
    question = html_message + ' and do not use apostrophes in your answer and write verbs fully and do use other punctuation marks'

    # Sending the message to OpenAI for completion
    response = openai.Completion.create(
            engine=deployment_id,
            prompt= question,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
        )

     # Parsing the response from OpenAI
    extract_response = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').replace("'b'", '').strip()
    
    start = extract_response.find("'")
    end = extract_response.find("'", start + 1)
    result = extract_response[start+1:end]

    # Formatting the response as a JSON object that is suitable for Teams
    message = jsonify({'type': 'message','text':result})
    
    return message

# Running the Flask app    
if __name__ == '__main__':
    app.run(debug=True)
