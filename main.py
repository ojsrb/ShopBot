import os
import random
import discord
from discord import Intents
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import pymongo

#Load the app token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('SERVER')

#set up database
dbclient = pymongo.MongoClient(SERVER)

dbdb = dbclient["inventories"]

db = dbdb["inventories"]

#Version of the bot
currentVersion = "0.0.1"

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

@client.tree.command(name='createaccount')
async def create(interaction: discord.Interaction):
    await interaction.response.send_message(f"creating account for user {interaction.user.name}", ephemeral=True)
    db.insert_one({
        'user': interaction.user.id,
        'credits': 100,
        'items': []
    })

@client.tree.command(name='additem')
async def additem(interaction: discord.Interaction, user: discord.User, item: str):
    if interaction.user.id in whitelist:
        dbuser = db.find_one({'user': user.id})
        if dbuser is None:
            interaction.response.send_message("User does not exist", ephemeral=True)
            return
        userItems = dbuser.get('items')
        userItems.append(item)
        db.update_one({'user': user.id}, {'$set': {'items': userItems}})
        interaction.response.send_message(f"Added item {item} to user {user.name}", ephemeral=True)
    else:
        interaction.response.send_message(f"{interaction.user.mention} You are not allowed to use this command.", ephemeral=True)
        return

@client.tree.command(name='removeitem')
async def removeitem(interaction: discord.Interaction, user: discord.User, item: str):
    if interaction.user.id in whitelist:
        dbuser = db.find_one({'user': user.id})
        if dbuser is None:
            interaction.response.send_message("User does not exist", ephemeral=True)
            return
        userItems = dbuser.get('items')
        userItems.remove(item)
        db.update_one({'user': user.id}, {'$set': {'items': userItems}})
    else:
        interaction.response.send_message(f"{interaction.user.mention} You are not allowed to use this command.", ephemeral=True)
        return

#End of main commands

#This is used to check version
@client.tree.command(name='version')
async def version(interaction: discord.Interaction):
    global currentVersion
    await interaction.response.send_message(f"My version is currently: {currentVersion}")

#Literally explains itself
client.run(TOKEN)
