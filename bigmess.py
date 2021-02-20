import discord
from discord.ext import commands
from replit import db
import requests
import json
import random
from web import start_web


class AllOrders(commands.Cog):

    def __init__(self, client):

        self.client = client
        if 'responding' in db.keys():
            self.responding = db['responding']
        else:
            self.responding = False
    '''
    @commands.command()
    async def on_command(ctx):
      server = ctx.guild.name
      user = ctx.author
      command = ctx.command
      await start_web(f'{server} \t {user} \t {command}')
    '''
    @commands.command()
    async def inspire(self, ctx):
        quote = get_quote()
        await ctx.send(quote)

    @commands.command()
    async def new(self, ctx, *, new_words):
        update_encouragements(new_words)
        await ctx.send("New encouraging message created")

    @commands.command()
    async def remove(self, ctx, index):
        encouragements = []
        temp_txt = ''
        if 'encouragements' in db.keys():
            encouragements = db['encouragements']
            if encouragements:
                try:
                    index = int(index)
                    delete_encouragements(index)
                    encouragements = db['encouragements']
                    temp_txt = (
                        f'user created encouragements now include: {(" + ").join(encouragements)}')
                except:
                    temp_txt = (
                        'Something went wrong. Did you include an index number (starts at 0.)')
            else:
                temp_txt = ('Empty List : Add some using the "new" command')
        else:
            temp_txt = (
                'There is no list called "encouragements" in my memory')

        await ctx.send(temp_txt)

    @commands.command()
    async def sadwords(self, ctx):
        await ctx.send(sad_words)

    @commands.command()
    async def list(self, ctx):
        encouragements = []
        temp_txt = ('We do not have any user added encouraging messages saved')
        if 'encouragements' in db.keys():
            encouragements = db['encouragements']
            if len(encouragements) != 0:
                temp_txt = (
                    f'user created encouragements include: {(" + ").join(encouragements)}')
        await ctx.send(temp_txt)

    @commands.command()
    async def status(self, ctx):
        if self.responding:
            await ctx.send('I am listening')
        else:
            await ctx.send('I am distracted right now')

    @commands.command()
    async def listen(self, ctx, cmd):

        if cmd.lower() in ['true', 'on']:
            db['responding'] = True
            self.responding = True
            await ctx.send('RESPONDING is ON')
        elif cmd.lower() in ['false', 'off']:
            db['responding'] = False
            self.responding = False
            await ctx.send('RESPONDING is OFF')
        else:
            await ctx.send(f'STATUS unchanged, RESPONDING = {db["responding"]}')

    @commands.command()
    async def userinfo(self, ctx, user: discord.User = None):
        temp = ''
        if user is None:
            await ctx.send('Please provide a user to get info')
            return
        temp = ((f'- User\'s ID: {user.id}\n') +
                (f'- User\'s discrim: {user.discriminator}\n') +
                ('- Is User a bot?: '))
        temp = temp + ('YES' if user.bot else 'NO')

        embed = discord.Embed(
            title='Userinfo', description=f'misc. info about {user.name}', colour=discord.Colour.blue())

        embed.add_field(name=user, value=temp)
        if user.avatar is not None:
            embed.set_thumbnail(url=user.avatar_url_as(size=64))

        await ctx.send(':mag:', embed=embed)

    @commands.command()
    # passing ctx is context and is required
    # it has such information as message ...
    async def ping(self, ctx):
        '''
        I'll play
        '''
        # await is used with async to prevent blocking simple
        # processes by allowing others to continue
        await ctx.send(f'Pong: {round(self.client.latency*1000)}ms')

    @commands.Cog.listener("on_message")
    async def sad_check(self, message):
        if message.author == self.client:
            return

        if self.responding:
            msg = message.content
            msg_words = msg.split()
            if any(word in msg_words for word in sad_words):
                await message.channel.send(f'{random.choice(load_options())} {message.author.name}')

# Helper Function


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return(quote)


def update_encouragements(encouraging_message):
    if "encouragements" in db.keys():
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db['encouragements'] = [encouraging_message]


def delete_encouragements(index):
    encouragements = db['encouragements']
    if len(encouragements) > index:
        del encouragements[index]
        db['encouragements'] = encouragements


def setup(client):

    client.add_cog(AllOrders(client))


def load_options():
    temp_list = starter_encouragements
    if 'encouragements' in db.keys():
        temp_list.extend(db['encouragements'])
    return temp_list


sad_words = ['sad', 'depressed', 'unhappy', 'miserable', 'depressing', 'cry', 'angry',
             'upset', 'pissed', 'worried', 'scared', 'terrified']

starter_encouragements = [
    'Cheer up',
    'Hang in there',
    'You are a great person / bot'
]
