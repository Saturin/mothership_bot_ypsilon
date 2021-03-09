import discord
from Ypsilon import Ypsilon

_TOKEN = 'ODE4MTI2MDEwMTU1NDAxMjI4.YEThOA.RSkpdMzQ7yppmxcRH9RffanmRFo'
client = discord.Client()
_TERMINAL_START_CALL = '$station'
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    y = Ypsilon(str(message.content))
    if message.author == client.user:
        return

    if message.content.startswith(_TERMINAL_START_CALL):
        await message.channel.send(y.action())
client.run(_TOKEN)