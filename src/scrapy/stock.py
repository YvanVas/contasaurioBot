from bs4 import BeautifulSoup
import requests


def get_price(url: str) -> str:
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('h1', class_='productname').getText().strip()
    price = soup.find('span', class_='productPrice').getText().strip()

    return f"{name}\nPrecio: {price.replace('Gs    ', 'Gs ')}"

