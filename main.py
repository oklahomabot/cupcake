from dbstuff import CCguild, CCuser, add_guild_if_new
from secret import add_exp
import discord
import os
import random
from web import start_web
from discord.ext import commands
from dotenv import load_dotenv
import sqlite3


client = commands.Bot(command_prefix='cc-')

#cogs = ['bigmess', 'secret']
cogs = ['dbstuff']

# cog loader
for cog in cogs:
    try:
        client.load_extension(cog)
    except Exception as e:
        print(f'Could not load cog {cog}: {str(e)}')
    else:
        print(f'{cog} cog loaded')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # populate guilds in console for testing
    print('CupCake guilds :')
    async for guild in client.fetch_guilds(limit=150):
        tmp = CCguild(guild.id, name=guild.name)
        add_guild_if_new(tmp)
        print(
            f'Attempted to add {guild.name} : {guild.id} in db')


# start_web()
load_dotenv()
client.run(os.getenv('dTOKEN'))
