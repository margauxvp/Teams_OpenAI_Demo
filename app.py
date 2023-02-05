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


KVUri = f"https://kv-csabot.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

openai.api_key = client.get_secret("oaik").value
openai.api_base =  "https://openai-csabot.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2022-12-01' # this may change in the future

deployment_id='gpt3davinci' #This will correspond to the custom name you chose for your deployment when you deployed a model. 


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


"""@app.route('/transcript', methods=['POST'])
def transcript():
    print("Here is the content that was received:")
    content = request.json 
    print(content)
    prompt_list = parse_transcript(content)
    map_list = list(map(call_openai, prompt_list))
    return jsonify(map_list)
def parse_transcript(text_to_parse):
    transcript = text_to_parse
    my_list_of_transcripts = split_and_combine(transcript, 10, 5)
    return map(create_prompt, my_list_of_transcripts)
def split_and_combine(list, batch_size, overlap_size):
    my_new_list = []
    list_size = len(list)
    for i in range (0,list_size,batch_size):
        number_of_elem_to_take = batch_size+overlap_size
        
        if number_of_elem_to_take > list_size-i:
            number_of_elem_to_take = list_size-i
        
        my_new_list.append(list[i:number_of_elem_to_take])
    return my_new_list
def create_prompt(list_to_prompt):
    prompt = "Summarize the following: \n"
    for each in list_to_prompt:
        prompt+=each["speaker"]+" said: "+each["text"]+"\n"
    return prompt
def call_openai(message):
    try:
        res = openai_chat_call(message)
        print("OPENAI ANSWER:")
        print(res)
        res_text =  res['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
        message = {'type': 'message','text':res_text}
    except Exception as e:
        print(e)
        message = {'type': 'message','text':'There was an error:'+str(e)}
    return message
"""

if __name__ == '__main__':
   app.run()