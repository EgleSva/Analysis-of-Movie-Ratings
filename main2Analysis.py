import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import seaborn as sns
import psycopg2

# Duomenų bazės prisijungimo parametrai
db_host = 'localhost'
db_name = 'films'
db_user = 'postgres'
db_password = '3T8tWn4ME'

# Prisijungiame prie duomenų bazės
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}')

# SQL užklausa duomenims ištraukti
select_query = '''
    SELECT title, genre, years, duration, rating, people_rating, critic_rating, votes
    FROM imdbfilms
'''

# Sukuriame DataFrame iš SQL duomenų
df = pd.read_sql_query(select_query, engine)

# Peržiūrime duomenis
# print(df.head())

# Apsivalome duomenis
df.dropna(axis=0, inplace=True)
df['years'] = pd.to_numeric(df['years'], errors='coerce')
df['people_rating'] = df['people_rating'].astype(float)
df['critic_rating'] = df['critic_rating'].astype(int)
df['duration'] = df['duration'].astype(int)
df['votes'] = df['votes'].replace(',', '', regex=True)
df['votes'] = df['votes'].astype(int)
df['title'] = df['title'].astype("string")


# Top 5 populiariausia filmu metai
populiariausi_metai = df['years'].value_counts().head(5)
# print(populiariausi_metai)

# 5 lentele. Random pavadinimas - top 5 dazniausiai naudojami zodziai pavadinimuose, kurie yra ilgesni arba lygu nei 4 raides, pavadinimuose
col = 'title'

# Ismetame eilutes su null reiksme
df_filtered = df[df[col].notnull()]

# visus pavadinimus sujungiame i viena eilute
all_words = ' '.join(df_filtered[col].astype(str))
# print(all_words)

# atskiriame visus zodziu kaip atskirus
words = all_words.split()

# issifiltruojam tik tuos zodziu, kruie turi 4 ar daugiau raidziu
filtered_words = [word for word in words if len(word) >= 4]

# susikuriam zodziu ir ju pasikartojimu skaiciu dictionary
word_counts = {}
for word in filtered_words:
    word_counts[word] = filtered_words.count(word)

# dictionary pasiverciame i tuple, tada pagal antraji elementa tuple (daznis) issrikiuojam sarasa, sarasa rasaome mazejancia tvarka ir paimam top 5
top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]
top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
# print(top_words_df)

# priesiame grafika
plt.bar(top_words_df['Word'], top_words_df['Frequency'])
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 5 words in titles that are longer or equal to 4 letters')
plt.show()
# 5 lentele pabaiga.


# # 1 lentele.  Koreliacija - kaip kinta zmoniu ivertinimas, nuo balsu kiekio
# correlation = df['votes'].corr(df['people_rating'])
#
# # Grafinis pavaizdavimas
# plt.figure(figsize=(10, 6))
# sns.regplot(x='votes', y='people_rating', data=df, scatter_kws={'s': 50}, line_kws={'color': 'red'})
# plt.title(f'Correlation between Votes and People\'s Ratings: {correlation:.2f}')
# plt.xlabel('Votes')
# plt.ylabel('People\'s Ratings')
#
# plt.show()
# # 1 lentele pabaiga.


# 6 lentele. Penktadienio filmo rekomendacija - Top 10, geriausias ivertinimas pagal kritikus, geriausias ivertinimas pagal zmones, daugiausia balsu
# sortinam top10
top10_movies_critic = df.sort_values(by='critic_rating', ascending=False).head(10)

# Votes to numeric
top10_movies_critic['votes'] = top10_movies_critic['votes'].apply(lambda x: pd.to_numeric(x, errors='coerce'))

# dydis
fig, ax1 = plt.subplots(figsize=(12, 8))

# pirma asis
color = 'tab:blue'
ax1.set_xlabel('Title')
ax1.set_ylabel('Critic rating', color=color)
ax1.bar(top10_movies_critic['title'], top10_movies_critic['critic_rating'], label='Critic Rating', color=color)
ax1.tick_params(axis='y', labelcolor=color)

# antra asis
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('People rating', color=color)
ax2.plot(top10_movies_critic['title'], top10_movies_critic['people_rating'], label='People Rating', marker='o', color=color)
ax2.tick_params(axis='y', labelcolor=color)

# trecia asis
ax3 = ax1.twinx()
color = 'tab:green'
ax3.spines['right'].set_position(('outward', 60))
ax3.set_ylabel('Votes', color=color)
ax3.plot(top10_movies_critic['title'], top10_movies_critic['votes'], label='Votes', marker='s', color=color)
ax3.tick_params(axis='y', labelcolor=color)
ax3.set_xticks(ax1.get_xticks())  # Pridėta eilutė

# Pridėta eilutė, kad nustatytumėte ašies ribas nuo 0 iki didžiausios votes reikšmės
max_votes = top10_movies_critic['votes'].max()
ax3.set_ylim(0, max_votes)

# pasukimas
ax1.set_xticklabels(top10_movies_critic['title'], rotation=45, ha='right')

# aprasymas
fig.suptitle('Top 10 Critically Acclaimed Movies with People Ratings and Votes')
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
# 6 lentele pabaiga.

