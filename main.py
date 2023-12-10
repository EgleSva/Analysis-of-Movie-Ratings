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
for movie in movies:
    title = movie.find('h3', class_='ipc-title__text').text.strip()
    movie_details = movie.find_all('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item')
    year = None
    duration = None
    rating = None
    if len(movie_details) >= 1:
        year = movie_details[0].text.strip()
    if len(movie_details) >= 2:
        duration = movie_details[1].text.strip()
    if len(movie_details) >= 3:
        rating = movie_details[2].text.strip()
    people_rating = movie.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')
    people_rating_text = people_rating.get_text(strip=True) if people_rating else None
    critic_rating = movie.find('span', class_='sc-b0901df4-0 bcQdDJ metacritic-score-box')
    critic_rating_text = critic_rating.get_text(strip=True) if critic_rating else None
    movies_list.append({'Pavadinimas': title, 'Metai': year, 'Trukme': duration, 'Filmo indeksas': rating,
                        'Ivertinimas pagal zmones': people_rating_text, 'Ivertinimas pagal kritikus': critic_rating_text})
print(movies_list)
