import random
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import requests
import os
import numpy as np
import youtube_dl
from youtube_search import YoutubeSearch


from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

url = "https://api.covid19india.org/data.json"

client = commands.Bot(command_prefix = "$")

def chunk(xs, n):
    out = []
    split = np.array_split(xs,n)
    for i in split:
        out.append(list(i))
    return out

@client.event
async def on_ready():
    print("Bot is ready")

@client.event
async def on_command_error(ctx,error):
    if isinstance(error, CommandNotFound):
        await ctx.send("That's not how you spell it dumbass")
        return
    raise(error)

# @client.command()
# async def join(ctx):
#     channel = ctx.message.author.voice.channel
#     print(channel.members)
#     # if(await channel.connect()):
#     #     print("Success")
@client.command()
async def online(ctx):
    online = []
    membersInServer = ctx.guild.members
    onlineMembersInServer = list(filter(filterOnlyOnlineMembers, membersInServer))
    onlineMembersCount = len(onlineMembersInServer)
    for member in onlineMembersInServer:
        online.append(member.name)
    await ctx.send(online)

@client.command()
async def cleps(ctx,*args):
 
    # await ctx.send("Sorry "+str(ctx.author.nick)+", Cleps is under construction at the moment please try again later")
    channel = ctx.message.author.voice.channel
    # players = ["aprbhd","jakesuli","wolfinthehouse","greybeard278","dobby","anishkasi"]
    players = []
    sitout = []
    membersInChannel = channel.members    
    # onlineMembersInServer = list(filter(filterOnlyOnlineMembers, membersInServer))
    for member in membersInChannel:
        if member.nick:
            players.append(member.nick.capitalize())
        else:
            players.append(member.name.capitalize())

    # name = str(ctx.author)
    # name = name.split("#")[0]

    if(args):
        n = int(args[0])

        if(n<=0):
            await ctx.send("STOP MESSING AROUND "+str(ctx.author.nick).split("#")[0].capitalize())

        if(n>len(players)):
            await ctx.send("Not enough players to group into "+str(n)+" teams")

        else:

            random.shuffle(players)
            ans = chunk(players,n)
            for i in range(len(ans)):
                await ctx.send("Team "+str(i+1)+ ":" +" "+' '.join(ans[i]))
    
    else:
        random.shuffle(players)
        ans = chunk(players,2)
        for i in range(len(ans)):
            await ctx.send("Team "+str(i+1)+ ":" +" "+' '.join(ans[i]))
    #end
    # if(len(args)>0):
    #     args = list(args)
    #     for s in args:
    #         sitout.append(s.lower())
    #         players.remove(s.lower())

    # random.shuffle(players)
    # n = len(players)
    # if(n>8):
    #     for i in range(n-8):
    #         sitout.append(players.pop())
    #     n = len(players)
    # team1 = players[0:int(n/2)]
    # team2 = players[int(n/2):n]
    # print(team1)
    # print(team2)
    # await ctx.send('TEAM1 - {}'.format(' '.join(team1)))
    # await ctx.send('TEAM2 - {}'.format(' '.join(team2)))
    # if(sitout):
    #     await ctx.send('SIT - {}'.format(' '.join(sitout)))
    #     print(sitout)


# @client.command()
# async def cleps3(ctx,*args):
#     channel = ctx.message.author.voice.channel
#     players = []
#     sit = []
#     membersInChannel = channel.members

#     for member in membersInChannel:
#         players.append(member.name.lower())

#     n = len(players)
    
#     random.shuffle(players)
#     team1 = players[0:3]
#     team2 = players[3:6]
#     team3 = players[6:n]

#     # if(n>9):
#     #     sit = players[9:n]

#     print(team1)
#     print(team2)
#     print(team3)

#     await ctx.send('TEAM1 - {}'.format(' '.join(team1)))
#     await ctx.send('TEAM2 - {}'.format(' '.join(team2)))
#     await ctx.send('TEAM3 - {}'.format(' '.join(team3)))
#     # if(sit):
#     #     await ctx.send('SIT - {}'.format(' '.join(sit)))
#     #     print(sit)



@client.command()
async def covid19(ctx):
    data = requests.get(url)
    data = data.json()
    data = data["statewise"][11]
    data = f'''#Total cases: {data["confirmed"]}
    |                                 |       Today       |       Total       |
    |---------------------|----------------|------------------|
    |       Active              |       {data["deltaconfirmed"]}         |       {int(data["active"])}       |
    |       Deaths            |        {data["deltadeaths"]}           |       {data["deaths"]}        |
    |       Recovered       |       {data["deltarecovered"]}         |       {data["recovered"]}     |
    '''
    print(data)
    await ctx.send(data)

@client.command()
async def randomneil(ctx):
    #channel = ctx.message.author.voice.channel
    folder = "/Users/gopuman/Neil/"
    files = os.listdir(folder)
    n = len(files)
    rando = random.randint(0,n)
    pick = folder+files[rando]
    await ctx.send(file=discord.File(pick))
    print("worked")
'''
@client.command()
async def lyrics(ctx,*args):
    if len(args)==0:
        await ctx.send("For which song da!!!")
    elif len(args)==1:
        url = "https://api.canarado.xyz/lyrics/"
        song = args[0]
        res = requests.get(url+song)
        res = res.json()
        if(res["status"]["code"]==200):
            lyrics = res["content"][0]["lyrics"]
            n = len(lyrics)
            for i in range(2000,n,2000):
                await ctx.send(' '.join(lyrics[0:]))
            await ctx.send(' '.join(lyrics[int(n/2):n]))
        else:
            await ctx.send("Lyrics not found :(")
    else:
        url = "https://api.canarado.xyz/lyrics/"
        song = " ".join(args)
        res = requests.get(url+song)
        res = res.json()
        if(res["status"]["code"]==200):
            lyrics = res["content"][0]["lyrics"]
            n = len(lyrics)
            await ctx.send(' '.join(lyrics[0:int(n/2)]))
            await ctx.send(' '.join(lyrics[int(n/2):n]))
        else:
            await ctx.send("Lyrics not found :(")
'''

@client.command(brief="Plays a single video, from a youtube URL")
async def play(ctx,*args):
    if len(args) == 0:
        await ctx.send("Which song to play?")
    if len(args)>1:
        searchterm = ' '.join(args)
        print(searchterm)
    elif len(args)==1:
        searchterm = args[0]
        print(searchterm)
    
    first_url = "https://www.youtube.com"
    results = YoutubeSearch(searchterm,max_results=10).to_json()
    res = eval(results)
    url = first_url + res['videos'][0]['url_suffix']

    channel = ctx.message.author.voice.channel
    vc = await channel.connect()
    #'format': 'bestaudio', 
    YDL_OPTIONS = {'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send("Now Playing: "  + res['videos'][0]['title'])
        vc.is_playing()
    else:
        await ctx.send("Already playing song")
        return








# def filterOnlyOnlineMembers(member):
#     return member.status != discord.Status.offline and not member.bot
#     # for user in ctx.guild.members:
#     #     if user.status != discord.Status.offline:e
#     #         print (user.name+"#"+user.discriminator)

# @client.event
# async def on_voice_state_update(before, after):
#     if before.voice.voice_channel is None and after.voice.voice_channel is not None:
#         for channel in before.server.channels:
#             if channel.name == 'general':
#                 await client.send_message(channel, "Howdy")

# @client.event
# async def on_voice_state_update(member, before, after):
#     if before.channel is None and after.channel is not None:
#         if after.channel.id == [YOUR_CHANNEL_ID]:
#             await member.guild.system_channel.send("Alarm!")

client.run('NzI1NjU0OTA5MzI4MDMxNzc2.Xv8hOg.IO6gIHQ337S-CW5ck9oX2M0L3-s')
#6757275
# DerpyBoy
# KennethCook
# JakeJake
# Lancinator
# mvp06
# jamerson