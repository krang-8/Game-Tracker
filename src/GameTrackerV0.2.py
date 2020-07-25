import requests
import json
import discord
from discord.ext import commands
from Screenshot import Screenshot_Clipping
from selenium import webdriver
import time
from PIL import Image


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
    playerList1 = []
    playerList2 = []
    factionList = ['faction1', 'faction2']

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
                for faction in factionList:
                    for count in range(0, 5):
                        player = json.dumps(
                            matchDeets[packageName][COUNTER]['teams'][faction]['roster'][count]['nickname'],indent=2).replace('"', '')
                        if faction == 'faction1':
                            if player not in playerList1:
                                playerList1.append(player)
                        if faction == 'faction2':
                            if player not in playerList2:
                                playerList2.append(player)
                matchLink = "https://www.faceit.com/en/csgo/room/"+matchPackage
                fixedMatchLink = matchLink.replace('"', '')

                if fixedMatchLink not in matchList :
                    matchList.append(fixedMatchLink)


                COUNTER += 1
            except:
                testVar = False


    return matchList, playerList1, playerList2



def screenshotMatchpage(match):
    ob = Screenshot_Clipping.Screenshot()
    driver = webdriver.Chrome('E:\chromedriver.exe')
    url = match
    driver.get(url)
    time.sleep(1)
    submit_button = driver.find_elements_by_xpath('/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/button[2]')[0]
    submit_button.click()
    img_url = ob.full_Screenshot(driver, save_path=r'C:\Users\krang\Desktop\matches', image_name='Myimage.png')
    driver.close()
    driver.quit()
    im = Image.open(r'C:\Users\krang\Desktop\matches\myImage.png')
    cropped = im.crop((0, 150, 928, 600))
    cropped.save(r'C:\Users\krang\Desktop\matches\myImage.png')

client = discord.Client()

postedMatches = []

def splitPlayers(playerList1,playerList2):
    teamListA =[]
    teamListB =[]
    teamListA = playerList1[0:5]
    teamListB = playerList2[0:5]
    del playerList1[:5]
    del playerList2[:5]

    return teamListA, teamListB




@client.event
async def on_ready():
    channelID = client.get_channel(735918664053948478)
    while True:
        matchList,playerList1,playerList2 = liveGames(headers,params)
        for match in matchList:
            if match not in postedMatches:
                teamListA, teamListB = splitPlayers(playerList1,playerList2)
                embed = discord.Embed(title="Live Game",description="Map Name", color = 0xff5500)
                embed.set_author(name="MATCH",url=match, icon_url = "https://pbs.twimg.com/profile_images/1262464144802013184/BHLstW-J_400x400.jpg")
                embed.add_field(name="Team A" + "             ", value= teamListA[0] + '\n' + teamListA[1] + '\n' + teamListA[2] + '\n' + teamListA[3] + '\n' + teamListA[4] , inline=True)
                embed.add_field(name="               " + "Team B", value=teamListB[0] + '\n' + teamListB[1] + '\n' + teamListB[2] + '\n' + teamListB[3] + '\n' + teamListB[4], inline=True)
                embed.set_footer(text="MESL Tracker made by Krang")
                embed.set_image(url='https://media.discordapp.net/attachments/735918664053948478/736380111665889350/Webp.net-resizeimage_13.png')
                await channelID.send(embed=embed)
                postedMatches.append(match)
            ### Following else statement will be implemented later, it is about deleting messages of matches that are no longer ongoing.
            #else:
                # check match status using API
                # if status is ongoing, pass
                # else, delete message from discord
        time.sleep(60)

client.run("discordAPIKEY)


