from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import psycopg2

# Aprašoma duombazė ir sukuriama lentelė
db_host = 'localhost'
db_name = 'films'
db_user = 'postgres'
db_password = ''

connection = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
cursor = connection.cursor()
create_table_query = '''
    CREATE TABLE IF NOT EXISTS imdbfilms(
        id SERIAL PRIMARY KEY,
        title text,
        genre text,
        years text,
        duration text,
        rating text,
        people_rating text,
        critic_rating text,
        votes text
    )
'''
cursor.execute(create_table_query)

# Nustatome webdriver'io kelią
webdriver_path = "C:/Users/Egle/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
service = Service(webdriver_path)
service.start()

# Sukuriamas naujas webdriver
driver = webdriver.Chrome(service=service)

# Funkcija, kuri paspaudžia "More" mygtuką ir laukia, kol bus įkelti nauji rezultatai
def click_more():
    try:
        more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ipc-see-more'))
        )
        driver.execute_script("arguments[0].scrollIntoView();", more_button)
        more_button.click()

        # Laukiame, kol bus įkelti nauji rezultatai
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.ipc-metadata-list-summary-item')))
    except Exception as e:
        print(f"Error clicking 'More' button: {e}")
        pass


# Funkcija, kuri konvertuoja bendrą trukmę į minutes
def convert_duration_to_minutes(duration):
    if duration is None:
        return None

    # h ir m ištraukiame
    match = re.match(r'(\d+)h\s*(\d*)m*', duration)

    if match:
        hours = int(match.group(1))
        minutes = int(match.group(2)) if match.group(2) else 0
        return hours * 60 + minutes
    else:
        return None


# Sukuriame sąrašą filmų
movies_list = []

# Driver'iui paduodame link'ą, kurį scrape'insime
url = "https://www.imdb.com/search/title/?title_type=feature"
driver.get(url)

# Puslapio scrolinimas
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)  # Uzkrovimo laikas

# Paspaudžiame "See More" mygtuką nurodytą kiekį kartų
for i in range(220):
    click_more()
    # Scrollinam
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Laukiam kol uzkrauna

# Parsisiunčiame HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')
movies = soup.find_all('li', class_='ipc-metadata-list-summary-item')

# Apsirašome, kuriuos duomenis ištraukti
for movie in movies:
    title_element = movie.find('h3', class_='ipc-title__text')
    title = re.sub(r'^\d+\.\s*', '', title_element.text.strip()) if title_element else None

    inner_link = movie.find('a', 'ipc-title-link-wrapper').get('href')
    full_link = "https://www.imdb.com" + inner_link
    driver.get(full_link)
    soup_inner = BeautifulSoup(driver.page_source, 'html.parser')
    genre_list = soup_inner.find_all('a', class_='ipc-chip ipc-chip--on-baseAlt')
    if len(genre_list) >= 1:
        genre = genre_list[0].text.strip()

    movie_details = movie.find_all('span', class_='sc-43986a27-8 jHYIIK dli-title-metadata-item')
    year = None
    duration = None
    rating = None

    if len(movie_details) >= 1:
        year = movie_details[0].text.strip()
    if len(movie_details) >= 2:
        duration = movie_details[1].text.strip()
        # Konvertuojame trukmę į monutes
        duration = convert_duration_to_minutes(duration)
    if len(movie_details) >= 3:
        rating = movie_details[2].text.strip()

    people_rating = movie.find('span', class_='ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating')
    people_rating_text = people_rating.get_text(strip=True).split('(')[0] if people_rating else None

    critic_rating = movie.find('span', class_='sc-b0901df4-0 bcQdDJ metacritic-score-box')
    critic_rating_text = critic_rating.get_text(strip=True) if critic_rating else None

    votes_element = movie.find('div', class_='sc-53c98e73-0 kRnqtn')
    votes_text = votes_element.text.strip() if votes_element else None

    # Jei 'Votes' nėra pateikti, priskiriame 'N/A'
    votes = 'N/A' if votes_text is None else f"{int(float(''.join(filter(str.isdigit, votes_text.replace(',', ''))))) :,}"

    # Jei 'Trukme' nėra pateikta, priskiriame 'N/A'
    trukme = 'N/A' if duration is None else duration

    movies_list.append({'Pavadinimas': title, 'Zanras': genre, 'Metai': year, 'Trukme': trukme, 'Filmo indeksas': rating,
                        'Ivertinimas pagal zmones': people_rating_text,
                        'Ivertinimas pagal kritikus': critic_rating_text,
                        'Votes': votes})

    # Įrašome duomenis į SQL lentelę
    insert_query = '''
        INSERT INTO imdbfilms(title, genre, years, duration, rating, people_rating, critic_rating, votes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    try:
        cursor.execute(insert_query, (title, genre, year, trukme, rating, people_rating_text, critic_rating_text, votes))
        connection.commit()
    except Exception as e:
        print(f"Error inserting data into the database: {e}")

# Uždarome webdriver
driver.quit()

# Sukuriame DataFrame ir išsaugome į CSV
df = pd.DataFrame(movies_list)
# df.to_csv("imdbfilms.csv", index=False)
# print(df)

# Uždarome duombazės prisijungimą
cursor.close()
connection.close()
# Darbas su svetainės duomenimis baigtas