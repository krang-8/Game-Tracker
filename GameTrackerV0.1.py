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
        'Authorization': 'Bearer FACEITapiKEY',
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


@client.event
async def on_message(message):


    if message.content.find("!matches") != -1:
        matchList = liveGames(headers,params)
        for match in matchList:
            if match not in postedMatches:
                await message.channel.send(match)
                screenshotMatchpage(match)
                await message.channel.send(file=discord.File(r'C:\Users\krang\Desktop\matches\Myimage.png'))
                postedMatches.append(match)


    if message.content.find("!hello") != -1:
        await message.channel.send("Hi") # If the user says !hello we will send back hi

client.run("discordAPIKEY")
