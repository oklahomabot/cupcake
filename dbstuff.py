import discord
from discord.ext import commands
import sqlite3


class CCguild():
    def __init__(self, id, name='Not Set', home=0, owner='Not Saved', listen=0):
        self.id = id
        self.name = name
        self.home = home
        self.owner = owner
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

    '''
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
    '''

    @commands.command(aliases=['myguilds', 'my_guilds'], hidden=False)
    async def list_guilds(self, ctx):
        if ctx.message.author.id not in [793433316258480128, 790459205038506055]:
            await ctx.send(f'You are not authorized to run this command {ctx.message.author.id}')
            return

        temp_txt, index = '', 0
        async for guild in self.client.fetch_guilds(limit=150):
            index += 1
            temp_txt = temp_txt + \
                f'**{index})** {guild.name}\n'
        embed = discord.Embed(title=f"{self.client.user.display_name}\'s Guilds", colour=discord.Colour(
            0xE5E242), description=temp_txt)

        embed.set_image(
            url="https://images.pexels.com/photos/461049/pexels-photo-461049.jpeg?auto=compress&cs=tinysrgb&dpr=3&h=750&w=1260")

        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=['finduser', 'userexists'], hidden=True)
    async def dbfinduser(self, ctx, user: discord.User = None):
        if ctx.message.author.id not in [793433316258480128, 790459205038506055]:
            await ctx.send(f'You are not authorized to run this command {ctx.message.author.id}')
            return

        if not user:
            user = ctx.message.author

        if user_exists(ctx.guild.id, user.id):
            info = get_user(ctx.guild.id, user.id)
            embed = discord.Embed(
                title='Userinfo', description=f'misc. info about {user.name} in {ctx.guild}', colour=discord.Colour.blue())
            temp = ''
            temp = ((f'- ID: {user.id}\n') +
                    (f'- MsgCount: {info.msgcount}\n') +
                    (f'- Exp Points: {info.exp}\n') +
                    (f'- Exp Level: {info.level}\n') +
                    ('- Is User a bot?: '))
            temp = temp + ('YES' if user.bot else 'NO')
            embed.add_field(name=user, value=temp)
            if user.avatar is not None:
                embed.set_thumbnail(url=user.avatar_url_as(size=64))

            await ctx.send(':mag:', embed=embed)
        else:
            await ctx.send(f'Looked for {user.name} on server {ctx.guild.name} : result - RECORD NOT FOUND in db')

    @commands.Cog.listener("on_message")
    async def msgcount(self, message):
        if message.author == self.client or message.author.bot:
            return

        if not user_exists(message.guild.id, message.author.id):
            # make new user
            tmpuser = CCuser(message.guild.id,
                             message.author.id, name=message.author.name)
            add_new_user(tmpuser)

        # perform per message activities (exp/level/msgcount)
        tmpuser = get_user(message.guild.id, message.author.id)
        tmpuser.msgcount += 1
        # check for exp level promotion
        if exp_level(tmpuser.level+1) - tmpuser.exp <= 5:
            tmpuser.level += 1
            await message.channel.send(
                f'Congratulations {message.author.name}! You have promoted to exp level {tmpuser.level +1}')
        tmpuser.exp += 5
        save_user(tmpuser)
        print(
            f'User {message.author.name} in guild {message.guild} sent a message')

# Helper Functions


def exp_level(level=0):
    '''
    Returns base exp value for exp level
    '''
    level_dic = {0: 0, 1: 100, 2: 220, 3: 350, 4: 500, 5: 675, 6: 875,
                 7: 1125, 8: 1450, 9: 1850, 10: 2600, 11: 3600, 12: 10000, 13: 1000000}
    return level_dic[level]


# SQLite Database Stuff
# Creates connection to db in current directory
conn = sqlite3.connect('cupcake.db')
# Creates a cursor
c = conn.cursor()
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

'''


def user_exists(guildID, userID):
    # returns boolean if guild/user record found in db table users
    with conn:
        c.execute(
            f"SELECT COUNT(*) from users WHERE guildID={guildID} AND userID={userID}")
        if c.fetchone()[0] >= 1:
            return True
        else:
            return False


def add_guild_if_new(g: CCguild):
    with conn:
        text = f"INSERT OR IGNORE INTO guilds VALUES (?, ?, ?, ?, ?)"
        c.execute(text, (g.id, g.name, g.home, g.owner, g.listen))


def get_user(guildID=None, userID=None):
    # returns CCuser object from db data
    # creates record if non exists
    with conn:
        c.execute(
            f"SELECT * from users WHERE guildID={guildID} AND userID={userID}")
        result = c.fetchone()
        CCuserOBJECT = CCuser(result[0], result[1],
                              result[2], result[3], result[4], result[5])
        return CCuserOBJECT


def add_new_user(user: CCuser):
    with conn:
        text = f"INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?, ?)"
        c.execute(text, (user.guildid, user.id, str(user.name), user.exp,
                         user.level, user.msgcount))


def save_user(user: CCuser):
    # takes CCuser object and updates db
    with conn:
        text = f'UPDATE users SET guildID = {user.guildid}, userID = {user.id}, name = \"{user.name}\",'
        text = text + \
            f'exp = {user.exp}, explevel = {user.level}, msgcount = {user.msgcount} '
        text = text + f'WHERE guildID = {user.guildid} AND userID = {user.id}'
        # print('save_user UPDATING db')
        # print(text)
        c.execute(text)


# Close database connection
# conn.close()

# Cog setup command


def setup(client):
    client.add_cog(dbstuff(client))
