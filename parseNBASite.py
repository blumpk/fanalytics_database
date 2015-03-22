import json
import urllib2
from pymongo import MongoClient
import pprint


client = MongoClient('mongodb://blumpk:pacers721@ds049641.mongolab.com:49641/fanalytics_zone')
db = client.fanalytics_zone
nbaplayers = db.nbaplayers
playercareerstats = db.nbaplayercareerstats

with open('teams.json') as data:
    teamData = json.load(data)
    #print teamid

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

rosterArray = ["TeamID","SEASON","LeagueID","PLAYER","NUM","POSITION","HEIGHT","WEIGHT","BIRTH_DATE","AGE","EXP","SCHOOL","PLAYER_ID"]
def update_team_roster(teamid):
    url = 'http://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2014-15&TeamID=' + str(teamid)
    teamData = json.load(urllib2.urlopen(url))
    teamData = teamData['resultSets'][0]['rowSet']
    for player in teamData:
        playerID = player[12]
        update_player_career_stats(playerID)
        #print playerID
'''
        teamDict = {}
        for x in range(len(rosterArray)):
            teamDict[rosterArray[x]] = player[x]
        print teamDict
'''
'''
        teamDict[rosterArray[0]] = player[0]
        teamDict[rosterArray[1]] = player[1]
        teamDict[rosterArray[2]] = player[2]
        teamDict[rosterArray[3]] = player[3]
        teamDict[rosterArray[4]] = player[4]
        teamDict[rosterArray[5]] = player[5]
        teamDict[rosterArray[6]] = player[6]
        teamDict[rosterArray[7]] = player[7]
        teamDict[rosterArray[8]] = player[8]
        teamDict[rosterArray[9]] = player[9]
        teamDict[rosterArray[10]] = player[10]
        teamDict[rosterArray[11]] = player[11]
        teamDict[rosterArray[12]] = player[12]
        nbaplayers.insert(teamDict)
        #print teamDict
'''
        #print player
    #print teamData

careerArray = ["PLAYER_ID","SEASON_ID","LEAGUE_ID","TEAM_ID","TEAM_ABBREVIATION","PLAYER_AGE","GP","GS","MIN","FGM","FGA","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT","OREB","DREB","REB","AST","STL","BLK","TOV","PF","PTS"]
print len(careerArray)
def update_player_career_stats(playerID):
    url = 'http://stats.nba.com/stats/playercareerstats?LeagueID=00&PerMode=PerGame&PlayerID=' + str(playerID)
    careerStats = json.load(urllib2.urlopen(url))
    careerStats = careerStats['resultSets'][0]['rowSet']
    allStats = []
    for stats in careerStats:
        statsDict = {}
        for x in range(len(careerArray)):
            statsDict[careerArray[x]] = stats[x]
        allStats.append(statsDict)
    player = {}
    player["PLAYER_ID"] = playerID
    player["STATS"] = allStats
    playercareerstats.insert(player)
    print player
    #allStats

    #print careerStats

def update_player_game_log():
    gameLog = json.load(urllib2.urlopen('http://stats.nba.com/stats/playergamelog?LeagueID=00&PlayerID=203112&Season=2014-15&SeasonType=Regular+Season'))
    gameLog = gameLog['resultSets'][0]['rowSet']
    print gameLog

for team in teamData:
    #nbateams.insert(team)
    teamid = team['teamId']
    #print teamid
    update_team_roster(teamid)

#update_player_info()
#update_player_list()
#update_team_roster()
#update_player_career_stats(200794)
#update_player_game_log()

#client = MongoClient('mongodb://blumpk:pacers721@ds049641.mongolab.com:49641/fanalytics_zone')
#db = client.fanalytics_zone
#db = db.players
#for index in db.find():
    #print index