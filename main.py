import os
import random
import discord
from discord import Intents
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

#Version of the bot
currentVersion = "0.0.1"

#Load the app token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = Intents.default()

#Create the client
client = commands.Bot(command_prefix='/', intents=intents)

#Whitelist Owen and Jay. May be used for executive commands and stuff
whitelist = [1131962772587020298, 800898653820551168]

#Store inventories and stuff


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@client.tree.command(name='ping')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention}")
    ephemeral = True

#Main Commands go here

#End of main commands

#This is used to check version
@client.tree.command(name='version')
async def version(interaction: discord.Interaction):
    global currentVersion
    await interaction.response.send_message(f"My version is currently: {currentVersion}")

#Literally explains itself
client.run(TOKEN)
