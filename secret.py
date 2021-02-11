import discord
from discord.ext import commands


class secret(commands.Cog):
  def __init__(self,client):
    self.client = client

  @commands.command(aliases=['Secret_Command','secret_command'], hidden=True)
  async def secret(self,ctx, message = None):
        
    description = 'Secret Message'
    embed = discord.Embed(title='SECRET TITLE',colour=discord.Colour(0xE5E242),description=description)

    embed.set_image(url="https://images.pexels.com/photos/3156660/pexels-photo-3156660.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500")
    embed.set_thumbnail(url=ctx.message.author.avatar_url_as(size=64))

    await ctx.send(embed=embed)

def setup(client):
  client.add_cog(secret(client))