import json
import urllib2
from pymongo import MongoClient
import pprint


'''
with open("players.json") as data:
    playerData = json.load(data)

with open("teams.json") as data:
    teamData = json.load(data)

print playerData

for player in playerData:
    full_name = player['firstName'] + " " + player['lastName']
    print full_name

print teamData
'''
def update_player_list():
    playerData = json.load(urllib2.urlopen('http://stats.nba.com/stats/commonallplayers?IsOnlyCurrentSeason=1&LeagueID=00&Season=2014-15'))
    playerData = playerData['resultSets'][0]['rowSet']
    playerList = []
    print playerData
    with open("players.json", 'w') as outfile:
        json.dump(playerData, outfile, indent=4, sort_keys=True)

def update_player_info():
    teamData = json.load(urllib2.urlopen('http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&PlayerID=203112&SeasonType=Regular+Season'))
    teamData = teamData['resultSets'][0]['rowSet']
    print teamData

def update_team_roster():
    teamData = json.load(urllib2.urlopen('http://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2014-15&TeamID=1610612737'))
    teamData = teamData['resultSets'][0]['rowSet']
    print teamData

def update_player_career_stats():
    careerStats = json.load(urllib2.urlopen('http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID=203112'))
    careerStats = careerStats['resultSets'][0]['rowSet']
    print careerStats

def update_player_game_log():
    gameLog = json.load(urllib2.urlopen('http://stats.nba.com/stats/playergamelog?LeagueID=00&PlayerID=203112&Season=2014-15&SeasonType=Regular+Season'))
    gameLog = gameLog['resultSets'][0]['rowSet']
    print gameLog



#update_player_info()
#update_player_list()
#update_team_roster()
#update_player_career_stats()
#update_player_game_log()

#client = MongoClient('mongodb://blumpk:pacers721@ds049641.mongolab.com:49641/fanalytics_zone')
#db = client.fanalytics_zone
#db = db.players
#for index in db.find():
    #print index