# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%
df = pd.read_csv('./files/game.csv')
df
# %%

# %%
### 1: victory per season (home team)
# size shows how much; value_counts shows the frequency

df[df['win_home']].groupby('team_name_home').size()

# %%
### 1: victory per season (home team)
df2 = df[df['game_date'] >= '2021-10-19 00:00:00'].copy()
df2
# %%
df2['win_home'] = df2["wl_home"] == 'W' # create a new column 'win_home' that is True if the home team won
df2['win_home']
#  %%
df2[df2['win_home']].groupby(['team_name_home']).size()

# %%
### 2: Mean point per season

pts_home_away = df2.groupby('season_id')[['pts_home', 'pts_away']].mean()

pts_home_away.plot.line()

# %%
### 3: Top 10 teams with more wins

team_name_home = df2[df2['win_home']].groupby(['team_name_home']).size().sort_values(ascending=False).head(10)
team_name_home.plot.barh()

# %%
### 4: distribution of points scored by the home team 
pts_home = df2.groupby('team_name_home')['pts_home'].sum()
pts_home.plot.hist()

# %%
### 5: comparison of rebouns and assistance (home vs away)

reb_ast = df2.groupby('team_name_home')[['reb_home', 'ast_home', 'reb_away', 'ast_away']].mean()
reb_ast.plot(kind='bar')

# %%
#
reb_ast = df2[df['team_name_home'].isin(['Atlanta Hawks', 'Boston Celtics'])].groupby('team_name_home')[['reb_home', 'ast_home', 'reb_away', 'ast_away']].mean()
reb_ast.plot(kind='bar')

# %%
### 6: time line of points 
points_hm = df2.groupby(['season_id', 'game_date'])['pts_home'].mean().unstack('season_id')
points_hm.plot.line(rot=90)

# %%

### 7: relations betweeen turnovers and loses

# tov_home = df2.groupby('wl_home')[['tov_home']].mean()
# mean_to_lose = df2[df['wl_home'] == 'L']['tov_home'].mean()
# mean_to_win = df2[df['wl_home'] == 'W']['tov_home'].mean()

compare = df2.groupby('wl_home')['tov_home'].mean().reset_index()
compare.columns = ['Situation', 'Mean_TO_Home']

# compare = compare.set_index('Situation').loc[['L', 'W']].reset_index()

# compare.plot(kind='bar',
#              x='Situation',
#              y='Mean_TO_Home')

plt.bar(compare['Situation'], compare['Mean_TO_Home'], color=['red', 'green'])
plt.title('relations betweeen turnovers and loses')
plt.xlabel('Game situation (L= Lose, W = Win)')
plt.ylabel('Mean of Turnovers')
plt.show()

# %%
### 8: Heatmap of fouls per season 

personal_fouls = df2.groupby(['team_abbreviation_home', 'season_id'])['pf_home'].mean().reset_index()
heat_map_data = personal_fouls.pivot(index='team_abbreviation_home', columns='season_id', values='pf_home')
plt.figure(figsize=(12, 6))
plt.imshow(heat_map_data, cmap='coolwarm', aspect='auto')

plt.title('Mean of Fouls per Team and Season')
plt.xlabel('Season')
plt.ylabel('Team')

plt.xticks(ticks=range(len(heat_map_data.columns)), labels=heat_map_data.columns)
plt.yticks(ticks=range(len(heat_map_data.index)), labels=heat_map_data.index)

plt.colorbar(label='Mean of Fouls')

plt.tight_layout()
plt.show()

# %%

### 9: most contest game
# calculate the abs between home points and away points
df2['diff_pts'] = (df2['pts_home'] - df2['pts_away']).abs()

# min value of the diff
minor_diff = df2['diff_pts'].min()

# most contest games
contest_games = df2[df2['diff_pts'] == minor_diff]

contest_games[['team_name_home', 'team_name_away', 'pts_home', 'pts_away', 'diff_pts']]

# %%

### 10: home team, win rate

df2['win_rate_home'] = df2['wl_home'] == 'W'

win_rate_home = df2.groupby('team_name_home')['win_rate_home'].mean().sort_values(ascending=False).head(5)

win_rate_home

#%%

# -=-=-=-=-=-=-==-= PART II =-=-=-=-=-=-==-=-

### 1 Game with more points combine 
df2['sum_points'] = df2['pts_home'] + df2['pts_away']

df2[['sum_points', 'matchup_home']].sort_values(by='sum_points', ascending=False).head(1)

#%%
# too slow, scan all the dataframe but works and it's a clean code
# df2[['game_id', 'game_date', 'sum_points', 'matchup_home']].sort_values(by='sum_points', ascending=False).head(1)

df2['sum_points'] = df2['pts_home'] + df2['pts_away']

idx = df2['sum_points'].idxmax() # find the game with most point by the index

result = df2.loc[idx, ['game_id', 'game_date', 'matchup_home', 'sum_points']]

result

# %%
### 2 games with overtime

# The 'min' column represents the total minutes played by the team.
# Standard game = 240 (48 mins * 5 players). > 240 implies overtime.
df2[df2['min'] > 240][['game_date', 'matchup_home', 'min']]

#%%
# df2.groupby('season_id').apply(lambda x: (x['min'] > 240).sum())
games_ot_per_season = df2[df2['min']> 240].groupby('season_id').size() 

games_ot_per_season

# %%
### 3 how many games had on each season 
games_per_season = df2.groupby('season_id').size()

games_per_season.plot.line() # pandas has a built-in plotting function

# %%
# with matplotlib

plt.plot(games_per_season.index, games_per_season.values) # x data, y data
plt.show

#%%
# with seaborn


sns.lineplot(x=games_per_season.index, y=games_per_season.values)

#%%
### 4 home win percentage by season

# df2[['season_id', 'game_date', 'game_id', 'matchup_away', 'matchup_home']]

home_win_percentage = df2.groupby('season_id')['game_id'].size()
# home_win_percentage = df2.groupby('season_id')['game_id'].count()

home_win_percentage
#%%
# counted all games by filtering the win home games
total_win_home_team = df2[df2['wl_home'] == 'W'].groupby('season_id').size()
total_win_home_team

#%%

hm_win_perctge = (total_win_home_team / games_per_season) * 100
hm_win_perctge

#%% 
### 5 Average points in wins vs losses (home team)

avg_points_w_vs_l = df2.groupby(['season_id', 'wl_home'])['pts_home'].mean().unstack('wl_home') # : Pivots the 'wl_home' (W/L) into columns, giving a DataFrame
avg_points_w_vs_l

#%%
### 6 