import discord 
from discord.ext import commands
import datetime
import random
import asyncio
import json
import os

client = commands.Bot(command_prefix= "t!") 
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity= discord.Activity(
        type= discord.ActivityType.watching, name= "❄️The snow fall" 
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
@commands.has_role("Giveaway manager")
async def giveaway(ctx):
    await ctx.send("Lets start with this giveaway! Answer this question within 15 seconds!")

    questions = [
        "which channel should it be hosted in?", 
        "what should be the duration of the giveaway? s|m|h|d",
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


@client.command()
async def help(ctx):
    embed = discord.Embed(title = "Commands" , color = 0xFF8000) 
    embed.add_field(name= "📒 help" , value= "-shows this message. " , inline= False) 
    embed.add_field(name= "💰 ecohelp" , value= "-shows all the Economy commands. " , inline= False)
    embed.add_field(name= "🛠️ minfo" , value= "-shows info about the mentioned user . " , inline= False) 
    embed.add_field(name= "✋ suggest" , value= "-Suggest's random Stuff " , inline= False)
    embed.add_field(name= "🎉 giveaway" , value= "-start a giveaway. required role (Giveaway manager) " , inline= False) 
    embed.set_footer(text= 'Prefixs- t!' ) 
    await ctx.send(embed=embed)

@client.command()
async def ecohelp(ctx):
    embed = discord.Embed(title = "Commands" , color = 0x7c7979 ) 
    embed.add_field(name= "📊 balance " , value= "-Check your account balance " , inline= True)
    embed.add_field(name= "🏆 leaderboard " , value= "-shows the leader board " , inline= True)
    embed.add_field(name= "🤏 beg " , value= "-Beg for money " , inline= True) 
    embed.add_field(name= "👨‍💼 work " , value= "-work for money " , inline= True)    
    embed.add_field(name= "🏦 deposit " , value= "-deposit your money " , inline= True)  
    embed.add_field(name= "🤐 rob " , value= "-Rob money from anyone in the server " , inline= True)  
    embed.add_field(name= "📩 send " , value= "-send money to anyone in the server " , inline= True) 
    embed.add_field(name= "💸 withdraw " , value= "-withdraw money " , inline= True)
    embed.add_field(name= "🛒 shop" , value= "-show the shop " , inline= True)
    embed.add_field(name= "🍻 bet" , value= "-Bet money  " , inline= True)          
    embed.add_field(name= "💰 buy" , value= "-Buy from a shop" , inline= True)
    embed.add_field(name= "🛒 buy_this" , value= "-Buy from a shop" , inline= True)
    embed.add_field(name= "🛍️ bag" , value= "-shows whats in your bag" , inline= True)
    embed.add_field(name= "💡 sell, sell_this" , value= "-sell your item" , inline= True)         
    embed.set_footer(text= 'Prefixs- t!' ) 
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



@client.command()
async def balance(ctx):
	await open_account(ctx.author)
	user = ctx.author
	users = await get_bank_data()

	wallet_amt = users[str(user.id)]["wallet"]
	bank_amt = users[str(user.id)]["bank"]

	em = discord.Embed(title = f"{ctx.author.name}'s  balance", color = 0x7c7979)
	em.set_thumbnail(url= "https://media.discordapp.net/attachments/768122587174797364/777542741575335985/Daco_4263670.png?width=481&height=481")
	em.add_field(name = "Wallet balance", value = wallet_amt)
	em.add_field(name = "Bank balance", value = bank_amt)
	await ctx.send(embed= em)

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def beg(ctx):	
	await open_account(ctx.author)

	users = await get_bank_data()

	user = ctx.author

	earnings = random.randrange(20)

	await ctx.send(f"📑 someone gave you 💰{earnings} coins!!")


	users[str(user.id)]["wallet"] += earnings
	
	with open("mainbank.json","w") as f:
		json.dump(users,f) 


@client.command()
@commands.cooldown(1, 40, commands.BucketType.user)
async def work(ctx):	
	await open_account(ctx.author)

	users = await get_bank_data()

	user = ctx.author

	earnings = random.randrange(20)

	await ctx.send(f"You earned 💰{earnings} coins!!")


	users[str(user.id)]["wallet"] += earnings
	
	with open("mainbank.json","w") as f:
		json.dump(users,f) 

@client.command()
async def withdraw(ctx,amount = None):
	await open_account(ctx.author)

	if amount == None:
		await ctx.send("please enter the amount")
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[1]:
		await ctx.send("you dont have that much money!")
		return
	if amount<0:
		await ctx.send("amount must be positive!")
		return

	await update_bank(ctx.author,amount)
	await update_bank(ctx.author,-1*amount, "bank")

	await ctx.send(f"You withdrew {amount} coins!")

@client.command()
async def deposit(ctx,amount = None):
	await open_account(ctx.author)

	if amount == None:
		await ctx.send("please enter the amount")
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[0]:
		await ctx.send("you dont have that much money!")
		return
	if amount<0:
		await ctx.send("amount must be positive!")
		return

	await update_bank(ctx.author,-1*amount)
	await update_bank(ctx.author,amount, "bank")

	await ctx.send(f"You deposited {amount} coins!")

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def send(ctx,member:discord.Member,amount = None):
	await open_account(ctx.author)
	await open_account(member)

	if amount == None:
		await ctx.send("please enter the amount")
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[1]:
		await ctx.send("you dont have that much money!")
		return
	if amount<0:
		await ctx.send("amount must be positive!")
		return

	await update_bank(ctx.author,-1*amount, "bank")
	await update_bank(member,amount, "bank")

	await ctx.send(f"You gave {amount} coins!")

@client.command()
@commands.cooldown(1, 100, commands.BucketType.user)
async def rob(ctx,member:discord.Member):
	await open_account(ctx.author)
	await open_account(member)

	bal = await update_bank(member)

	if bal[0]<100:
		await ctx.send("Its useless to rob this guy")
		return

	earnings = random.randrange(0, bal[0])

	await update_bank(ctx.author,earnings)
	await update_bank(member,-1*earnings)

	await ctx.send(f"You robbed and got {earnings} coins!") 

@client.command()
@commands.cooldown(1, 100, commands.BucketType.user)
async def thanosnap(ctx,member:discord.Member):
	await open_account(ctx.author)
	await open_account(member)

	bal = await update_bank(member)

	if bal[0]<100:
		await ctx.send("Its you cant snap this legend!")
		return

	earnings = random.randrange(0, bal[0])

	await update_bank(ctx.author,earnings)
	await update_bank(member,-1*earnings)

	await ctx.send(f"You snaped him to the other world!") 


@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def bet(ctx,amount = None):
	await open_account(ctx.author)

	if amount == None:
		await ctx.send("please enter the amount")
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[0]:
		await ctx.send("you dont have that much money!")
		return
	if amount<0:
		await ctx.send("amount must be positive!")
		return

	final = []
	for i in range(3):
		i = random.choice(["🏦","🚀","🌪️"])

		final.append(i)

	await ctx.send(str(final))

	if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
		await update_bank(ctx.author,2*amount)
		await ctx.send("You won!")
	else:
		await update_bank(ctx.author,-1*amount)
		await ctx.send("You Lost.")

async def open_account(user):

	users = await get_bank_data()

	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["wallet"] = 0 
		users[str(user.id)]["bank"] = 0

	with open("mainbank.json","w") as f:
		json.dump(users,f) 
	return True

async def get_bank_data():
	with open("mainbank.json","r") as f:
		users = json.load(f)

	return users

async def update_bank(user,change = 0,mode = "wallet"):
	users = await get_bank_data()

	users[str(user.id)][mode] += change

	with open("mainbank.json","w") as f:
		json.dump(users,f) 
	
	bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]	
	return bal

mainshop = [{"name":"Watch","price":100,"description":"Time"},
            {"name":"Laptop","price":1000,"description":"Work"},
            {"name":"PC","price":10000,"description":"Gaming"}]


@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["name"]
        price = item["price"]
        desc = item["description"]
        em.add_field(name = name, value = f"${price} | {desc}")

    await ctx.send(embed = em)



@client.command()
async def buy(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have enough money in your wallet to buy {amount} {item}")
            return


    await ctx.send(f"You just bought {amount} {item}")


@client.command()
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = "Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em)    

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("That Object isn't there!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your bag.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

@client.command(aliases = ["lb"])
async def leaderboard(ctx,x = 1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0x7c7979))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

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