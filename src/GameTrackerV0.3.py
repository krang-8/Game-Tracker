import requests
import json
import discord
from discord.ext import commands
import time



headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer faceitAPIKEY',
    }

params = (
        ('type', 'ongoing'),
        ('offset', '0'),
        ('limit', '20'),
    )

def liveGames(headers,params):


    hubList = ['bed6a13f-6aa3-4d01-839f-b83a9d26c589', '627e10d3-00ac-4376-9f62-a22812e220b1',
               'e244b64a-2a54-43a2-8a0e-df2380a8c1cc', 'e7ee1bc8-2be1-4512-955e-5542daae4152',
               '73b8f93e-6a49-4abd-90e7-71caa4735c04', '89b35fc4-cc30-4966-842e-9d5d3a47d09c']

    matchList = []


    for hub in hubList:

        requestURL = 'https://open.faceit.com/data/v4/hubs/' + hub + '/matches'
        response = requests.get(requestURL, headers=headers, params=params)
        matchDeets = response.json()
        packageName = "items"
        gameRoom = "match_id"
        players = ""

        matchPackage = json.dumps(matchDeets, indent = 2)
        testVar = True
        COUNTER = 0
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





client = discord.Client()

postedMatches = []

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


def getMap(match):
    teamRequestsURL = 'https://open.faceit.com/data/v4/matches/' + match[36:]
    requestMatch = requests.get(teamRequestsURL, headers = headers)
    mapDeets = requestMatch.json()
    try:
        map = json.dumps(mapDeets['voting']['map']['pick'])
        return map
    except:
        pass

def makeEmbed(playerList1,playerList2, match, map):
    embed = discord.Embed(title="Live Game", description=map, color=0xff5500)
    embed.set_author(name="MATCH", url=match,icon_url="https://pbs.twimg.com/profile_images/1262464144802013184/BHLstW-J_400x400.jpg")
    embed.add_field(name="Team A" + "             ",value=playerList1[0] + '\n' + playerList1[1] + '\n' + playerList1[2] + '\n' + playerList1[3] + '\n' + playerList1[4], inline=True)
    embed.add_field(name="               " + "Team B",value=playerList2[0] + '\n' + playerList2[1] + '\n' + playerList2[2] + '\n' + playerList2[3] + '\n' + playerList2[4], inline=True)
    embed.set_footer(text="MESL Tracker made by Krang")
    embed.set_image(url='https://media.discordapp.net/attachments/735918664053948478/736380111665889350/Webp.net-resizeimage_13.png')
    return embed





@client.event
async def on_ready():
    channelID = client.get_channel(735918664053948478)
    while True:
        matchList= liveGames(headers,params)
        for match in matchList:
            map = getMap(match)
            if map != None:
                map = map.replace('"','').replace('[','').replace(']','')
                if match not in postedMatches:
                    playerList1,playerList2 = getPlayers(match)
                    embed = makeEmbed(playerList1,playerList2,match,map)
                    await channelID.send(embed=embed)
                    postedMatches.append(match)
                ### Following else statement will be implemented later, it is about deleting messages of matches that are no longer ongoing.
                #else:
                    # check match status using API
                    # if status is ongoing, pass
                    # else, delete message from discord

client.run("discordAPIKEY")


