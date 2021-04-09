import discord
import os
from StationMsg import StationMsg
from Ypsilon import Ypsilon

_TOKEN = os.getenv("TOKEN")
client = discord.Client()
_TERMINAL_START_CALL = '>'
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith(_TERMINAL_START_CALL):
        y = Ypsilon()
        response = y.action(message.content)

        if type(response) == list:
            for el in response:
                await message.channel.send(el)
        else:
            await message.channel.send(response)
client.run(_TOKEN)