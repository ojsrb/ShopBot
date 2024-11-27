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
scamdb = dbdb['scams']

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
    if db.find_one({'name': interaction.user.name}) is None:
        db.insert_one({
            'user': interaction.user.id,
            'name': interaction.user.name,
            'credits': 100,
            'items': [],
            'blacklisted': False,
        })
        await interaction.response.send_message(f"creating account for user {interaction.user.name}", ephemeral=True)
    else:
        await interaction.response.send_message("nice try :)", ephemeral=True)

@client.tree.command(name='pay')
async def pay(interaction: discord.Interaction, recipient: discord.User, amount: int):
    if db.find_one({'user': interaction.user.id}).get('blacklisted'):
        return
    dbrecipient = db.find_one({'user': recipient.id})
    dbbuyer = db.find_one({'user': interaction.user.id})
    if dbrecipient is None or dbbuyer is None:
        interaction.response.send_message("Users do not exist", ephemeral=True)
        return
    recipientMoney = dbrecipient.get('credits')
    buyerMoney = dbbuyer.get('credits')
    if buyerMoney >= amount and amount > 0:
        recipientNewMoney = recipientMoney + amount
        buyerNewMoney = buyerMoney - amount
        db.update_one({'user': recipient.id}, {'$set': {'credits': recipientNewMoney}})
        db.update_one({'user': interaction.user.id}, {'$set': {'credits': buyerNewMoney}})
        await interaction.response.send_message(f"sent {amount} credits to {recipient}", ephemeral=True)
        return
    else:
        await interaction.response.send_message("Invalid money! (nice try)", ephemeral=True)
        return

@client.tree.command(name='give')
async def give(interaction: discord.Interaction, target: discord.User, item: str):
    if db.find_one({'user': interaction.user.id}).get('blacklisted'):
        return
    dbgiver = db.find_one({'user': interaction.user.id})
    dbtarget = db.find_one({'user': target.id})
    if dbtarget is None or dbgiver is None:
        await interaction.response.send_message("Users do not exist", ephemeral=True)
        return
    giverItems = dbgiver.get('items')
    targetItems = dbtarget.get('items')
    if item in giverItems:
        giverItems.remove(item)
        targetItems.append(item)
    else:
        await interaction.response.send_message("Item not in your inventory!", ephemeral=True)
        return

    db.update_one({'user': target.id}, {'$set': {'items': targetItems}})
    db.update_one({'user': interaction.user.id}, {'$set': {'items': giverItems}})
    await interaction.response.send_message(f"sent {item} to {target.name}", ephemeral=True)

@client.tree.command(name='inventory')
async def inventory(interaction: discord.Interaction, share: bool):
    if db.find_one({'user': interaction.user.id}).get('blacklisted'):
        return
    dbuser = db.find_one({'user': interaction.user.id})
    if dbuser is None:
        return
    userItems = dbuser.get('items')
    userCredits = dbuser.get('credits')
    itemsList = ""
    for i in userItems:
        itemsList += f"{i}\n"
    await interaction.response.send_message(f"""
# {interaction.user.name}'s inventory:
### {userCredits} credits
----------------------------------------
## Items:
{itemsList}
""", ephemeral=not share)

@client.tree.command(name='scam')
async def scam(interaction: discord.Interaction, committer: discord.User, explanation: str):
    if db.find_one({'user': interaction.user.id}).get('blacklisted'):
        return
    scamdb.insert_one({'name': committer.name,
                       'id': committer.id,
                       'sender': interaction.user.name,
                       'senderid': interaction.user.id,
                       'explanation': explanation,})
    await interaction.response.send_message(f"{committer.name} reported, thank you.", ephemeral=True)

#End of main commands

#This is used to check version
@client.tree.command(name='version')
async def version(interaction: discord.Interaction):
    global currentVersion
    await interaction.response.send_message(f"My version is currently: {currentVersion}")

#Literally explains itself
client.run(TOKEN)
