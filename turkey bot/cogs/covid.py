import discord
import asyncio
import requests
import wikipedia
from discord.ext import commands


class others(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(description="Shows the covid stats")
    async def covid(self, ctx, *, countryName = None):
        try:
            if countryName is None:
                embed=discord.Embed(title="This command is used like this: ```g!covid [country]```", colour=0x07C9F5, timestamp=ctx.message.created_at)
                await ctx.send(embed=embed)


            else:
                url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName}"
                stats = requests.get(url)
                json_stats = stats.json()
                country = json_stats["country"]
                totalCases = json_stats["cases"]
                todayCases = json_stats["todayCases"]
                totalDeaths = json_stats["deaths"]
                todayDeaths = json_stats["todayDeaths"]
                recovered = json_stats["recovered"]
                active = json_stats["active"]
                critical = json_stats["critical"]
                casesPerOneMillion = json_stats["casesPerOneMillion"]
                deathsPerOneMillion = json_stats["deathsPerOneMillion"]
                totalTests = json_stats["totalTests"]
                testsPerOneMillion = json_stats["testsPerOneMillion"]

                embed2 = discord.Embed(title=f"**COVID-19 Status Of {country}**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!", colour=0x07C9F5, timestamp=ctx.message.created_at)
                embed2.add_field(name="**Total Cases**", value=totalCases, inline=True)
                embed2.add_field(name="**Today Cases**", value=todayCases, inline=True)
                embed2.add_field(name="**Total Deaths**", value=totalDeaths, inline=True)
                embed2.add_field(name="**Today Deaths**", value=todayDeaths, inline=True)
                embed2.add_field(name="**Recovered**", value=recovered, inline=True)
                embed2.add_field(name="**Active**", value=active, inline=True)
                embed2.add_field(name="**Critical**", value=critical, inline=True)
                embed2.add_field(name="**Cases Per One Million**", value=casesPerOneMillion, inline=True)
                embed2.add_field(name="**Deaths Per One Million**", value=deathsPerOneMillion, inline=True)
                embed2.add_field(name="**Total Tests**", value=totalTests, inline=True)
                embed2.add_field(name="**Tests Per One Million**", value=testsPerOneMillion, inline=True)

                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/781887772390719498/795612340116389898/covidbot.PNG")
                await ctx.send(embed=embed2)

        except:
            embed3 = discord.Embed(title="Invalid Country Name Or API Error! Try Again..!", colour=0x07C9F5, timestamp=ctx.message.created_at)
            embed3.set_author(name="Error!")
            await ctx.send(embed=embed3)

    @commands.command(description="gives answer to questions.")
    async def whatis(self,ctx, *, question):
        try:
            embed= discord.Embed(color=0x07C9F5)
            embed.add_field(name="✔ Searched-",value=f"**{wikipedia.summary(question, sentences=2)}**", inline=True)
            await ctx.send(embed=embed)
        except:
            embed= discord.Embed(color=0x07C9F5)
            embed.add_field(name="❌ Failed-", value=f"**Invalid command**", inline=True)
            await ctx.send("Invalid command")

    @commands.command(description="target the page from wikipedia")
    async def link(self,ctx, *, target):
        target_obj = wikipedia.page(target)
        await ctx.send(target_obj.title)
        await ctx.send(target_obj.url)


def setup(bot):
    bot.add_cog(others(bot))