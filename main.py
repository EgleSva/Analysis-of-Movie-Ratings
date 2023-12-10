import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"}
url = "https://www.imdb.com/search/title/?title_type=feature"
response = requests.get(url, headers=headers)
# print(response)

soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)

movies = soup.find_all('li', class_='ipc-metadata-list-summary-item')
# print(len(movies))

movies_list = []
