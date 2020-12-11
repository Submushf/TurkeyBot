import discord 
from discord.ext import commands
import datetime
import random
import asyncio
import json
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
@commands.has_permissions(kick_members = True)
async def gstart(ctx):
    await ctx.send("Lets start with this giveaway! Answer this question within 15 seconds!")

    questions = [
        "which channel should it be hosted in?", 
        "what should be the duration of the giveaway? s |m | h | d",
        "what is the prize of the giveaway?"
    ]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('you didnt asnwer in time, please be quicker next time!.')
            return
        else:
            answers.append(msg.content)

    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didnt mention the channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"you didnt answer the time with the proper unit.")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer.")
        return

    prize = answers[2] 

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}.")

    embed = discord.Embed(title = "Giveaway", description = f"{prize}", color = 0xFF8000)

    embed.add_field(name= "Hosted by:", value= ctx.author.mention)

    embed.set_thumbnail(url ="https://cdn.discordapp.com/attachments/768503085412253707/776782057502146560/March_2020_Photography_Giveaway_Eight_Awesome_Prizes_You_Can_Win.jpg") 

    embed.set_footer(text= f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)

    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)

    new_msg = await channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    

    winner = random.choice(users)

    await channel.send(f"congratulations! {winner.mention} won {prize}!")


@client.command(aliases=['dh']) 
async def Dhelp(ctx):
    embed = discord.Embed(title = "Commands" , color = 0xFF8000) 
    embed.add_field(name= "📒 help" , value= "-shows this message. " , inline= False)  
    embed.add_field(name= "✋ suggest" , value= "-Suggest's random Stuff " , inline= False)
    embed.add_field(name= "🎉 gstart" , value= "-start a giveaway. required role (Giveaway manager) " , inline= False) 
    embed.set_footer(text= 'Prefixs- t!' ) 
    await ctx.send(embed=embed)

cmd = [
    "https://www.youtube.com/watch?v=Zszs7Jftv-M","https://www.youtube.com/watch?v=JBDt6ddgsNU","https://www.youtube.com/watch?v=qMmhnOQx7QE","https://www.youtube.com/watch?v=K8oAnM6p2HU&t=170s","https://www.youtube.com/watch?v=CUJFROAW5yA&list=RDCUJFROAW5yA&start_radio=1","https://www.youtube.com/watch?v=7xnW42MeCEc",
    "https://www.youtube.com/watch?v=lLvoZ5Wsf94","","https://youtu.be/3z4Hzo9UmrQ","https://www.youtube.com/watch?v=qLACUEjyHjw", "https://youtu.be/c6D8v6DhKc4", "https://youtu.be/2nVPFdqejD0", "https://youtu.be/lhSjYT7pWkw"
    ,"https://youtu.be/2nVPFdqejD0","https://www.youtube.com/watch?v=vdRYJPnBGVU","https://www.youtube.com/watch?v=DODLEX4zzLQ","https://www.youtube.com/watch?v=sKDzYQuPBsY","https://www.digitaltrends.com/web/funniest-youtube-videos/","https://www.youtube.com/watch?v=4d7XuZg5gkk","https://www.youtube.com/watch?v=QycJiYBPNIU","https://www.youtube.com/watch?v=RNFpMDXTCU8",
    "https://www.youtube.com/watch?v=9DWDJmC1Pkw","https://www.youtube.com/watch?v=VQJ40f_JdOI","https://www.youtube.com/watch?v=OqT8QK84KBc","https://www.youtube.com/watch?v=x-brv0EaPuE","https://www.youtube.com/watch?v=Zo_Y-n__Cbc",
    "https://www.youtube.com/watch?v=DrwYZCN2__g","https://www.youtube.com/watch?v=06kqZVHCSIs","https://www.youtube.com/watch?v=8oU0LAKoAL0","https://www.youtube.com/watch?v=J5Rzr-GL50Y","https://www.gq.com/story/no-cry-challenge-sad-internet-videos",
    "https://www.youtube.com/watch?v=tlvO3LnPQR8","https://www.youtube.com/watch?v=GfFVJyDVZuQ&list=WL&index=22&t=112s","https://www.youtube.com/watch?v=f0j--Y6G4Fg&list=WL&index=21&t=10s", "https://www.youtube.com/watch?v=Kv-OdJLhfFI","https://www.youtube.com/watch?v=Kv-OdJLhfFI","https://www.youtube.com/watch?v=OYMJNDB-rx0","https://www.youtube.com/watch?v=fxO4DCEw1FY",
    "https://www.youtube.com/watch?v=ftsBRXe_lhs","https://www.youtube.com/watch?v=HJjkw1kIgY0","https://www.youtube.com/watch?v=zBG8wsX3NkM"
]

@client.command(aliases=['s']) 
@commands.cooldown(1, 43200, commands.BucketType.user)
async def suggest(ctx):
    suggested =  random.choice(cmd)

    await ctx.send(f"**Today's suggestion's : {suggested}**")
    await ctx.send(f"Next suggestion available in 12 hours") 

client.run(os.environ['token']) 