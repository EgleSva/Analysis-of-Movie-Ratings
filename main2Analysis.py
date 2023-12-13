import pandas as pd
import matplotlib.pyplot as plt

# # Load data from CSV
df = pd.read_csv("imdb4.csv")

### Apsivalome duomenis

df.dropna(axis=0, inplace=True)
df['years'] = pd.to_numeric(df['years'], errors='coerce')
df['people_rating'] = df['people_rating'].astype(float)
df['critic_rating'] = df['critic_rating'].astype(int)
df['duration'] = df['duration'].astype(int)
df['votes'] = df['votes'].replace(',', '', regex=True)
df['votes'] = df['votes'].astype(int)

## pasitikriname, kokius duomenu tipus turime
# column_types = df.dtypes
# print(column_types)

### Zmoniu ir kritiku reitingai per metus
avg_ratings_by_year = df.groupby('years')[['people_rating', 'critic_rating']].mean()

fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.plot(avg_ratings_by_year.index, avg_ratings_by_year['people_rating'], label='People Rating', marker='o', color='green')
ax1.set_xlabel('Year')
ax1.set_ylabel('People Rating', color='green')
ax1.tick_params(axis='y', labelcolor='green')
ax1.set_ylim(1, 10)
ax2 = ax1.twinx()
ax2.plot(avg_ratings_by_year.index, avg_ratings_by_year['critic_rating'], label='Critic Rating', marker='o', color='red')
ax2.set_ylabel('Critic Rating', color='red')
ax2.tick_params(axis='y', labelcolor='red')
ax2.set_ylim(1, 100)
plt.title('Average Ratings by Year')
# plt.show()

### Top 10 filmu, kurie turi vidutiniskai geriausius ivertinimus, atsizvelgiant i zmoniu balsavima ir kritiku balsavima


### Top 5 populiariausia filmu metai
populiariausi_metai = df['years'].value_counts().head(5)
# print(populiariausi_metai)

