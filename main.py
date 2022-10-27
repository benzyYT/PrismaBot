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
    print(f"Bot | Status:   Bereit")
    print(f"Bot | ID:       {format(client.user.id)}")
    print(f"Bot | Name:     {format(client.user.name)}")
    print(f"Bot | Server:   {len(client.guilds)}")
    print(f"\n")
    print(f"Der Bot ist bereit genutzt zu werden")
    
    
@client.event 
async def on_command_error(ctx, error): 
    if isinstance(error, commands.CommandNotFound): 
        embed = discord.Embed(title="Command nicht gefunden", description=f'⛔ Diesen Command gibt es nicht', color=0xff0000) 
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="Mitglied nicht gefunden", description=f'⛔ Dieses Mitglied gibt es nicht', color=0xff0000) 
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(title="Keine Berechtigung", description=f'⛔ Dazu hat dieser Bot keine Berechtigung `(E: 403)`', color=0xff0000) 
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="ERROR", description=f'⛔ Fehler:\n```{error}```', color=0xff0000) 
        await ctx.send(embed=embed)
# On Ready Event #






# Server Logging #
@client.event
async def on_guild_join(guild):
    channel = client.get_channel(1035135578603266158) 
    print(f'Ich bin einem neuen Server gejoint | Name: {guild.name}')
    with open('servers.log', 'a') as log:
        log.write(f'Name: {guild.name} | ID: {guild.id} | Owner: {guild.owner}')
        log.write('\n')
    embed = discord.Embed(title='Neuer Server', description='Ich bin einem neuen Server gejoint!', color=0xff0000)
    embed.add_field(name='Server Name', value=f'`{guild.name}`', inline=False)
    embed.add_field(name='Server ID', value=f'`{guild.id}`', inline=False)
    embed.add_field(name='Server Owner', value=f'`{guild.owner}`', inline=False)
    await channel.send(embed=embed)
# Server Logging #


# Server Leave Command #
@client.command()
async def leaveguild(ctx, *args):
    if f'{ctx.author.id}' not in whitelisted:
        embed = discord.Embed(title='Keine Berechtigung', description='Dies ist ein Entwicklercommand, dazu hast du keine Berechtigung!', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        if len(args) > 1:
            embed = discord.Embed(title='Ungültige Angabe', description='Bitte gib eine ID von einem Server an, den ich verlassen soll!', color=0xff0000)
            await ctx.send(embed=embed)
        elif len(args) < 1:
            embed = discord.Embed(title='Ungültige Angabe', description='Bitte gib eine ID von einem Server an, den ich verlassen soll!', color=0xff0000)
            await ctx.send(embed=embed)
        else:
            guild = client.get_guild(int(args[0]))
            if guild:
                await guild.leave()
                embed = discord.Embed(title='Server verlassen', description='Ich habe den Server verlassen!', color=0xff0000)
                embed.add_field(name='Server ID', value=f'`{args[0]}`', inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='Ungültige Angabe', description='Ich bin auf diesem Server nicht!', color=0xff0000)
                embed.add_field(name='Server ID', value=f'`{args[0]}`', inline=False)
                await ctx.send(embed=embed)
# Server Leave Command #


# Server Auflisten Command #
@client.command()
async def listguilds(ctx):
    if f'{ctx.author.id}' not in whitelisted:
        embed = discord.Embed(title='Keine Berechtigung', description='Dies ist ein Entwicklercommand, dazu hast du keine Berechtigung!', color=0xff0000)
        await ctx.send(embed=embed)
    else:
        guilds = [f'{guild.id} | {guild.name}' for guild in client.guilds]
        embed = discord.Embed(title='Serverliste', description=f'Hier ist die Liste an Servern:\n`{guilds}`', color=0xff0000)
        await ctx.send(embed=embed)
# Server Auflisten Command #



# Kick Command #
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, Member: discord.Member):
    if Member:
        await ctx.guild.kick(Member)
        embed = discord.Embed(title='Member gekickt', description=f'Ich habe den Nutzer `{Member}` erfolgreich gekickt!', color=0xff0000)
        await ctx.send(embed=embed)
# Kick Command #


# Ban Command #
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, Member: discord.Member):
    if Member:
        await ctx.guild.ban(Member)
        embed = discord.Embed(title='Member gebannt', description=f'Ich habe den Nutzer `{Member}` erfolgreich gebannt!', color=0xff0000)
        await ctx.send(embed=embed)
# Ban Command #


# Say Command #
@client.command()
async def say(ctx, *, text):
    message = ctx.message
    await message.delete()
    await ctx.send(f'{text}')
# Say Command #


    




################################# CODE #################################
















client.run(TOKEN)