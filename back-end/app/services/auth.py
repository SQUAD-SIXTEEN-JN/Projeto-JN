import os
import requests
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = os.getenv("API_AUDIENCE")  # Igual ao que você já usa

def auth0_login(username: str, password: str):
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "audience": AUTH0_AUDIENCE,
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "scope": "openid"
    }

    headers = {"content-type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    print("Status Code:", response.status_code)
    print("Response:", response.text)

    if response.status_code != 200:
        raise ValueError("Falha na autenticação com Auth0")

    return response.json()