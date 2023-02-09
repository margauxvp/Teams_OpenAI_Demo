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

@app.route('/')
def index():
   print('Request for index page received')
   return "<h1>Hello Azure!</h1>"

# Running the Flask app    
if __name__ == '__main__':
    app.run(debug=True)
