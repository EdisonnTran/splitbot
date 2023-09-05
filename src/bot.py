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


bot.run(DISCORD_TOKEN)