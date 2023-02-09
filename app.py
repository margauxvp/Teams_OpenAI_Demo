# Importing required packages
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask import request, jsonify
from bs4 import BeautifulSoup
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

# Defining a POST endpoint for the '/' route
@app.route('/')
def index():
   print('Request for index page received')
   return "<h1>Hello Azure!</h1>"

# Defining a POST endpoint for the '/gpt3' route
@app.route('/gpt3', methods=['POST'])
def function_name():
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
