import discord 
from discord.ext import commands
import asyncio
import random

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
        embed = discord.Embed(color = 0x07C9F5 )
        embed.add_field(name="Kicked",value=f"👍 {member.mention} was kicked from the server.",inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=['b'], description = "Ban members")
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member):
        await member.ban()
        embed = discord.Embed(color= 0x07C9F5)
        embed.add_field(name="Banned", value= f"🔨 {member.mention} was banned from the server.") 
        await ctx.send(embed=embed)

    @commands.command(aliases=['ub'], description = "UnBan members")
    async def unban(self, ctx,*, member):
        banned_user= await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_user:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed = discord.Embed(color = 0x07C9F5)
                embed.add_field(name="Unbanned", value=f"📜 {user.mention} was unbanned.")
                await ctx.send(embed=embed)
                return

    @commands.command(aliases=['ui'], description = "Shows User's Info ")
    @commands.has_permissions(kick_members=True)
    async def info(self, ctx, member : discord.Member):
        embed = discord.Embed(title = member.name , description = f'User: {member.mention}' , color = 0x07C9F5)
        embed.add_field(name= 'ID', value= member.id, inline = True)
        embed.set_thumbnail(url= member.avatar_url)
        embed.set_footer(icon_url= ctx.author.avatar_url , text = f"Requested by {ctx.author.name}" )
        await ctx.send(embed=embed)

    @commands.command(
        name="channelstats",
        aliases=["cs"],
        description="Sends a embed with channel stats",
    )
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channelstats(self, ctx):
        channel = ctx.channel

        embed = discord.Embed(
            title=f"Stats for **{channel.name}**",
            description=f"{'**Category:** {}'.format(channel.category.name) if channel.category else 'This channel is not in a category'}",
            color=0x07C9F5,
        )
        embed.add_field(name="-Channel Guild", value=ctx.guild.name, inline=True)
        embed.add_field(name="-Channel Id", value=channel.id, inline=True)
        embed.add_field(
            name="-Channel Topic",
            value=f"{channel.topic if channel.topic else 'No topic.'}",
            inline=True,
        )
        embed.add_field(name="-Position", value=channel.position, inline=True)
        embed.add_field(
            name="-Slowmode Delay", value=channel.slowmode_delay, inline=True
        )
        embed.add_field(name="-nsfw?", value=channel.is_nsfw(), inline=True)
        embed.add_field(
            name="-Creation Time", value=channel.created_at, inline=True
        )
        embed.add_field(
            name="-Permissions Synced",
            value=channel.permissions_synced,
            inline=True,
        )
        embed.add_field(name="-Channel Hash", value=hash(channel), inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def poll(self,ctx,client,message):

        questions = [
            "which channel should the poll be in?", 
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

        embed = discord.Embed(title = "Poll", description = f"{message}", color = 0x7E07F5) 
        embed.set_footer(icon_url="https://cdn.discordapp.com/attachments/768122587174797364/779768983439015966/icon-256x256.png",text= "Drape's bot")
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')


def setup(client):
    client.add_cog(Moderation(client))
