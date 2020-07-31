import math
import requests
import json
import time

headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer apiKey',
    }

params = {
    'from' : 1514764800,
}

def getPlayerID(username):
    requestPlayerURL = 'https://open.faceit.com/data/v4/players?nickname='+username+'&game=COUNTER%20STRIKE%3A%20GLOBAL%20OFFENSIVE'
    requestPlayerStats = requests.get(requestPlayerURL, headers=headers)
    statDeets = requestPlayerStats.json()
    elo = json.dumps(statDeets['games']['csgo']['faceit_elo'], indent=2).replace('"','')
    level = json.dumps(statDeets['games']['csgo']['skill_level'], indent=2).replace('"', '')
    playerID = json.dumps(statDeets['player_id'], indent=2).replace('"', '')
    return playerID,elo,level

playerID, elo, level = getPlayerID('krang')
gameList = []
requestGamesURL = 'https://open.faceit.com/data/v4/players/' + playerID + '/history?game=csgo&offset=0&limit=20'
requestGames = requests.get(requestGamesURL, headers=headers, params=params)
gameDeets = requestGames.json()

for count in range(20):
    games = json.dumps(gameDeets['items'][count]['match_id'], indent=2).replace('"', '')
    gameList.append(games)

def getKills(username):
    matchCount = 0
    killTotal = 0
    gameList = getMatches(username)
    for game in gameList:
        requestKillURL = 'https://open.faceit.com/data/v4/matches/' + game + '/stats'
        requestKills = requests.get(requestKillURL, headers=headers)
        killDeets = requestKills.json()
        for team in range(2):
            for player in range(5):
                try:
                    killCheck = json.dumps(killDeets['rounds'][i]['teams'][team]['players'][player]['nickname'].replace('"',''),indent=2)
                    if killCheck.replace('"', '') == username:
                        kills = json.dumps(killDeets['rounds'][i]['teams'][team]['players'][player]['player_stats']['Kills'].replace('"',''),indent=2)
                        killNum = int(kills.replace('"', ''))
                        killTotal += killNum
                        matchCount += 1
                except:
                    continue

    killAvg = round((killTotal) / matchCount)
    return killAvg


killAvg = getKills('krang')
print(killAvg)