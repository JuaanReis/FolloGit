"""
    Functions to follow or unfollow who you follow or don't follow.
    Don't forget to create a .env

    Date-creation: 04/09/2025
    Last-modification: -
    Author: JuaanReis
"""
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# === CONFIGURAÇÕES ===
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")

# Headers com autenticação
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# === FUNÇÕES ===

def get_following():
    """Retorna lista de usernames que você segue."""
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/following"
    return fetch_paginated(url)

def get_followers():
    """Retorna lista de usernames que te seguem."""
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/followers"
    return fetch_paginated(url)

def fetch_paginated(url):
    """Lida com paginação da API do GitHub."""
    users = []
    while url:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        users += [user['login'] for user in response.json()]
        url = response.links.get('next', {}).get('url')
    return users

def follow_user(username):
    """Seguir usuário."""
    url = f"https://api.github.com/user/following/{username}"
    response = requests.put(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"[+] Seguiu: {username}")
    else:
        print(f"[!] Erro ao seguir {username}: {response.status_code}")

def unfollow_user(username):
    """Deixar de seguir usuário."""
    url = f"https://api.github.com/user/following/{username}"
    response = requests.delete(url, headers=HEADERS)
    if response.status_code == 204:
        print(f"[-] Deixou de seguir: {username}")
    else:
        print(f"[!] Erro ao deixar de seguir {username}: {response.status_code}")

# === EXECUÇÃO ===

def main():
    following = set(get_following())
    followers = set(get_followers())

    print(f"[+] Você segue: {len(following)}")
    print(f"[+] Te seguem: {len(followers)}")

    # Deixar de seguir quem não te segue
    for user in following - followers:
        unfollow_user(user)

    # Seguir quem te segue mas você não segue
    for user in followers - following:
        follow_user(user)

if __name__ == "__main__":
    main()
