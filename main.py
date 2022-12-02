import discord
import requests
import json
import pandas as pd
import time
from models import Member
import datetime

#saving last request so multiple requests aren't made in a short period of time
last_req = datetime.datetime.fromtimestamp(0)
members = []

#get data from AoC and populate members list
def get_data():
    global last_req
    ct = datetime.datetime.now()
    if ((ct - last_req).total_seconds() < 30):
        return
    else:
        last_req = ct

    print("Sending AOC API request...")
    r = requests.get(leaderboard_url, cookies=cookies)
    json_data = r.text

    #use this for testing so you're not spamming them with requests
    """
    json_file = open("sample.json", "r")
    json_data = json_file.read().replace('\n','')
    """

    members.clear()
    df = pd.read_json(json_data)
    for k,v in enumerate(df.members):
        members.append(Member(v['name'], v['stars'], v['local_score'], v['completion_day_level']))

    members.sort(key=lambda h: (h.score, h.name))
    members.reverse()

#prints scoreboard for the defined leaderboard
def scoreboard():
    get_data()

    resp = ""
    resp += (f'{"Rank":<{10}}{"Name":<{30}}{"Score":<{10}}{"Stars":<{10}}{"Avg Time Between Parts (min)":<{30}}\n')
    for index, i in enumerate(members):
        if i.score > 0:
            resp += (f'{index+1:<{10}}{i.name:<{30}}{i.score:<{10}}{i.stars:<{10}}{i.average_pt_b:<{30}}\n')
    return resp

#prints a member of the leaderboard's daily stats
def stats(name):
    get_data()

    resp = ""
    for index,i in enumerate(members):
        if i.name == name:
            resp += "Name: {0}\nLeaderboard Rank: {1}\nLeaderboard Score: {2}\nStars: {3}\nAvg Time Between Parts (min): {4}\n\n".format(i.name, "{0}/{1}".format(index+1,len(members)), i.score, i.stars, i.average_pt_b)
            if len(i.day_score) > 0:
                resp += (f'{"Day":<{10}}{"Part 1":<{10}}{"Part 2":<{10}}{"Total":<{10}}\n')
                for j in i.day_score:
                    s = "12/{0}/2022 0:0:0".format(j.day)
                    pt_a_interval_sec = (j.pt_a_timestamp - (datetime.datetime.strptime(s, "%m/%d/%Y  %H:%M:%S"))).total_seconds()
                    pt_a_interval = "{:01d}:{:02d}".format(int(pt_a_interval_sec // 60), int(pt_a_interval_sec % 60))
                    if j.pt_b_timestamp != 0:
                        pt_b_interval_sec = j.pt_b_interval * 60
                        pt_b_interval = "{:01d}:{:02d}".format(int(pt_b_interval_sec // 60), int(pt_b_interval_sec % 60))
                        total_interval_sec = (j.pt_b_timestamp - (datetime.datetime.strptime(s, "%m/%d/%Y  %H:%M:%S"))).total_seconds()
                        total_interval = "{:01d}:{:02d}".format(int(total_interval_sec // 60), int(total_interval_sec % 60))
                    else:
                        pt_b_interval = "--:--"
                        total_interval = "--:--"
                    resp += (f'{j.day:<{10}}{pt_a_interval:<{10}}{pt_b_interval:<{10}}{total_interval:<{10}}\n')
            break
    if resp == "": resp = "Are you sure you spelled that right?"
    return resp

#read leaderboard url from file
leaderboard_url_file = open("leaderboard_url.txt", "r")
leaderboard_url = leaderboard_url_file.read().replace('\n','')

#read session id from file
sesh_file = open("session.txt", "r")
sesh = sesh_file.read().replace('\n','')
cookies = {'session':sesh}

#read token from file
token_file = open("token.txt", "r")
token = token_file.read().replace('\n','')

#required bot stuff
intent = discord.Intents.default()
intent.members = True
intent.message_content = True
client = discord.Client(intents=intent)

@client.event
async def on_ready():
    print('We have logged in as {0.user}.format(client)')

@client.event
async def on_guild_join():
    await message.channel.send("I'm the AoC 2022 bot. Use '$scoreboard' to check the scoreboard or '$stats {aoc-name}' to check your stats.")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$stats'):
        splt = message.content.split()
        if len(splt) >= 2:
            resp = stats(" ".join(splt[1:]))
            await message.channel.send('```'+resp+'```')
        else:
            await message.channel.send('Invalid Input. Stats command syntax: $stats {name}')
    if message.content.startswith('$scoreboard'):
        resp = scoreboard()
        await message.channel.send('```'+resp+'```')

client.run(token)