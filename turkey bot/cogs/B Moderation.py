import discord 
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client 

    @commands.command(aliases=['c'], description = "clear's messages")
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit = amount)

    @commands.command(aliases= ['k'], description = "Kicks members")
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member : discord.Member):
        await member.kick()
        await ctx.channel.send(f"{member.mention} was kicked from the server.")

    @commands.command(aliases=['b'], description = "Ban members")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member):
        await member.ban()
        await ctx.channel.send(f"{member.mention} was banned from the server.")

    @commands.command(aliases=['ub'], description = "UnBan members")
    async def unban(self, ctx,*, member):
        banned_user= await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_user:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'{user.mention} was unbanned.')
                return

    @commands.command(aliases=['ui'], description = "Shows User's Info ")
    @commands.has_permissions(kick_members=True)
    async def info(self, ctx, member : discord.Member):
        embed = discord.Embed(title = member.name , description = f'User: {member.mention}' , color = 0xF59307) 
        embed.add_field(name= 'ID', value= member.id, inline = True)
        embed.set_thumbnail(url= member.avatar_url)
        embed.set_footer(icon_url= ctx.author.avatar_url , text = f"Requested by {ctx.author.name}" )
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Moderation(client))
