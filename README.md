# Teams_OpenAI_Demo

## Flask OpenAI App
This is a Flask application that makes use of OpenAI API to generate text based on a given prompt.

## Prerequisites
Flask
OpenAI API Key
BeautifulSoup
Requests
JSON
Azure KeyVault
Azure Identity

## API Key
The API key is stored in the Azure KeyVault, and the SecretClient is used to access the API key.

## OpenAI API
This app uses the OpenAI API to generate text based on the prompt. The deployment ID teams-davinci003 is used to specify which OpenAI deployment to use.

## Features
The app receives a POST request containing HTML text.
The HTML text is cleaned using the BeautifulSoup library to extract the text content.
The cleaned text is passed as a prompt to the OpenAI API.
The response from the OpenAI API is returned in a JSON format to the user.

## How to use
To run the app, you can execute the following command in the terminal:
python app.py
You can also make a POST request to the endpoint /gpt3 to generate text based on a prompt.
