import discord 
from discord.ext import commands
import datetime
import random
import os

client = commands.Bot(command_prefix= "g!", intents = discord.Intents.all())  
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity= discord.Activity(
        type= discord.ActivityType.watching, name= "❄️The snow fall" 
    )) 
    print("bot is ready")


@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}") 

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}") 

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}') 



client.run(os.environ['token']) 