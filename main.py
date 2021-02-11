import discord
import os
import random


from replit import db
from web import start_web
from discord.ext import commands

client = commands.Bot(command_prefix='$')

cogs = ['bigmess','secret']

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
#  update_message('We have logged in as {0.user}'.format(client))


'''
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  msg_words = msg.split()

  responding = False
  if 'responding' in db.keys():
    responding = db['responding']  
  
  if not msg.startswith(command_prefix):
    options = starter_encouragements
    if 'encouragements' in db.keys():
      options = options + db['encouragements']

    if responding:
      if any(word in msg_words for word in sad_words):
        await message.channel.send(f'{random.choice(options)} {message.author.name}')


  else:
    #bot_msg_commands(message,strip(msg_words[0],command_prefix),msg_words[1:])
  # if message starts with command_prefix

  # goto message handler function OR
  # check for sad words

    if msg.startswith('$inspire'):
      quote = get_quote()
      await message.channel.send(quote)

    if msg.startswith('$msginfo'):
      temp_text = (f'{" ".join(msg_words[1:])} | msg_words = {msg.split()[1:]} | command = {msg_words[0][1:]}')
      temp_text = temp_text + (f'\tprefix = {msg_words[0][0]}')
      await message.channel.send(temp_text)

    if msg.startswith('$new'):
      encouraging_message = msg.split("$new ",1)[1]
      update_encouragements(encouraging_message)
      await message.channel.send("New encouraging message created")

    if msg.startswith('$sad_words'):
      await message.channel.send(f'sad words list :\n {sad_words}')

    if msg.startswith('$del'):
      encouragements = []
      temp_txt = ''
      if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        if encouragements:
          try:
            index = int(msg.split('$del',1)[1])
            delete_encouragements(index)
            encouragements = db['encouragements']
            temp_txt = (f'user created encouragements now include: {(" + ").join(encouragements)}')
          except:
            temp_txt = ('Something went wrong. Did you include an index number (starts at 0.)')
        else:
          temp_txt = ('Empty List : Add some using the "new" command')
      else:
        temp_txt = ('There is no list called "encouragements" in my memory')
      
      await message.channel.send(temp_txt)

    if msg.startswith('$list'):
      encouragements = []
      temp_txt=('We do not have any user added encouraging messages saved')
      if 'encouragements' in db.keys():
        encouragements = db['encouragements']
        if len(encouragements) != 0:
          temp_txt = (f'user created encouragements include: {(" + ").join(encouragements)}')

      await message.channel.send(temp_txt)

    if msg.startswith('$responding'):
      # add check for no argument to keep from error in terminal
      value = msg.split('$responding ',1)[1]

      if value.lower() in ['true','on']:
        db['responding'] = True
        responding = True
        await message.channel.send('RESPONDING is ON')
      elif value.lower() in ['false','off']:
        db['responding'] = False
        responding = False
        await message.channel.send('RESPONDING is OFF')
      else:
        await message.channel.send(f'STATUS unchanged, RESPONDING = {db["responding"]}')

    if msg.startswith('$status'):
      if responding:
        await message.channel.send('I am listening')
      else:
        await message.channel.send('I am distracted right now')
'''


start_web()
client.run(os.getenv('dTOKEN'))