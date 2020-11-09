import discord 
from discord.ext import commands
import datetime
import random
import asyncio
import os

client = commands.Bot(command_prefix= "T!") 
client.remove_command("help")

@client.command()
@commands.has_role("Giveaways")
async def gstart(ctx, mins : int, * , prize = str):
    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

    end = datetime.datetime.utcnow() + datetime.timedelta(seconds= mins*60)

    embed.add_field(name = "Ends at:", value = f"{end} UTC")
    embed.set_footer(text= f"ends {mins} minutes from now ") 

    my_msg = await ctx.send(embed = embed)

    await my_msg.add_reaction("🎉") 

    await asyncio.sleep(mins *60 )   

    new_msg = ctx.channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten() 
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await ctx.send(f"Congragulations! {winner.mention} won {prize}!")

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity= discord.Activity(
        type= discord.ActivityType.playing, name= "🦃Catch the Turkey | T!help" 
    )) 
    print("bot is ready") 

@client.command()
async def help(ctx):
    embed = discord.Embed(title = "Commands" , color = discord.Colour.green()) 
    embed.add_field(name= "🏓 ping" , value= "-reply's pong! . " , inline= True)
    embed.add_field(name= "📂 clear {# of msg}" , value= "-Deletes the given amount of messages. " , inline= True)
    embed.add_field(name= "🦵 kick @mention" , value= "-Kicks the mentioned User. " , inline= True)
    embed.add_field(name= "🔨 ban @mention" , value= "-Bans the mentioned user. " , inline= True)
    embed.add_field(name= "🛠️ unban @mention" , value= "Unbans the mentioned User. " , inline= True)
    embed.add_field(name= "📒 minfo" , value= "-shows info about the mentioned user . " , inline= True) 
    embed.add_field(name= "🎉 gstart [time] {prize}" , value= "-start a giveaway. " , inline= True) 
    embed.set_thumbnail(url ="https://cdn.discordapp.com/attachments/768122587174797364/774984074778378260/turkeybot-removebg-preview.png") 
    embed.set_footer(text= 'Prefixs- T!, more commands coming soon' ) 
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send("pong!")

@client.command(aliases=['user','info']) 
@commands.has_permissions(kick_members= True)
async def minfo(ctx, member : discord.Member):
    embed = discord.Embed(title= member.name , description = member.mention , color = discord.Colour.green()) 
    embed.add_field(name = "ID" , value = member.id , inline = True)
    embed.set_thumbnail(url = member.avatar_url) 
    embed.set_footer(icon_url= ctx.author.avatar_url, text= f"Requested by {ctx.author.name }")
    await ctx.send(embed = embed) 

@client.command(aliases=['c'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx,amount=2):
    await ctx.channel.purge(limit = amount)  

@client.command(aliases= ['k'])
@commands.has_guild_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "reason not provided"):
    await member.kick(reason = reason) 

@client.command(aliases= ['b'])
@commands.has_guild_permissions(ban_members = True)
async def Ban(ctx,member : discord.Member,*,reason):
    await member.ban(reason = reason) 


@client.command(aliases= ['ub'])
@commands.has_guild_permissions(ban_members = True) 
async def unBan(ctx,*,member):
    banned_users = await ctx.guild.ban()
    member_name, member_disc = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name, member_disc):

            await ctx.guild.Unban(user)
            await ctx.send(member_name +" Has been Unbanned")
            return

        await ctx.send(member+" was not found") 

client.run(os.environ('Token'))