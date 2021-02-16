import os
import discord
from discord.ext import commands
import sqlite3


class CCguild():
    def __init__(self, guildid, name='Not Set', home=0, listen=0):
        self.guildid = guildid
        self.name = name
        self.home = home
        self.listen = listen

    def __str__(self):
        return f'CCguild object, UserID={self.id}'


class CCuser():
    def __init__(self, guildid, userid, name='No Name', exp=0, lvl=0, msgcount=0):
        self.guildid = guildid
        self.id = userid
        self.name = name
        self.exp = exp
        self.level = lvl
        self.msgcount = msgcount

    def __str__(self):
        return f'CCuser object, UserID={self.id}'


class dbstuff(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['listexp', 'list_exp'], hidden=False)
    async def make_exp_list(self, ctx, qty=3):
        if ctx.message.author.id not in [793433316258480128, 790459205038506055]:
            await ctx.send(f'You are not authorized to run this command {ctx.message.author.id}')
            return

        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title='SECRET TITLE', colour=discord.Colour(
            0xE5E242), description='\<description in embed\>')

        embed.set_image(
            url="https://images.pexels.com/photos/1148820/pexels-photo-1148820.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260")

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        # adds a field name for each result in query
        for index, record in enumerate(get_data(qty)):
            embed.add_field(
                name=f"Field {index + 1} Title", value=record, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['myguilds', 'my_guilds'], hidden=False)
    async def list_guilds(self, ctx):
        if ctx.message.author.id not in [793433316258480128, 790459205038506055]:
            await ctx.send(f'You are not authorized to run this command {ctx.message.author.id}')
            return

        temp_txt, index = '', 0
        async for guild in self.client.fetch_guilds(limit=150):
            index += 1
            temp_txt = temp_txt + f'**{index})** {guild.name}\n'
        embed = discord.Embed(title=f"{self.client.user.display_name}\'s Guilds", colour=discord.Colour(
            0xE5E242), description=temp_txt)

        embed.set_image(
            url="https://images.pexels.com/photos/461049/pexels-photo-461049.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260")

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)


'''
    async def db_populate_guilds(self):
        print('My guilds : ', end='')
        async for guild in self.client.fetch_guilds(limit=150):
            print(f'{guild.name}')
'''


def get_data(qty=2):
    my_fake_data = ['Fake Person 1 with 10 exp',
                    'Fake Person 2 with 250 exp', 'Fake Person 3 with 305 exp']
    return my_fake_data

# SQLite Database Stuff


# Creates connection to db in current directory
# conn = sqlite3.connect('cupcake.db')
# Creates a cursor
# c = conn.cursor()
'''
# Create a table (run once)
c.execute("""CREATE TABLE "users" (
	"ID"	integer,
	"NAME"	text DEFAULT 'No Name',
	"EXP"	integer DEFAULT 0,
	"LEVEL"	INTEGER DEFAULT 0,
	PRIMARY KEY("ID")
)""")
# Add A Record
c.execute("INSERT INTO users VALUES(1001,'Steve',100)")

# Retrieve Information
# c.execute("SELECT * FROM users")
# options are fetchone / fetchmany(num) / fetchall
# c.fetchall()

# Commit our changes
conn.commit()



def new_user(guildid, userid, name):
    with conn:
        pass


def new_guild(guild):
    with conn:
        pass
'''


def guild_exists(guildid):
    # with conn:
    return f'Checking for guild {guildid} in db'

# Close database connection
# conn.close()

# Cog setup command


def setup(client):
    client.add_cog(dbstuff(client))
