# Teams_OpenAI_Demo
This sample app is designed to make it easy to integrate the powerful capabilities of OpenAI into your Microsoft Teams workflow. With just a simple POST request, you can send a message to OpenAI, receive a response, and have it formatted as a JSON object that can be easily sent to Microsoft Teams. 

## Flask OpenAI App in Teams
This is a Flask application that makes use of Azure OpenAI API to generate text based on a given prompt. This app can then be implemented in Teams as a second step to have an OpenAI Bot experience. Azure Web App will be used to host my app and expose it to the public internet. Other ways to make your app integrate with Teams exist, e.g. exposing localhost via tunnelling service such as ngrok.

## Steps
1. Deploy an OpenAI Model e.g. text-davinci-003 [tutorial](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal)
2. Create a Flask app that is able to call the OpenAI model locally with the /gpt3 endpoint [code](https://github.com/margauxvp/OpenAI_FlaskApp/blob/main/app.py)
3. Create temporary outgoing webhook in Teams to get the authentication token and store it in Key Vault *teamstoken* [tutorial](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-outgoing-webhook?tabs=urljsonpayload%2Cdotnet)
4. Finalize the app [code](https://github.com/margauxvp/Teams_OpenAI_Demo/blob/main/app.py)
5. Host the app on publicly accessible URL by making some changes [deployment center](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions?tabs=applevel#use-the-deployment-center) or [detailed tutorial](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cvscode-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli) 
6. Replace the endpoint URL with your Web App in the outgoing Webhook

## Requirements
* Flask
* OpenAI
* BeautifulSoup
* Azure KeyVault
* Azure Identity

## Azure Key Vault
The API key for the OpenAI LLM model is stored in Azure Key Vault, and the SecretClient is used to access the API key.
In a second stage, Azure Key Vault also holds the security token that you receive when creating an outgoing Webhook in Teams. This is used to authenticate calls between Teams and the designated outside service.

## OpenAI API
This app uses the OpenAI API to generate text based on the prompt. The deployment ID teams-davinci003 is used to specify which OpenAI deployment to use.

## Demonstration
![Screenshot 2023-02-22 184150](https://user-images.githubusercontent.com/33750077/220710524-3afda81a-1338-45f0-8c44-777649252cc7.jpg)

