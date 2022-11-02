from bs4 import BeautifulSoup
import requests


def get_product(url: str) -> str:
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('span', class_='base').getText()
    price = soup.find('span', class_='price').getText()
    stock = soup.find(
        'div', class_='stock available').getText().replace('\n', '')

    return f"{name}\n{stock}\nPrecio: {price}"
