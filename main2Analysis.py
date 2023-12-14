import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
import seaborn as sns
import psycopg2
import numpy as np

# Duomenų bazės prisijungimo parametrai
db_host = 'localhost'
db_name = 'films'
db_user = 'postgres'
db_password = ''

# Prisijungiame prie duomenų bazės
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')

# SQL užklausa duomenims ištraukti
select_query = '''
    SELECT title, genre, years, duration, rating, people_rating, critic_rating, votes
    FROM imdbfilms2
'''

# Sukuriame DataFrame iš SQL duomenų
df = pd.read_sql_query(select_query, engine)

# Pasitikriname duomenis
# print(df.head())

# Tvarkome duomenis
df.replace("N/A", np.NaN, inplace=True)
df.dropna(axis=0, inplace=True)
df['years'] = pd.to_numeric(df['years'], errors='coerce')
df['people_rating'] = df['people_rating'].astype(float)
df['critic_rating'] = df['critic_rating'].astype(int)
df['duration'] = df['duration'].astype(int)
df['votes'] = df['votes'].replace(',', '', regex=True)
df['votes'] = df['votes'].astype(int)
df['title'] = df['title'].astype("string")


# # 1. lentelė. Top 5 dažniausiai naudojami žodžiai pavadinimuose, kurie yra ilgesni arba lygūs nei 4 raidės.
# col = 'title'
#
# # Išmetame eilutes su null reikšme
# df_filtered = df[df[col].notnull()]
#
# # Visus pavadinimus sujungiame į vieną eilutę
# all_words = ' '.join(df_filtered[col].astype(str))
# # print(all_words)
#
# # Atskiriame visus žodzius, kaip atskirus
# words = all_words.split()
#
# # Išsifiltruojame tik tuos žodžius, kruie turi 4 ar daugiau raidžių
# filtered_words = [word for word in words if len(word) >= 4]
#
# # Susikuriame žodžių ir jų pasikartojimų skaičių dictionary
# word_counts = {}
# for word in filtered_words:
#     word_counts[word] = filtered_words.count(word)
#
# # Dictionary pasiverčiame į tuple, tada pagal antrąjį elementą tuple (dažnis) išrikiuojame sąrašą, sąrašą rašaome mažėjančia tvarka ir paimame top 5
# top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]
# top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
# # print(top_words_df)
#
# # Piešiame grafiką
# plt.bar(top_words_df['Word'], top_words_df['Frequency'], color='darkolivegreen')
# plt.xlabel('Words')
# plt.ylabel('Frequency')
# plt.title('Graph 5. Top 5 words in titles that are longer or equal to 4 letters')
# plt.show()
# # 1 lenteles pabaiga.


# # 2 lentelė. Koreliacija - kaip kinta žmonių įvertinimas, nuo balsų kiekio
# correlation = df['votes'].corr(df['people_rating'])
#
# # Grafinis pavaizdavimas
# plt.figure(figsize=(10, 6))
# sns.regplot(x='votes', y='people_rating', data=df, scatter_kws={'s': 50, 'color': 'darkolivegreen'},
#             line_kws={'color': 'purple'})
# plt.title(f'Graph 3. Correlation between Votes and People\'s Ratings: {correlation:.2f}')
# plt.xlabel('Votes')
# plt.ylabel('People\'s Ratings')
#
# plt.show()
# # 2 lentelės pabaiga.


# # 3 lentelė. Palyginimas - kritikų ir žmonių įvertinimo vidurkis pagal filmo išleidimo metus
# df['years'] = pd.to_numeric(df['years'], errors='coerce')
#
# avg_ratings_by_year = df.groupby('years')[['people_rating', 'critic_rating']].mean()
#
# fig, ax1 = plt.subplots(figsize=(12, 6))
#
# ax1.plot(avg_ratings_by_year.index, avg_ratings_by_year['people_rating'], label='People Rating', marker='o',
#          color='darkolivegreen')
# ax1.set_xlabel('Year')
# ax1.set_ylabel('People Rating', color='darkolivegreen')
# ax1.tick_params(axis='y', labelcolor='darkolivegreen')
# ax1.set_ylim(1, 10)
#
# ax2 = ax1.twinx()
# ax2.plot(avg_ratings_by_year.index, avg_ratings_by_year['critic_rating'], label='Critic Rating', marker='o',
#          color='purple')
# ax2.set_ylabel('Critic Rating', color='purple')
# ax2.tick_params(axis='y', labelcolor='purple')
# ax2.set_ylim(1, 100)
#
# plt.title('Graph 2.Average Ratings by Year Critic vs People')
# plt.show()
# # 3 lenteles pabaiga


# # 4 lentelė. Prognozė - kaip keičiasi vidutinis balsų skaičius per filmą, pagal metus ir prognozė iki 2035
#
# # Balsų suma pagal metus
# votes_per_year = df.groupby('years')['votes'].sum()
#
# # Fimų suma pagal metus
# movies_count_per_year = df.groupby('years').size()
#
# # Balsų vidurkis
# average_votes_per_movie_per_year = votes_per_year / movies_count_per_year
#
# # Sudarome DataFrame su reikiamais duomenimis
# df_votes_per_year = pd.DataFrame({
#     'Years': average_votes_per_movie_per_year.index,
#     'Average Votes per Movie': average_votes_per_movie_per_year.values
# })
#
# df_votes_per_year = df_votes_per_year[df_votes_per_year['Years'] >= 1990]
#
# # Tiesinės regresijos modelis
# X = df_votes_per_year[['Years']]
# y = df_votes_per_year['Average Votes per Movie']
# reg_model = LinearRegression().fit(X, y)
#
# # Prognozė nuo 2024 iki 2035 metų
# future_years = pd.DataFrame({'Years': range(2024, 2036)})
# future_votes = reg_model.predict(future_years)
#
# # Sudarome DataFrame su prognoze
# df_future_votes = pd.DataFrame({
#     'Years': future_years['Years'],
#     'Average Votes per Movie (Forecast)': future_votes
# })
# # Sudarome bendrą DataFrame su esamais ir prognozuojamais duomenimis
# df_combined = pd.concat([df_votes_per_year, df_future_votes])
#
# # Grafiko piešimas
# plt.figure(figsize=(12, 8))
# plt.plot(df_combined['Years'], df_combined['Average Votes per Movie'], label='Actual (1990-2022)',
#          color='darkolivegreen')
# plt.plot(df_combined['Years'], df_combined['Average Votes per Movie (Forecast)'], label='Forecast (2024-2035)',
#          linestyle='dashed', color='purple')
# plt.title('Graph 4. Average Votes per Movie Over the Years with Forecast')
# plt.xlabel('Years')
# plt.ylabel('Average Votes per Movie')
# plt.legend()
# plt.show()
# # 4 lentelės pabaiga.


# # 5 lentelė. Top 10 populiariausių kategorijų.
# # Išsitraukiame top 10 populiariausių kategorijų
# genre_popularity = df['genre'].value_counts().head(10)
#
# # Grafikas
# genre_popularity.plot(kind='bar', color='darkolivegreen')
# plt.title('Graph 1. Top 10 most popular genres')
# plt.xlabel('Genres')
# plt.ylabel('Frequency')
# plt.xticks(rotation=45)
# plt.subplots_adjust(bottom=0.3)
# plt.show()
# # 5 lentelės pabaiga.


# # 6 lentelė. Top 10 filmų, kurių pavadinime yra žodis Christmas, geriausias įvertinimas pagal kritikus, geriausias įvertinimas pagal žmones, daugiausia balsų.
# # Filtruojame filmus, kurių pavadinime yra "Christmas"
# df_christmas = df[df['title'].str.contains('Christmas', case=False)]
#
# # Rikiuojame top10 pagal critic_rating
# top10_movies_critic = df_christmas.sort_values(by='critic_rating', ascending=False).head(10)
#
# # Votes paverčiame į skaičių
# top10_movies_critic['votes'] = top10_movies_critic['votes'].apply(lambda x: pd.to_numeric(x, errors='coerce'))
#
# # Grafiko dydis
# fig, ax1 = plt.subplots(figsize=(12, 8))
#
# # Pirma ašis
# ax1.set_xlabel('Title')
# ax1.set_ylabel('Critic rating', color='darkolivegreen')
# ax1.bar(top10_movies_critic['title'], top10_movies_critic['critic_rating'], label='Critic Rating', color='darkolivegreen')
# ax1.tick_params(axis='y', labelcolor='darkolivegreen')
#
# # Antra ašis
# ax2 = ax1.twinx()
# color = 'tab:purple'
# ax2.set_ylabel('People rating', color=color)
# ax2.plot(top10_movies_critic['title'], top10_movies_critic['people_rating'], label='People Rating', marker='o', color=color)
# ax2.tick_params(axis='y', labelcolor=color)
#
# # Trecia ašis
# ax3 = ax1.twinx()
# color = 'tab:orange'
# ax3.spines['right'].set_position(('outward', 60))
# ax3.set_ylabel('Votes', color=color)
# ax3.plot(top10_movies_critic['title'], top10_movies_critic['votes'], label='Votes', marker='s', color=color)
# ax3.tick_params(axis='y', labelcolor=color)
# ax3.set_xticks(ax1.get_xticks())  # Pridėta eilutė
#
# # Pridėta eilutė, kad nustatytumėte ašies ribas nuo 0 iki didžiausios votes reikšmės
# max_votes = top10_movies_critic['votes'].max()
# ax3.set_ylim(0, max_votes)
#
# # Pasukimas
# ax1.set_xticklabels(top10_movies_critic['title'], rotation=45, ha='right')
#
# # Aprašymas
# fig.suptitle('Graph 6. Top 10 "Christmas" Critically Acclaimed Movies with People Ratings and Votes')
# fig.tight_layout(rect=[0, 0.03, 1, 0.95])
# plt.show()
# # 6 lentelės pabaiga.