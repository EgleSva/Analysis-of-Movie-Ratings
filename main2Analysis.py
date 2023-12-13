import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import psycopg2

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

# Random pavadinimas - top 5 dazniausiai naudojami zodziai pavadinimuose, kurie yra ilgesni arba lygu nei 4 raides, pavadinimuose
col = 'title'
df_filtered = df[df[col].notnull()]
all_words = ' '.join(df_filtered[col].astype(str))
# print(all_words)
words = all_words.split()
filtered_words = [word for word in words if len(word) >= 4]

word_counts = {}
for word in filtered_words:
    word_counts[word] = filtered_words.count(word)

top_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:5]
top_words_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
# print(top_words_df)

plt.bar(top_words_df['Word'], top_words_df['Frequency'])
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 5 words in titles that are longer or equal to 4 letters')
plt.show()