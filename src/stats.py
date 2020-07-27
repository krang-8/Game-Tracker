import requests
import json
import discord
from discord.ext import commands



client = commands.Bot(command_prefix = ".")


headers = {
        'accept': 'application/json',
        'Authorization': 'Bearer FACEIT APIKEY',
    }

params = (
        ('type', 'ongoing'),
        ('offset', '0'),
        ('limit', '20'),
    )



playerList1 = []
playerList2 = []


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
    playerEmbed.add_field(name="Average K/D", value=kd.replace('"',''), inline=True)
    playerEmbed.add_field(name="Win Rate %", value=winrate.replace('"','')+"%", inline=True)
    playerEmbed.set_footer(text="Faceit Stats Tracker by Krang")
    return playerEmbed



@client.command()
async def stats(ctx, *,arg=None):

    if ctx.channel.id == 737212408489181265:
        if arg ==None:
            await ctx.channel.send("You forgot to enter a username")
        else:
            try:
                kd,elo,level,winrate = getPlayerStats(arg)
                if level == 1 :
                    img = 'https://media.discordapp.net/attachments/736790825123708948/736938274664218700/images-removebg-preview.png'
                    playerEmbed =makePlayerEmbed(0xeeeded,kd,elo,img,winrate,arg)
                    await ctx.channel.send(embed=playerEmbed)
                elif level == '2' or level == '3' :
                    if level == '2' :
                        img = 'https://media.discordapp.net/attachments/736790825123708948/736938276354523146/images__1_-removebg-preview.png'
                        playerEmbed = makePlayerEmbed(0x27e10e, kd, elo, img, winrate, arg)

                    elif level =='3' :
                        img = 'https://media.discordapp.net/attachments/736790825123708948/736938261716664350/images__2_-removebg-preview.png'
                        playerEmbed = makePlayerEmbed(0x27e10e,kd,elo,img,winrate,arg)

                    await ctx.channel.send(embed=playerEmbed)

                elif level =='4' or level == '5' or level == '6' or level == '7':
                    if level == '4' :
                        img = 'https://media.discordapp.net/attachments/736790825123708948/736938264157487154/download-removebg-preview_1.png'
                        playerEmbed = makePlayerEmbed(0xf9f10b, kd, elo, img, winrate, arg)

                    elif level == '5' :
                        img = 'https://media.discordapp.net/attachments/736790825123708948/736938265873219644/images__3_-removebg-preview.png'
                        playerEmbed = makePlayerEmbed(0xf9f10b, kd, elo, img, winrate, arg)

                    elif level == '6' :
                        img = 'https://media.discordapp.net/attachments/736790825123708948/736938267051819039/download__2_-removebg-preview.png'
                        playerEmbed = makePlayerEmbed(0xf9f10b, kd, elo, img, winrate, arg)

                    elif level == '7' :
                        img = 'https://media.discordapp.net/attachments/736790825123708948/736938268855238666/download__3_-removebg-preview.png'
                        playerEmbed = makePlayerEmbed(0xf9f10b, kd, elo, img, winrate, arg)

                    await ctx.channel.send(embed=playerEmbed)

                elif level == '8' or level == '9' :
                    if level == '8' :
                        img = 'https://media.discordapp.net/attachments/736790825123708948/736938270197284986/images__4_-removebg-preview.png'
                        playerEmbed = makePlayerEmbed(0xca6302, kd, elo, img, winrate, arg)
                    elif level == '9' :
                        img = 'https://media.discordapp.net/attachments/736790825123708948/736938271678136400/download__1_-removebg-preview.png'
                        playerEmbed = makePlayerEmbed(0xca6302, kd, elo, img, winrate, arg)

                    await ctx.channel.send(embed=playerEmbed)

                elif level == '10' :
                    img = 'https://media.discordapp.net/attachments/736790825123708948/736938274333130822/ap_550x550_12x12_1_transparent_t-removebg-preview.png'
                    playerEmbed = makePlayerEmbed(0xe90101, kd, elo, img, winrate, arg)
                    await ctx.channel.send(embed=playerEmbed)
            except :
                await ctx.channel.send('No player exists with username ' + str(arg))
    else:
        await ctx.channel.send("Please use the stats channel to use this command")


client.run("DiscordAPIKEY")

