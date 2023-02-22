# Teams_OpenAI_Demo

## Flask OpenAI App in Teams
This is a Flask application that makes use of Azure OpenAI API to generate text based on a given prompt. This app can then be implemented in Teams as a second step to have an OpenAI Bot experience. Azure Web App will be used to host my app and expose it to the public internet. Other ways to make your app able to integrate with Teams exist, e.g. exposing localhost via tunnelling service such as ngrok.

## Steps
1. Deploy an OpenAI Model e.g. text-davinci-003 [tutorial](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal)
2. Create a Flask app that is able to call the OpenAI model locally with the /gpt3 endpoint [code](https://github.com/margauxvp/OpenAI_FlaskApp/blob/main/app.py)
4. Create temporary outgoing webhook in Teams to get the authentication token [tutorial](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-outgoing-webhook?tabs=urljsonpayload%2Cdotnet)
5. Make some changes to your code 
3. Host the app on publicly accessible URL by making some changes [deployment center](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions?tabs=applevel#use-the-deployment-center) or [detailed tutorial](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli) 

5. Adapt the code to make your app 



## Requirements
* Flask
* OpenAI
* BeautifulSoup
* Azure KeyVault
* Azure Identity

## Azure Key Vault
The API key for the OpenAI LLM model is stored in the Azure KeyVault, and the SecretClient is used to access the API key.
In a second stage, Azure Key Vault also holds the scurity token that you receive when creating an outgoing Webhook in Teams. This is used to authenticate calls between Teams and the designated outside service.

## OpenAI API
This app uses the OpenAI API to generate text based on the prompt. The deployment ID teams-davinci003 is used to specify which OpenAI deployment to use.

## Features
The app receives a POST request containing HTML text.
The HTML text is cleaned using the BeautifulSoup library to extract the text content.
The cleaned text is passed as a prompt to the OpenAI API.
The response from the OpenAI API is returned to the Teams user.

## How to use
![Screenshot 2023-02-22 184150](https://user-images.githubusercontent.com/33750077/220710524-3afda81a-1338-45f0-8c44-777649252cc7.jpg)

