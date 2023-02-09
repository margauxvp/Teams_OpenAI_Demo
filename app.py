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

@app.route('/')
def index():
   print('Request for index page received')
   return "<h1>Hello Azure!</h1>"

# Running the Flask app    
if __name__ == '__main__':
    app.run(debug=True)
