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

app = Flask(__name__)


KVUri = f"https://openaibot-kv.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

openai.api_key = client.get_secret("teamsappsecret").value
openai.api_base =  "https://openaijorge2.openai.azure.com/" 
openai.api_type = 'azure'
openai.api_version = '2022-12-01' 

deployment_id='teams-davinci003' 


def openai_chat_call(text):  
    response = openai.Completion.create(
        engine=deployment_id,
        prompt=text,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    return response



def extract_text(attachments):
    text=""
    for item in attachments:
        if item["contentType"]=="text/html":
            text = text + item["content"]+" " 
    return text

def clean_html(html):
    # Use the BeautifulSoup library to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    # Find all of the text nodes in the HTML
    text_nodes = soup.findAll(text=True)
    # Join all of the text nodes together and return the result
    return ' '.join(text_nodes).replace("GPT3", "", 1)

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


@app.route('/')
def index():
   print('Request for index page received')
   return "<h1>Hello Azure!</h1>"

def decorator_verify_hmac(f):
    req_body = request.data
    auth_verify = hmac.new(base64.decodebytes(bytes(auth[0],'utf-8')),req_body,'sha256')
    auth_header = request.environ['HTTP_AUTHORIZATION']
    auth_string = base64.b64encode(auth_verify.digest()).decode()
    full_string = "HMAC "+ auth_string
    if auth_header != full_string:
        return jsonify({"type": "message","text": "ERROR: User unauthorized!"})

@app.route('/gpt3', methods=['POST'])
@verify_hmac('UNOR/kZ/BBugXfMZxfQshZnNToa3onK9ZWRV1TTlTa8=')
def function_name():
    content = request.json 
    html_message = extract_text(content["attachments"])
    message = clean_html(html_message)
    print("MESSAGE PROMPT:")
    print(message)
    
    try:
        res = openai_chat_call(message)
        print("OPENAI ANSWER:")
        print(res)
        res_text =  res['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
        message = jsonify({'type': 'message','text':res_text})
    except Exception as e:
        print(e)
        message = jsonify({'type': 'message','text':'There was an error:'+str(e)})
        
    return message

if __name__ == '__main__':
   app.run()
