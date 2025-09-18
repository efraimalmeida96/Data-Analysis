# %%

import pandas as pd

df = pd.read_csv('./files/ginf.csv')
df
# %%
import matplotlib.pyplot as plt

# %%
### 1: total of games for country
'''
num_games = df["country"].value_counts()
positions = range(len(num_games))

plt.figure(figsize=(8, 6))
plt.bar(positions, num_games)
plt.xticks(positions, num_games.index)
plt.xlabel('Contry')
plt.ylabel('Games Played')
plt.show()
'''
df["country"].value_counts().plot.bar()

# %%
### 2: gols mean per game per season

df["total_goals"] = df["fthg"] + df["ftag"]
df["total_goals"]

df.groupby('season')["total_goals"].mean()
# %%
df.groupby('season')["total_goals"].mean().plot.line()

# %%
### 3: team with most win playing home 

# home_team = df.groupby('ht')
df['win'] = df['fthg'] > df['ftag']

df['win']

# %%
df[df['win']].groupby('ht').size().sort_values(ascending=False).head(10).plot.barh()

# %%
df.groupby('win')['ht'].value_counts().sort_values(ascending=False)

### 4: probabilty of draw for country

df['draw'] = df['fthg'] == df['ftag']

df[df['draw']].groupby('country').size().sort_values(ascending=False)

# %%
### 5: compare the odds between leagues

df.groupby('league')
league_mean = df.groupby('league')[['odd_h', 'odd_d','odd_a']].mean()

league_mean.plot(kind='bar')