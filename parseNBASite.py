import json
import urllib2
from pymongo import MongoClient
import pprint


client = MongoClient('mongodb://blumpk:pacers721@ds049641.mongolab.com:49641/fanalytics_zone')
db = client.fanalytics_zone
nbaplayers = db.nbaplayers
playercareerstats = db.nbaplayercareerstats
playergamestats = db.nbaplayergamestats
playerinfodb = db.nbaplayerinfo
teamgamestats = db.nbateamgamestats
teaminfodb = db.nbateaminfo

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

playerInfoArray = ["PERSON_ID","FIRST_NAME","LAST_NAME","DISPLAY_FIRST_LAST","DISPLAY_LAST_COMMA_FIRST","DISPLAY_FI_LAST","BIRTHDATE","SCHOOL","COUNTRY","LAST_AFFILIATION","HEIGHT","WEIGHT","SEASON_EXP","JERSEY","POSITION","ROSTERSTATUS","TEAM_ID","TEAM_NAME","TEAM_ABBREVIATION","TEAM_CODE","TEAM_CITY","PLAYERCODE","FROM_YEAR","TO_YEAR","DLEAGUE_FLAG"]
def update_player_info(playerID):
    url = 'http://stats.nba.com/stats/commonplayerinfo?LeagueID=00&SeasonType=Regular+Season&PlayerID=' + str(playerID)
    teamData = json.load(urllib2.urlopen(url))
    teamData = teamData['resultSets'][0]['rowSet'][0]
    playerDict = {}
    for x in range(len(playerInfoArray)):
        playerDict[playerInfoArray[x]] = teamData[x]
    teaminfodb.insert(playerDict)
    print playerDict

teamInfoArray = ["TEAM_ID","SEASON_YEAR","TEAM_CITY","TEAM_NAME","TEAM_ABBREVIATION","TEAM_CONFERENCE","TEAM_DIVISION","TEAM_CODE","W","L","PCT","CONF_RANK","DIV_RANK","MIN_YEAR","MAX_YEAR"]
def update_team_info(teamID):
    url = 'http://stats.nba.com/stats/teaminfocommon?LeagueID=00&SeasonType=Regular+Season&season=2014-15&TeamID=' + str(teamID)
    teamData = json.load(urllib2.urlopen(url))
    teamData = teamData['resultSets'][0]['rowSet'][0]
    teamDict = {}
    for x in range(len(teamInfoArray)):
        teamDict[teamInfoArray[x]] = teamData[x]
    teaminfodb.insert(teamDict)
    print teamDict

rosterArray = ["TeamID","SEASON","LeagueID","PLAYER","NUM","POSITION","HEIGHT","WEIGHT","BIRTH_DATE","AGE","EXP","SCHOOL","PLAYER_ID"]
def update_team_roster(teamid):
    url = 'http://stats.nba.com/stats/commonteamroster?LeagueID=00&Season=2014-15&TeamID=' + str(teamid)
    teamData = json.load(urllib2.urlopen(url))
    teamData = teamData['resultSets'][0]['rowSet']
    for player in teamData:
        playerID = player[12]
        #update_player_career_stats(playerID)
        #update_player_game_log(playerID)
        update_player_info(playerID)
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
#print len(careerArray)
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

gameLogArray = ["SEASON_ID","Player_ID","Game_ID","GAME_DATE","MATCHUP","WL","MIN","FGM","FGA","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT","OREB","DREB","REB","AST","STL","BLK","TOV","PF","PTS","PLUS_MINUS"]
def update_player_game_log(playerID):
    url = 'http://stats.nba.com/stats/playergamelog?LeagueID=00&Season=2014-15&SeasonType=Regular+Season&PlayerID=' + str(playerID)
    gameLog = json.load(urllib2.urlopen(url))
    gameLog = gameLog['resultSets'][0]['rowSet']
    player = {}
    gamesArray = []
    for game in gameLog:
        gameDict = {}
        for x in range(len(gameLogArray)):
            gameDict[gameLogArray[x]] = game[x]
        gamesArray.append(gameDict)
    #print gamesArray
    player["PLAYER_ID"] = playerID
    player["STATS"] = gamesArray
    playergamestats.insert(player)
    print player

teamGameArray = ["Team_ID","Game_ID","GAME_DATE","MATCHUP","WL","MIN","FGM","FGA","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT","OREB","DREB","REB","AST","STL","BLK","TOV","PF","PTS"]
def update_team_game_log(teamID):
    url = 'http://stats.nba.com/stats/teamgamelog?LeagueID=00&Season=2014-15&SeasonType=Regular+Season&TeamID=' + str(teamID)
    gameLog = json.load(urllib2.urlopen(url))
    gameLog = gameLog['resultSets'][0]['rowSet']
    team = {}
    gamesArray = []
    for game in gameLog:
        gameDict = {}
        for x in range(len(teamGameArray)):
            gameDict[teamGameArray[x]] = game[x]
        gamesArray.append(gameDict)
    #print gamesArray
    team["Team_ID"] = teamID
    team["STATS"] = gamesArray
    teamgamestats.insert(team)
    print team

http://stats.nba.com/stats/playerdashboardbygeneralsplits?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=203112&PlusMinus=N&Rank=N&Season=2014-15&SeasonSegment=&SeasonType=Regular+Season&VsConference=&VsDivision=

for team in teamData:
    #nbateams.insert(team)
    teamid = team['teamId']
    #update_team_game_log(teamid)
    update_team_info(teamid)
    #print teamid
    #update_team_roster(teamid)

#update_player_info(200794)
#update_player_list()
#update_team_roster()
#update_player_career_stats(200794)
#update_player_game_log(200794)

#client = MongoClient('mongodb://blumpk:pacers721@ds049641.mongolab.com:49641/fanalytics_zone')
#db = client.fanalytics_zone
#db = db.players
#for index in db.find():
    #print index