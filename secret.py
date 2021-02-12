import discord
from discord.ext import commands
from replit import db


class secret(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Secret_Command', 'secret_command'], hidden=True)
    async def secret(self, ctx, message=None):

        description = 'Secret Message'
        embed = discord.Embed(title='SECRET TITLE', colour=discord.Colour(
            0xE5E242), description=description)

        embed.set_image(
            url="https://images.pexels.com/photos/3156660/pexels-photo-3156660.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500")
        embed.set_thumbnail(url=ctx.message.author.avatar_url_as(size=64))

        await ctx.send(embed=embed)

    @commands.Cog.listener("on_message")
    async def rankdoor(self, message):

        if message.author.bot:
            return

        add_exp(message.author.id)

        exp, lvl = get_stats(message.author.id)

        # Check for level promotion
        if exp in level_check_point:
            update_level(message.author.id)
            await message.channel.send(f'Congratulations {message.author} You are now level {lvl}!!!')
        print(
            f'Message heard from {message.author.id}\t{message.author.name}\t{message.channel.name}')
        print(f'--- {message.author.name} has {exp} points and is level {lvl}---')

    @commands.command(aliases=['restart_db', 'nuke_db'], hidden=True)
    async def delete_db(self, ctx):
        if ctx.message.author.id in masters:
            nuke_db()
            await ctx.send(f'*Explosion Noises* What have you done {ctx.message.author.name}?')
        else:
            await ctx.send(f'You do not have that power {ctx.message.author.name}')
        return

    @commands.command(aliases=['rank', 'lvl', 'level'], hidden=True)
    async def level_request(self, ctx, member: discord.Member = None):

        if not member:  # Command user requests own info
            exp, lvl = get_stats(ctx.author.id)

            embed = discord.Embed(title='Level {}'.format(
                lvl), description=f"{exp} XP ", color=discord.Color.green())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

        else:  # Command user requests info on someone else
            # Creates a user in db with 0 xp
            if member.id not in db.keys():
                db[member.id] = '0,0'

            exp, lvl = get_stats(member.id)
            lvl = user_level(exp)
            embed = discord.Embed(title='Level {}'.format(
                lvl), description=f"{exp} XP", color=discord.Color.green())
            embed.set_author(name=member, icon_url=member.avatar_url)

            await ctx.send(embed=embed)


# Helper functions below
def add_exp(id):
    if id in db.keys():
        exp, lvl = db[id].split(',')
        db[id] = f'{str(int(exp)+5)},{lvl}'
    else:
        db[id] = '5,0'


def user_level(exp):
    lvl = 0
    for index, num in enumerate(level_check_point):
        if exp >= num:
            lvl = index+1
    return lvl


def update_level(id):
    if not id:  # No id given
        return

    if id not in db.keys():  # id not in db
        db[id] = '0,0'

    exp, lvl = db[id].split(',')
    lvl = str(user_level(int(exp)))
    db[id] = f'{exp},{lvl}'


def get_stats(id=None):
    if not id:
        return 0, 0

    if id not in db.keys():
        db[id] = '0,0'

    exp, lvl = db[id].split(',')
    return int(exp), int(lvl)


def nuke_db():
    for k in db.keys():
        if k != 'encouragements':
            del db[k]
    print('Invoking NUKE function')
    return


# level_check_point = [100, 200, 500, 700, 900, 1100,1300, 1500, 1800, 2300, 2700, 3100, 3700, 4300, 5000]
level_check_point = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 1000]
masters = [793433316258480128, 790459205038506055]


def setup(client):

    client.add_cog(secret(client))
