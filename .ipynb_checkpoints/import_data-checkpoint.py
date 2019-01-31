import json 
import pandas as pd 
import requests 
from nba_api.stats.static import teams 
import urllib 

uri = 'https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2018-19&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=' 
 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"} 
def get_table_from_url(uri, headers):     
    response = requests.get(uri, headers=headers) 
    json_obj = response.text 
    d = json.loads(json_obj) 
    df = pd.DataFrame(d['resultSets'][0]['rowSet'], columns=d['resultSets'][0]['headers']) 
    return df

# type = {0: General shooting, 1: ShotClockShooting, 2: DribbleShooting, 3: ClosestDefenderShooting, 4: ClosestDefenderShooting +10} 

def get_team_sht_dashboard(type, team_id, headers): 

    uri = 'https://stats.nba.com/stats/teamdashptshots?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&Month=0&OpponentTeamID=0&Outcome=&PerMode=Totals&Period=0&Season=2018-19&SeasonSegment=&SeasonType=Regular+Season&TeamID={}&VsConference=&VsDivision='.format(team_id) 

    response = requests.get(uri, headers=headers) 
    json_obj = response.text 
    d = json.loads(json_obj) 
    df = pd.DataFrame(d['resultSets'][type]['rowSet'], columns=d['resultSets'][type]['headers']) 
    return df 