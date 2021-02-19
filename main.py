from dbstuff import CCguild, add_guild_if_new
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

prefix = 'cc-'
client = commands.Bot(command_prefix=prefix)

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


async def load_guilds():
    print('CupCake guilds :')
    async for guild in client.fetch_guilds(limit=150):
        tmp = CCguild(guild.id, name=guild.name)
        add_guild_if_new(tmp)
        print(f'Attempted to add {guild.name} : {guild.id} in db')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for cc- command"))
    await load_guilds()

# start_web()
load_dotenv()
client.run(os.getenv('dTOKEN'))
