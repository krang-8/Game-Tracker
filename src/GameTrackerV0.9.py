import requests
import json
import discord
from discord.ext import commands
import math


### api key 
headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer faceitAPIKEY',
    }

## setting up params for getting game info
params = (
        ('type', 'ongoing'),
        ('offset', '0'),
        ('limit', '20'),
    )

### Function : requestMatch
### Parameters : headers,params,hub
### returns : matchDeets or None (returns None if it fails, still trying to figure out why it fails sometimes randomly)
### calls the api and uses the json data to retrieve match details
def requestMatch(headers,params,hub):
    try:
        requestURL = 'https://open.faceit.com/data/v4/hubs/' + hub + '/matches'
        response = requests.get(requestURL, headers=headers, params=params)
        matchDeets = response.json()
        return matchDeets
    except :
        return None

### Function : liveGames
### Parameters : headers,params,hub
### returns : matchList
### calls the api, gets the match id, concludes match link, appends the match link to an initialized matchList
def liveGames(headers,params,hub):


    matchList = []


    packageName = "items"
    gameRoom = "match_id"
    players = ""
    matchDeets = requestMatch(headers,params,hub)
    testVar = True
    COUNTER = 0

    if matchDeets != None:
        while testVar != False:
            try:
                matchPackage = json.dumps(matchDeets[packageName][COUNTER][gameRoom])
                matchLink = "https://www.faceit.com/en/csgo/room/"+matchPackage
                fixedMatchLink = matchLink.replace('"', '')
                if fixedMatchLink not in matchList :
                    matchList.append(fixedMatchLink)
                COUNTER += 1
            except:
                testVar = False


        return matchList




## run discord bot
client = commands.Bot(command_prefix = ".")

postedMatches = []

### Function : getPlayers
### Parameters : match
### Returns : playerList1, playerList2
### requests player details and finds players and seperates them into 2 lists, 1 for each team/faction
def getPlayers(match):
    teamRequestsURL = 'https://open.faceit.com/data/v4/matches/' + match[36:]
    requestMatch = requests.get(teamRequestsURL, headers = headers)
    playerDeets = requestMatch.json()
    factionList = ['faction1','faction2']
    playerList1 = []
    playerList2 = []
    for faction in factionList:
        for count in range(0,5):
            player = json.dumps(playerDeets['teams'][faction]['roster'][count]['nickname']).replace('"', '')
            if faction == 'faction1':
                if player not in playerList1:
                    playerList1.append(player)
            if faction == 'faction2':
                if player not in playerList2:
                    playerList2.append(player)
    return playerList1,playerList2






def makeEmbed(playerList1,playerList2, match, map, eloWonA, eloLostA, eloWonB, eloLostB):
    embed = discord.Embed(title="Live Game", description=map, color=0xff5500)
    embed.set_author(name="MATCH", url=match,icon_url="https://pbs.twimg.com/profile_images/1262464144802013184/BHLstW-J_400x400.jpg")
    embed.add_field(name="__**Team A**__" + "             ", value='**Elo: ' +'+' +eloWonA +'/' + eloLostA+'**' +'\n' +"[{}](https://www.faceit.com/en/players/{})".format(playerList1[0],playerList1[0])+ '\n' + "[{}](https://www.faceit.com/en/players/{})".format(playerList1[1],playerList1[1]) + '\n' + "[{}](https://www.faceit.com/en/players/{})".format(playerList1[2],playerList1[2]) + '\n' + "[{}](https://www.faceit.com/en/players/{})".format(playerList1[3],playerList1[3]) + '\n' +"[{}](https://www.faceit.com/en/players/{})".format(playerList1[4],playerList1[4]), inline=True)
    embed.add_field(name="               " + "__**Team B**__",value='**Elo: ' +'+' + eloWonB +'/'+ eloLostB+'**' +'\n' + "[{}](https://www.faceit.com/en/players/{})".format(playerList2[0],playerList2[0]) + '\n' + "[{}](https://www.faceit.com/en/players/{})".format(playerList2[1],playerList2[1]) + '\n' + "[{}](https://www.faceit.com/en/players/{})".format(playerList2[2],playerList2[2]) + '\n' + "[{}](https://www.faceit.com/en/players/{})".format(playerList2[3],playerList2[3]) + '\n' + "[{}](https://www.faceit.com/en/players/{})".format(playerList2[4],playerList2[4]), inline=True)
    embed.set_footer(text="MESL Tracker made by Krang")
    embed.set_image(url='https://media.discordapp.net/attachments/735918664053948478/736380111665889350/Webp.net-resizeimage_13.png')
    return embed


def getMap(statusDeets):
    try:
        map = json.dumps(statusDeets['voting']['map']['pick'])
        if map != None:
            return map
        else:
            return None
    except:
        return None
def checkMatch(match):
    try:
        statusRequestsURL = 'https://open.faceit.com/data/v4/matches/' + match[36:]
        requestStatus = requests.get(statusRequestsURL, headers = headers)
        statusDeets = requestStatus.json()
        hubID = json.dumps(statusDeets['competition_id'], indent=2).replace('"','')
        status = json.dumps(statusDeets['status'], indent=2)
        map = getMap(statusDeets)

        return status, hubID, map
    except:
        return None, None, None

def determineChannel(hub):
    hubDict = {'bed6a13f-6aa3-4d01-839f-b83a9d26c589':736603132796076212, '627e10d3-00ac-4376-9f62-a22812e220b1':735918664053948478,
               'e244b64a-2a54-43a2-8a0e-df2380a8c1cc':736741005713342485, 'e7ee1bc8-2be1-4512-955e-5542daae4152':736741005713342485,
               '73b8f93e-6a49-4abd-90e7-71caa4735c04':736741005713342485, '89b35fc4-cc30-4966-842e-9d5d3a47d09c':736790825123708948,
               '210f559a-1140-46d6-8442-def647daad5d':736790825123708948}
    if hub in hubDict:
        channelID2 = hubDict[hub]
        channelID = client.get_channel(channelID2)
        return channelID, channelID2


matchDictionary = {}


def getMessageID(matchDictionary, match):
    ID = matchDictionary[match]
    return ID



@client.event
async def on_ready():
    print('READY')



def getPlayerID(username):
    requestPlayerURL = 'https://open.faceit.com/data/v4/players?nickname='+username+'&game=COUNTER%20STRIKE%3A%20GLOBAL%20OFFENSIVE'
    requestPlayerStats = requests.get(requestPlayerURL, headers=headers)
    statDeets = requestPlayerStats.json()
    elo = json.dumps(statDeets['games']['csgo']['faceit_elo'], indent=2).replace('"','')
    level = json.dumps(statDeets['games']['csgo']['skill_level'], indent=2).replace('"', '')
    playerID = json.dumps(statDeets['player_id'], indent=2).replace('"', '')
    return playerID,elo,level


def getPlayerStats(username):
    try :
        playerID,elo,level = getPlayerID(username)
        requestPlayerURL = 'https://open.faceit.com/data/v4/players/'+playerID+'/stats/csgo'
        requestPlayerStats = requests.get(requestPlayerURL, headers=headers)
        statDeets = requestPlayerStats.json()
        kd = json.dumps(statDeets['lifetime']['Average K/D Ratio'],indent=2)
        winrate = json.dumps(statDeets['lifetime']['Win Rate %'],indent=2)
        return kd,elo,level,winrate
    except :
        return Null


def makePlayerEmbed(colour,kd,elo,img,winrate,username):
    username.replace('"','')
    kd.replace('"','')
    playerEmbed = discord.Embed(title="  ", description="Elo : "+elo, color=colour)
    playerEmbed.set_thumbnail(url="https://cdn-images-1.medium.com/max/816/1*PwN-Y2RzTdVo2e2wlPv0SQ@2x.png")
    playerEmbed.set_author(name=username+"'s stats",url="https://www.faceit.com/en/players/"+username, icon_url = img)
    playerEmbed.add_field(name="Average K/D", value=kd, inline=True)
    playerEmbed.add_field(name="Win Rate %", value=winrate.replace('"','')+"%", inline=True)
    playerEmbed.set_footer(text="Faceit Stats Tracker by Krang")
    return playerEmbed


def calculateElo(playerList1,playerList2):
    totalEloA = 0
    totalEloB = 0

    for player in playerList1:
        requestPlayerURL = 'https://open.faceit.com/data/v4/players?nickname=' + player.replace('"', '') + '&game=COUNTER%20STRIKE%3A%20GLOBAL%20OFFENSIVE'
        requestPlayerStats = requests.get(requestPlayerURL, headers=headers)
        statDeets = requestPlayerStats.json()
        playerElo = int(json.dumps(statDeets['games']['csgo']['faceit_elo'], indent=2).replace('"', ''))
        totalEloA += playerElo
        avgEloA = totalEloA / 5

    for player in playerList2:
        requestPlayerURL = 'https://open.faceit.com/data/v4/players?nickname=' + player.replace('"', '') + '&game=COUNTER%20STRIKE%3A%20GLOBAL%20OFFENSIVE'
        requestPlayerStats = requests.get(requestPlayerURL, headers=headers)
        statDeets = requestPlayerStats.json()
        playerElo = int(json.dumps(statDeets['games']['csgo']['faceit_elo'], indent=2).replace('"', ''))
        totalEloB += playerElo
        avgEloB = totalEloB /5

    eloDiff = avgEloB - avgEloA
    percent = 1 / (1 + math.pow(10, eloDiff / 400))

    eloWonA = round(50 * (1 - percent))
    eloLostA = round(50 * (0 - percent))

    eloLostB = -(round(50 * (1 - percent)))
    eloWonB = -(round(50 * (0 - percent)))

    return str(eloWonA), str(eloLostA), str(eloWonB), str(eloLostB)


@client.command()
async def yalla(ctx):
    if ctx.channel.id == 736603132796076212:
        hubList = ['bed6a13f-6aa3-4d01-839f-b83a9d26c589', '627e10d3-00ac-4376-9f62-a22812e220b1',
                   'e244b64a-2a54-43a2-8a0e-df2380a8c1cc', 'e7ee1bc8-2be1-4512-955e-5542daae4152',
                   '73b8f93e-6a49-4abd-90e7-71caa4735c04', '89b35fc4-cc30-4966-842e-9d5d3a47d09c',
                   '210f559a-1140-46d6-8442-def647daad5d']
        loopCount = 0
        logChannel = client.get_channel(737581188893638666)
        while True:
            try:
                for hub in hubList:
                    matchList = liveGames(headers, params, hub)
                    channelID, channelID2 = determineChannel(hub)
                    if 0 <= loopCount <= 4:
                        await channelID.purge(limit=30)
                        print('NUKED ' + str(channelID))

                    else:
                        for match in matchList:
                            status, hubID, map = checkMatch(match)
                            if status != '"CANCELLED"' and status != '"FINISHED"' and map != None and match not in postedMatches:
                                playerList1, playerList2 = getPlayers(match)
                                eloWonA, eloLostA, eloWonB, eloLostB = calculateElo(playerList1,playerList2)
                                map = map.replace('"', '').replace('[', '').replace(']', '')
                                embed = makeEmbed(playerList1, playerList2, match, map, eloWonA, eloLostA, eloWonB, eloLostB)
                                embedMSG = await channelID.send(embed=embed)
                                embedID = embedMSG.id
                                postedMatches.append(match)
                                matchDictionary[match] = embedID
                                ID = getMessageID(matchDictionary, match)
                                sent = 'STARTED ' + ':' + str(ID) + ' + ' + match + ' + ' + status + ' IN ' + str(channelID)
                                await logChannel.send(sent)


                    for game in postedMatches:
                        status, hubID, map = checkMatch(game)
                        if status == '"CANCELLED"' or status == '"FINISHED"':
                            ID = getMessageID(matchDictionary, game)
                            IDChannel, IDChannel2 = determineChannel(hubID)
                            await client.http.delete_message(IDChannel2, ID)
                            postedMatches.remove(game)
                            matchDictionary.pop(game)
                            message = 'DELETED ' + ':' + str(ID) + ' + ' + game + ' + ' + status + ' from ' + str(IDChannel)
                            await client.send_message(737581188893638666,message)
                    loopCount += 1
            except :
                continue





client.run("discordAPIKEY")



