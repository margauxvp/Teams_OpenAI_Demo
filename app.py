from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask import request, jsonify
from bs4 import BeautifulSoup
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
    return ' '.join(text_nodes).replace("teamsbot", "", 1)



@app.route('/')
def index():
   print('Request for index page received')
   return "<h1>Hello Azure!</h1>"



@app.route('/gpt3', methods=['POST'])
def function_name():
    html_message = str(request.data)
    question = html_message + ' and do not use apostrophes in your answer and write verbs fully and do use other punctuation marks'

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

    extract_response = response['choices'][0]['text'].replace('\n', '').replace(' .', '.').replace("'b'", '').strip()
    
    start = extract_response.find("'")
    end = extract_response.find("'", start + 1)

    result = extract_response[start+1:end]
    #res_text =  response['choices'][0]['text'].replace('\n', '').replace(' .', '.').strip()
    message = jsonify({'type': 'message','text':result})
    
    return message
    
if __name__ == '__main__':
    app.run(debug=True)