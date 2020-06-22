import discord
from discord.utils import get
from discord.ext import commands
import shutil
import os
import asyncio
import youtube_dl

client = commands.Bot(command_prefix = "!")

### Bot booting ###
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Streaming(name="RAZERKrakenYT | #RazerStreamer!", url="https://www.twitch.tv/razerkrakenyt"))
    # await client.user.edit(username="Deathstalkers™")
    print("I am on service sir !")

### Member joining ###
@client.event
async def on_member_join(member: discord.Member):
    channel = await member.create_dm()
    await channel.send("Welcome to our server")

### Member leaving ###
@client.event
async def on_member_remove(member: discord.Member):
    print(f"{member} has left this server.")
    channel = await member.create_dm()
    await channel.send("Sorry to see you go :frowning2:")

### Latency ###
@client.command()
async def ping(ctx):
    await ctx.send(f"Currently pinging at {round(client.latency*1000)}ms")

### Deleting ###
@client.command()
@commands.has_role("DS-Bot")
async def delete(ctx, amount=1):
    if amount==1:
        await ctx.send(f'{ctx.author.mention} Please define range of deletion after command.\nExample: ".delete 5"')
    else:
        await ctx.channel.purge(limit=amount+1)

### Kick ###
@client.command()
@commands.has_role("DS-Bot")
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.send(f"{member.mention} has been kicked.")

### Banning ###
@client.command()
@commands.has_role("DS-Bot")
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send(f"{member.mention} has been banned.")

### Unbanning ###
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

### Exception handling ###
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"{ctx.author.mention} Oopppsss! Command not found!.")

### Echoing ###
@client.command()
@commands.has_role("DS-Bot")
async def echo(ctx):
    await ctx.channel.purge(limit=1)
    msg = ctx.message.content.split()
    output = ""
    for word in msg[1:]:
        output += word
        output += " "
    await ctx.channel.send(output)

### Dm a member ###
@client.command()
@commands.has_role("DS-Bot")
async def dm(ctx, member: discord.Member, *, content):
    await ctx.channel.purge(limit=1)
    channel = await member.create_dm()
    await channel.send(content)
    await ctx.channel.send(f'"{content}" has been sent to {member}')

###### Music ######

### Bot joining a voice channel ###
@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

### Bot leaving a voice channel ###
@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

client.run(os.environ["DISCORD_TOKEN"])