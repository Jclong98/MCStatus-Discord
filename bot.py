import asyncio
import json

import discord
import requests


class MyClient(discord.Client):
    """
    a modified version of https://github.com/Rapptz/discord.py/blob/master/examples/background_task.py
    to keep track of a minecraft servers players
    """

    def __init__(self, ip="localhost", port="25565", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ip = ip
        self.port = port

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.update_player_count())

    async def on_ready(self):
        """happens when the bot is ready"""
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        
        # getting players and initially setting the status
        await self.get_players(ip=self.ip, port=self.port)

    async def update_player_count(self):
        """the background task being created and run in __init__()"""
        await self.wait_until_ready()

        # infinite loop
        while True:
            # every 60 seconds, get the amount of players on the server
            await self.get_players(ip=self.ip, port=self.port)
            await asyncio.sleep(60)

    async def get_players(self, ip="localhost", port="25565"):
        """
        a function to get the status of the server and display 
        the results as the client's activity

        parameters:
            ip (str): the ip of a minecraft server
            port (str): port of the server address
        """

        # parsing the api json into a dictionary
        r = requests.get(f"http://mcapi.us/server/status?ip={ip}&port={port}")
        server_dict = json.loads(r.text)

        activity = discord.CustomActivity(
            name="Server Offline"
        )

        # if the server is online, then the server is up
        if server_dict['online']:

            # if the server is online, get the current players
            current_players = server_dict['players']['now']
            max_players = server_dict['players']['max']

            # set the status to online
            status = discord.Status.online

            activity = discord.Game(
                name=f": {current_players}/{max_players}",
            )

        else:
            status = discord.Status.do_not_disturb
            activity = discord.Game(
                name="Server Offline"
            )

        # pushing the new status and activity
        await self.change_presence(
            status=status,
            activity=activity
        )


if __name__ == "__main__":
    
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-ip', '--ip', help="the address of a minecraft server", default='localhost')
    parser.add_argument('-p', '--port', help="the port of a minecraft server", default='25565')

    # loading credentials
    creds = json.load(open("./credentials.json"))

    args = parser.parse_args()

    client = MyClient(ip=args.ip, port=args.port)
    client.run(creds['discord_secret_key'])
