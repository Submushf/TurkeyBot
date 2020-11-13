import discord 
from discord.ext import commands
import datetime
import random
import asyncio
import os

client = commands.Bot(command_prefix= "t!") 
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity= discord.Activity(
        type= discord.ActivityType.watching, name= "t!help" 
    )) 
    print("bot is ready")

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24} 

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

@client.command()
@commands.has_role("Owner")
async def giveaway(ctx):
    await ctx.send("let's start with this giveaway! Answer this few questions within 15 seconds!") 

    questions = ["which channel whould it be hosted in?",
        "what should be the duration of the giveaway? s|m|h|d",
        "what is the prize of the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
            await ctx.send(i)

    try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
    except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time! ')
            return
    else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"you didnt mention the channel properly. do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"you didnt answer the time with the proper unit, use (s|m|h|d)!")
        return
    elif time == -2:
        await ctx.send(f"the time must be a integer. Please enter an integer")
        return
    prize = answers[2]
    
    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}! ")


    embed = discord.Embed(title = "Giveaway", description = f"{prize}", color = 0x0712F5)

    embed.add_field(name= "Hosted by:", value = ctx.author.mention )

    embed.set_footer(text= f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("🎉")


    await asyncio.sleep(time)

    new_msg = await channel.fetch_message(my_msg.id)
    
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congragulations! {winner.mention} won {prize}!")


@client.command()
async def help(ctx):
    embed = discord.Embed(title = "Commands" , color = discord.Colour.green()) 
    embed.add_field(name= "🏓 ping" , value= "-reply's pong! . " , inline= True)
    embed.add_field(name= "📂 clear {# of msg}" , value= "-Deletes the given amount of messages. " , inline= True)
    embed.add_field(name= "🦵 kick @mention" , value= "-Kicks the mentioned User. " , inline= True)
    embed.add_field(name= "🔨 ban @mention" , value= "-Bans the mentioned user. " , inline= True)
    embed.add_field(name= "🛠️ unban @mention" , value= "Unbans the mentioned User. " , inline= True)
    embed.add_field(name= "📒 minfo" , value= "-shows info about the mentioned user . " , inline= True) 
    embed.add_field(name= "🎉 giveaway" , value= "-start a giveaway. " , inline= True) 
    embed.set_thumbnail(url ="https://cdn.discordapp.com/attachments/768122587174797364/774984074778378260/turkeybot-removebg-preview.png") 
    embed.set_footer(text= 'Prefixs- t!, more commands coming soon' ) 
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
    await ctx.send(f"removed {amount} of messages")  

@client.command(aliases= ['k'])
@commands.has_guild_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason= "reason not provided"):
    await member.kick(reason = reason) 
    await ctx.send("user have been kicked")

@client.command(aliases= ['b'])
@commands.has_guild_permissions(ban_members = True)
async def Ban(ctx,member : discord.Member,*,reason):
    await member.ban(reason = reason) 
    await ctx.send("user have been banned")


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

client.run("Nzc0NTM4NTA3MzE0MDAzOTc5.X6ZPMg.MS4bbLnG4l_7xjlKHrI0UYtq8n8")