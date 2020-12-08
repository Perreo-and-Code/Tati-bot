from bs4 import BeautifulSoup
import requests


def getTeslaActionsPrice():
    """Return current tesla actions price"""
    acciones_tesla_url = "https://es.investing.com/equities/tesla-motors"
    headers = {
        'OB-USER-TOKEN': '3f525c9f-690b-4ff8-af13-4ce562643af8',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    response = requests.get(acciones_tesla_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    element = soup.find("span", {"id": "last_last"})
    return element.text
