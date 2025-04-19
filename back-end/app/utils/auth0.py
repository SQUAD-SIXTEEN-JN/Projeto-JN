import requests

JWKS_URL = "https://myapp.auth0.com/.well-known/jwks.json"

def get_public_key():
    try:
        response = requests.get(JWKS_URL)
        jwks = response.json()
        return jwks["keys"][0]
    except Exception:
        raise ValueError("Erro ao obter a chave pública do Auth0")
