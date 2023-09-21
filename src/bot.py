from spreadsheetapi import SpreadsheetAPI
import spreadsheetDB

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
async def addSpending(ctx, title, cost, *args):
    spreadsheet = spreadsheetDB.get_spreadsheet(str(ctx.guild.id))
    sheet.add_spending(spreadsheet, title, float(cost), [*args])
    await ctx.message.add_reaction("✅")

@bot.command()
async def addSpreadsheet(ctx, spreadsheet_id):
    server_id = str(ctx.guild.id)
    spreadsheetDB.add_spreadsheet(server_id, spreadsheet_id)
    await ctx.message.add_reaction("✅")




bot.run(DISCORD_TOKEN)