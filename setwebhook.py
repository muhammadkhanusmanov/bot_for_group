import requests
import os

url = 'https://echobot1deploy.pythonanywhere.com/webhook'


TOKEN = os.environ['Token']

payload = {
    "url":url
}

r = requests.get(f"https://api.telegram.org/bot{TOKEN}/setWebhook", params=payload)
r = requests.get(f"https://api.telegram.org/bot{TOKEN}/GetWebhookInfo", params=payload)



print(r.json())