import json 
import pandas as pd 
import requests 
from nba_api.stats.static import teams 
import urllib 

url = 'https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2018-19&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=' 
 

def get_table_from_url(url): 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'} 
    response = requests.get(url, headers=headers) 
    json_obj = response.text 
    d = json.loads(json_obj) 
    df = pd.DataFrame(d['resultSets'][0]['rowSet'], columns=d['resultSets'][0]['headers']) 
    return df

# type = {0: General shooting, 1: ShotClockShooting, 2: DribbleShooting, 3: ClosestDefenderShooting, 4: ClosestDefenderShooting +10} 

def get_team_sht_dashboard(type, team_id, headers): 
    url = 'https://stats.nba.com/stats/teamdashptshots?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PerMode=Totals&Period=0&Season=2018-19&SeasonSegment=&SeasonType=Regular+Season&TeamID={}&VsConference=&VsDivision='.format(team_id) 
    response = requests.get(url, headers=headers) 
    json_obj = response.text 
    d = json.loads(json_obj) 
    df = pd.DataFrame(d['resultSets'][type]['rowSet'], columns=d['resultSets'][type]['headers']) 
    return df 

     

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'} 
team_list = [] 
for team_info in teams.get_teams(): 
    team_list.append(team_info['id']) 
    

# with respect to defender's proximity 

df_list = [] 
for t_id in team_list: 
    sample = get_team_sht_dashboard(3, str(t_id), headers) 
    df_list.append(sample) 
merged_df = pd.concat(df_list) 
pivot_res = pd.pivot_table(merged_df, index='TEAM_NAME', columns = ['CLOSE_DEF_DIST_RANGE'], values = ['FGA_FREQUENCY', 'FG2A_FREQUENCY', 'FG3A_FREQUENCY']) 
fga_freq = pivot_res.loc[:, 'FGA_FREQUENCY'] 
fga_freq.sort_values('6+ Feet - Wide Open', ascending=False)