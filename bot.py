import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix = ".")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="RAZERKrakenYT | #RazerStreamer!", url="https://www.twitch.tv/razerkrakenyt"))
    # await client.user.edit(username="Deathstalkers™")
    print("I am on service sir !")


#This commented code is for user join and leave.
# Will change this to send a message in server in a while.
"""
@client.event
async def on_member_join(member):
    print(f"{member} has joined this server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left this server.")
"""

@client.command()
async def ping(ctx):
    await ctx.send(f"Currently pinging at {round(client.latency*1000)}ms")

@client.command()
@commands.has_role("DS-Bot")
async def delete(ctx, amount=1):
    if amount==1:
        await ctx.send(f'{ctx.author.mention} Please define range of deletion after command.\nExample: ".delete 5"')
    else:
        await ctx.channel.purge(limit=amount+1)

@client.command()
@commands.has_role("DS-Bot")
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.send(f"{member.mention} has been kicked.")

@client.command()
@commands.has_role("DS-Bot")
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send(f"{member.mention} has been banned.")

@client.command()
@commands.has_role("DS-Bot")
async def unban(ctx, *, member):
    banned_list = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")
    
    for ban_entry in banned_list:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned.")
            return

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention} Oopppsss! Command not found!.")

@client.event
async def on_message(message):
    if message.content.startswith(".echo"):
        await message.channel.purge(limit=1)
        msg = message.content.split()
        output = ""
        for word in msg[1:]:
            output += word
            output += " "
        await client.send_message(message.channel, output)

client.run(os.environ["DISCORD_TOKEN"]);