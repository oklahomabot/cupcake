import discord
import os
import requests
import json
import random
from replit import db
from web import persist


client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy', 'miserable', 'depressing', 'cry', 'angry',
             'upset', 'pissed', 'worried', 'scared', 'terrified']

starter_encouragements = [
  'Cheer up',
  'Hang in there',
  'You are a great person / bot'
]
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

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if 'encouragements' in db.keys():
    options = options + db['encouragements']

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
      await message.channel.send('RESPONDING is ON')
    elif value.lower() in ['false','off']:
      db['responding'] = False
      await message.channel.send('RESPONDING is OFF')
    else:
      await message.channel.send(f'STATUS unchanged, RESPONDING = {db["responding"]}')

  if msg.startswith('$status'):
    if db['responding']:
      await message.channel.send('I am listening')
    else:
      await message.channel.send('I am distracted right now')

  if db['responding']:
    if any(word in msg for word in sad_words):
      await message.channel.send(f'{random.choice(options)} {message.author.name}')

persist()
client.run(os.getenv('dTOKEN'))