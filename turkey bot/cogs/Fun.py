import discord 
from aiohttp import ClientSession
from discord.ext import commands
import random

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(
        name="dadjoke",
        description="Send a dad joke!",
        aliases=['dadjokes','dj'] 
    )
    async def dadjoke(self, ctx):
        url = "https://dad-jokes.p.rapidapi.com/random/jokes"

        headers = {
            'x-rapidapi-key': "81dd963d15mshf3e3a91dd6fe3cap1d971djsnbeb11a691831",
            'x-rapidapi-host': "dad-jokes.p.rapidapi.com" 
        }

        async with ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                r = await response.json()
                r = r["body"][0]
                embed= discord.Embed(color = 0x07C9F5)
                embed.add_field(name="Joke-",value=f"\n**{r['setup']}**\n||{r['punchline']}||", inline=True)
                await ctx.send(embed=embed)

    @commands.command(aliases=['p'],description = "Pat a user with a Gif")
    async def pat(self, ctx):
        embed = discord.Embed(color = 0x07C9F5 )
        embed.set_image(url= 'https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(aliases=['co'],description = "congratulate a user with a Gif")
    async def congrats(self, ctx,*,message):
        embed = discord.Embed(color = 0x07C9F5)
        embed.add_field(name="Congrats", value=f"{message}")
        embed.set_image(url= 'https://media.giphy.com/media/g9582DNuQppxC/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(aliases=['ki'], description = "Kick a user with a Gif")
    async def Kick(self, ctx):
        embed = discord.Embed(color = 0x07C9F5)
        embed.set_image(url= 'https://media.giphy.com/media/u2LJ0n4lx6jF6/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(aliases=['cp'],description="create a poll")
    async def poll(self,ctx,*,message):
        embed = discord.Embed(title = "Poll", description = f"{message}", color = 0x07C9F5) 
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')


#    @commands.command(aliases=['s'],description = "Suggest's video's to warm up") 
#    @commands.cooldown(1, 43200, commands.BucketType.user)
#    async def suggest(self,ctx):
#        suggested =  random.choice(cmd)

#        await ctx.send(f"**Today's suggestion For you: {suggested}**")
#        await ctx.send(f"Next suggestion available in 12 hours") 


#cmd = [
 #   "https://www.youtube.com/watch?v=Zszs7Jftv-M","https://www.youtube.com/watch?v=JBDt6ddgsNU","https://www.youtube.com/watch?v=qMmhnOQx7QE","https://www.youtube.com/watch?v=K8oAnM6p2HU&t=170s","https://www.youtube.com/watch?v=CUJFROAW5yA&list=RDCUJFROAW5yA&start_radio=1","https://www.youtube.com/watch?v=7xnW42MeCEc",
  #  "https://www.youtube.com/watch?v=lLvoZ5Wsf94","","https://youtu.be/3z4Hzo9UmrQ","https://www.youtube.com/watch?v=qLACUEjyHjw", "https://youtu.be/c6D8v6DhKc4", "https://youtu.be/2nVPFdqejD0", "https://youtu.be/lhSjYT7pWkw"
   # ,"https://youtu.be/2nVPFdqejD0","https://www.youtube.com/watch?v=vdRYJPnBGVU","https://www.youtube.com/watch?v=DODLEX4zzLQ","https://www.youtube.com/watch?v=sKDzYQuPBsY","https://www.digitaltrends.com/web/funniest-youtube-videos/","https://www.youtube.com/watch?v=4d7XuZg5gkk","https://www.youtube.com/watch?v=QycJiYBPNIU","https://www.youtube.com/watch?v=RNFpMDXTCU8",
    #"https://www.youtube.com/watch?v=9DWDJmC1Pkw","https://www.youtube.com/watch?v=VQJ40f_JdOI","https://www.youtube.com/watch?v=OqT8QK84KBc","https://www.youtube.com/watch?v=x-brv0EaPuE","https://www.youtube.com/watch?v=Zo_Y-n__Cbc",
    #"https://www.youtube.com/watch?v=DrwYZCN2__g","https://www.youtube.com/watch?v=06kqZVHCSIs","https://www.youtube.com/watch?v=8oU0LAKoAL0","https://www.youtube.com/watch?v=J5Rzr-GL50Y","https://www.gq.com/story/no-cry-challenge-sad-internet-videos",
    #"https://www.youtube.com/watch?v=tlvO3LnPQR8","https://www.youtube.com/watch?v=GfFVJyDVZuQ&list=WL&index=22&t=112s","https://www.youtube.com/watch?v=f0j--Y6G4Fg&list=WL&index=21&t=10s", "https://www.youtube.com/watch?v=Kv-OdJLhfFI","https://www.youtube.com/watch?v=Kv-OdJLhfFI","https://www.youtube.com/watch?v=OYMJNDB-rx0","https://www.youtube.com/watch?v=fxO4DCEw1FY",
    #"https://www.youtube.com/watch?v=ftsBRXe_lhs","https://www.youtube.com/watch?v=HJjkw1kIgY0","https://www.youtube.com/watch?v=zBG8wsX3NkM","https://youtu.be/biGHT89VsYo","https://youtu.be/-IIQIsZIo7o","https://youtu.be/8e1XX-ngJcc",
    #"https://youtu.be/0DAmWHxeoKw","https://youtu.be/Q3TYvvozc6s","https://youtu.be/3tND2re_D1A","https://youtu.be/F5naTTEkdAE"
#]


def setup(client):
    client.add_cog(Fun(client))