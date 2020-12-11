import discord 
from discord.ext import commands
import random

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(description = "Reply's pong!")
    async def ping(self, ctx):
        await ctx.send("Pong!")

    @commands.command(description = "Slap a user with a Gif")
    async def slap(self, ctx):
        embed = discord.Embed(color = 0x07C9F5 )
        embed.set_image(url= 'https://media.giphy.com/media/xUNd9HZq1itMkiK652/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(description = "Beat a user with a Gif") 
    async def beat(self, ctx):
        embed = discord.Embed(color = 0x07C9F5 )
        embed.set_image(url= 'https://media.giphy.com/media/m6etefcEsTANa/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(description = "Pat a user with a Gif")
    async def pat(self, ctx):
        embed = discord.Embed(color = 0x07C9F5 )
        embed.set_image(url= 'https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(description = "congratulate a user with a Gif")
    async def congrats(self, ctx):
        embed = discord.Embed(color = 0x07C9F5)
        embed.set_image(url= 'https://media.giphy.com/media/g9582DNuQppxC/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(description = "Kick a user with a Gif")
    async def Kick(self, ctx):
        embed = discord.Embed(color = 0x07C9F5)
        embed.set_image(url= 'https://media.giphy.com/media/u2LJ0n4lx6jF6/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(description = "Baka a user with an Gif")
    async def baka(self, ctx):
        embed = discord.Embed(color = 0x07C9F5)
        embed.set_image(url= 'https://media.giphy.com/media/4QxQgWZHbeYwM/giphy.gif')
        await ctx.send(embed=embed)

    @commands.command(description = "Uno reverse")
    async def reverse(self, ctx):
        embed = discord.Embed(color = 0xF59307)
        embed.set_image(url= 'https://media.giphy.com/media/Wt6kNaMjofj1jHkF7t/giphy.gif') 
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))