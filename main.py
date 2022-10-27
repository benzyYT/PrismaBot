import asyncio
import datetime
import os
import io
from traceback import format_exception
import discord
from discord.ext import commands
import mysql.connector
import random
import string
from mysql.connector import MySQLConnection, Error
from dotenv import dotenv_values
from mysql.connector import RefreshOption
from discord.utils import get
refresh = RefreshOption.LOG | RefreshOption.THREADS
vars = dotenv_values(".env")
TOKEN = vars["TOKEN"]
whitelisted = vars["WHITELIST_IDS"]
from aioconsole import aexec



intents = discord.Intents().all()
client = commands.Bot(command_prefix='.', intents=intents)


################################# CODE #################################

# On Ready Event #
@client.event
async def on_ready():
    print(f"\n")
    print(f"Bot | Status:   Ready")
    print(f"Bot | ID:       {format(client.user.id)}")
    print(f"Bot | Name:     {format(client.user.name)}")
    print(f"Bot | Server:   {len(client.guilds)}")
    print(f"\n")
    print(f"The bot is ready to be used")
    #await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="to your commands"))
    
    
@client.event 
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        embed = discord.Embed(title="Command not found", description=f'⛔ This command does not exist', color=0xff0000) 
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="Member not found", description=f'⛔ That member was not found on this server', color=0xff0000) 
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title="No permission", description=f'⛔ This bot is not authorized to do this `(E: 403)`', color=0xff0000) 
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="Wrong statement", description=f'⛔ You must enter a number', color=0xff0000) 
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="FATAL ERROR", description=f'⛔ Error:\n```{error}```', color=0xff0000) 
        await ctx.send(embed=embed)
# On Ready Event #






# Server Logging #
@client.event
async def on_guild_join(guild):
    channel = client.get_channel(1035135578603266158) 
    print(f'I joined to a new server | Name: {guild.name}')
    with open('servers.log', 'a') as log:
        log.write(f'Name: {guild.name} | ID: {guild.id} | Owner: {guild.owner}')
        log.write('\n')
    embed = discord.Embed(title='New server', description='I joined to a new server!', color=0xff0000)
    embed.add_field(name='Server Name', value=f'`{guild.name}`', inline=False)
    embed.add_field(name='Server ID', value=f'`{guild.id}`', inline=False)
    embed.add_field(name='Server Owner', value=f'`{guild.owner}`', inline=False)
    await channel.send(embed=embed)
# Server Logging #


# Server Leave Command #
@client.command()
async def leaveguild(ctx, *args):
    if f'{ctx.author.id}' not in whitelisted:
        embed = discord.Embed(title='No permission', description='This is a developer command, you do not have permission to do this!', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        if len(args) > 1:
            embed = discord.Embed(title='Invalid input', description='Please provide an ID from a server you want me to leave!', color=0xff0000)
            await ctx.send(embed=embed)
        elif len(args) < 1:
            embed = discord.Embed(title='Invalid input', description='Please provide an ID from a server you want me to leave!', color=0xff0000)
            await ctx.send(embed=embed)
        else:
            guild = client.get_guild(int(args[0]))
            if guild:
                await guild.leave()
                embed = discord.Embed(title='Left server', description='I left the server!', color=0xff0000)
                embed.add_field(name='Server ID', value=f'`{args[0]}`', inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='Invalid input', description='I am not on this server!', color=0xff0000)
                embed.add_field(name='Server ID', value=f'`{args[0]}`', inline=False)
                await ctx.send(embed=embed)
# Server Leave Command #


# Server Auflisten Command #
@client.command()
async def listguilds(ctx):
    if f'{ctx.author.id}' not in whitelisted:
        embed = discord.Embed(title='No permission', description='This is a developer command, you do not have permission to do this!', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        guilds = [f'{guild.id} | {guild.name}' for guild in client.guilds]
        embed = discord.Embed(title='Serverlist', description=f'Here is the list of servers:\n`{guilds}`', color=0xff0000)
        await ctx.send(embed=embed)
# Server Auflisten Command #



# Kick Command #
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, Member: discord.Member):
    if Member:
        await ctx.guild.kick(Member)
        embed = discord.Embed(title='Member kicked', description=f'I have kicked the user `{Member}` successfully!', color=0xff0000)
        await ctx.send(embed=embed)
# Kick Command #


# Ban Command #
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, Member: discord.Member):
    if Member:
        await ctx.guild.ban(Member)
        embed = discord.Embed(title='Member banned', description=f'I have banned the user `{Member}` successfully!', color=0xff0000)
        await ctx.send(embed=embed)
# Ban Command #


# Say Command #
@client.command()
async def news(ctx, *, text):
    if f'{ctx.author.id}' not in whitelisted:
        embed = discord.Embed(title='No permission', description='This is a developer command, you do not have permission to do this!', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        message = ctx.message
        await message.delete()
        await ctx.send(f'{text}')
# Say Command #


# Clear Command #
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    if amount > 1000:
        embed = discord.Embed(title='Too many messages', description='The bot cannot delete over 1000 messages!', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        await ctx.message.delete()
        await asyncio.sleep(0.1)
        await ctx.channel.purge(limit=amount)


    




################################# CODE #################################
















client.run(TOKEN)