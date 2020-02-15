import argparse
import asyncio
import json
import random

import discord
from discord.ext import commands
from mcstatus import MinecraftServer

parser = argparse.ArgumentParser()
parser.add_argument('-ip', '--ip', help="the address of a minecraft server", default='localhost')
parser.add_argument('-p', '--port', help="the port of a minecraft server", default='25565')
args = parser.parse_args()

IP = args.ip
PORT = args.port

bot = commands.Bot(command_prefix='?')

async def update_status():
    """
    this function uses mcstatus to get the amount of 
    players on the server and change the discord bot's 
    status to the amount online / max amount of players
    """
    await bot.wait_until_ready()

    while True:
        try:
            server = MinecraftServer.lookup(f"{IP}:{PORT}")
            server_status = server.status()
            
            # set the status to online
            status = discord.Status.online
            activity = discord.Game(name=f": {server_status.players.online}/{server_status.players.max}")

        except Exception as e:
            status = discord.Status.do_not_disturb
            activity = discord.Game(name="Server Offline")

        # pushing the new status and activity
        await bot.change_presence(
            status=status,
            activity=activity
        )

        await asyncio.sleep(30)

# running update_status in the background
bot.loop.create_task(update_status())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def players(ctx):
    """
    sends a message in the chat with the current/max players and a list of those players' names
    """
    try:
        server = MinecraftServer.lookup(f"{IP}:{PORT}")
        status = server.status()

        # if nobody is online, sample will not appear. this makes it default to an empty list
        player_list = status.raw['players'].get('sample', [])

        # each player has a dict of player_id and name.
        player_names = [p['name'] for p in player_list]

        embed = discord.Embed(
            title=f"{status.players.online}/{status.players.max} players online",
            description="\n".join(player_names),
            color=discord.Color.from_rgb(107, 181, 124)
        )

    except:
        embed = discord.Embed(
            title=f"Server Offline 😔",
            description="OOPSIE WOOPSIE!!",
            color=discord.Color.from_rgb(107, 181, 124)
        )

    await ctx.send(embed=embed)

# loading credentials
creds = json.load(open("./credentials.json"))

bot.run(creds["discord_secret_key"])
