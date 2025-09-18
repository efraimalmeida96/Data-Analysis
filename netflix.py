# %%
import pandas as pd
# %%
import matplotlib.pyplot as plt

# %%
df = pd.read_csv("./files/netflix_data.csv")
df

# %%

release_year = (df["release_year"] >= 1990) & (df["release_year"] <= 1999)

df_90s = df[release_year]
df_90s

# %%

df_90s_movies = df_90s[df_90s["type"] == "Movie"] # filter
df_90s_movies

# %%
action_movies = df_90s_movies[df_90s_movies['genre'] == "Action"]
action_movies

# %%

duration = 120

# %%

plt.title("Movies from 90's", color='blue') # title of the graphic
plt.hist(df_90s['duration']) # creates a histogram
plt.xlabel('Duration')
plt.ylabel('Number of movies')
plt.show()

# %%

df[['type', 'genre']] # shows only thoses columns 

# %%

df['genre'] == 'Action' # return a series, boolean Series

action = df[df['genre'] == 'Action'] # DataFrame, return filter
# %%

genre = df['genre'] == 'Action'
year = df['release_year'] >= 2018

df[genre & year].sort_values(by="release_year", ascending=True)[['title', 'type', 'genre', 'release_year']]