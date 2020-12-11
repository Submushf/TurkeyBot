import re
import math
import random

import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(
        name = 'help', aliases = ['h'], description = "The help command!"
    )
    async def help(self, ctx, cog='1'):
        helpembed= discord.Embed(
            title= "Help Command" , color = 0x07C9F5 
        )
        helpembed.set_thumbnail(url= ctx.avatar_url) 

        cogs = [c for c in self.client.cogs.keys()]

        totalpages = math.ceil(len(cogs) / 4)

        cog = int(cog) 
        if cog > totalpages or cog < 1 :
            await ctx.send(f"invalid page number: `{cog}`, please pick from {totalpages}.")
            return



        neededcogs = []
        for i in range(4):
            x = (i) + (int(cog) -1) * 4
            try:
                neededcogs.append(cogs[x]) 
            except IndexError:
                pass


        for cog in neededcogs:
            commandList = ""
            for command in self.client.get_cog(cog).walk_commands():
                if command.hidden:
                    continue
                elif command.parent != None:
                    continue

                commandList += f"``{command.name}``- {command.description} \n" 
            #commandList += "\n"

            helpembed.add_field(name=cog, value= commandList, inline= False) 
            helpembed.set_footer(text=f"Prefix - t!") 

        await ctx.send(embed = helpembed) 



def setup(client):
    client.add_cog(Help(client))