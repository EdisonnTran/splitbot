from spreadsheetapi import SpreadsheetAPI

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

sheet = SpreadsheetAPI()

bot = commands.Bot(command_prefix='%', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Hello!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong")
    await ctx.message.add_reaction("👍")

@bot.command()
async def addSpending(ctx, title, cost, group):
    people = group.split()
    sheet.add_spending(title, cost, people)


bot.run(DISCORD_TOKEN)