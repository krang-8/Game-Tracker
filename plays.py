import math
import requests
import json
import time

headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer 7155a5f7-f233-46a4-a175-6b514b6cd953',
    }

params = {
    'from' : 1514764800,
}

def getPlayerID(username):
    requestPlayerURL = 'https://open.faceit.com/data/v4/players?nickname='+username+'&game=COUNTER%20STRIKE%3A%20GLOBAL%20OFFENSIVE'
    requestPlayerStats = requests.get(requestPlayerURL, headers=headers)
    statDeets = requestPlayerStats.json()
    playerID = json.dumps(statDeets['player_id'], indent=2).replace('"', '')
    return playerID


def getMatches(username):
    killTotal = 0
    runTimes = 0
    playerID= getPlayerID(username)
    requestGamesURL = 'https://open.faceit.com/data/v4/players/' + playerID + '/history?game=csgo&offset=0&limit=20'
    requestGames = requests.get(requestGamesURL, headers=headers, params = params)
    gameDeets = requestGames.json()
    for count in range(0, 20):
        try:
            game = json.dumps(gameDeets['items'][count]['match_id'], indent=2).replace('"', '')
            requestKillURL = 'https://open.faceit.com/data/v4/matches/' + game + '/stats'
            requestKills = requests.get(requestKillURL, headers=headers)
            killDeets = requestKills.json()
            for team in range(2):
                for player in range(5):
                    killCheck = json.dumps(killDeets['rounds'][0]['teams'][team]['players'][player]['nickname'].replace('"', ''), indent=2)
                    if killCheck.replace('"', '') == username:
                        kills = json.dumps(
                            killDeets['rounds'][0]['teams'][team]['players'][player]['player_stats']['Kills'].replace(
                                '"', ''), indent=2)
                        killNum = int(kills.replace('"', ''))
                        killTotal += killNum
                        runTimes += 1


        except:
            print('oops')
            continue
    killAvg = round((killTotal) / runTimes)
    return killAvg





start_time = time.time()
killAvg = getMatches('krang')
print(killAvg)
print("My program took", time.time() - start_time, "to run")

