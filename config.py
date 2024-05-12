
# Importing
import pymongo
from dotenv import load_dotenv
from discord.ext import commands
import os
import discord

# Setting variables
load_dotenv() # Loading from .env file (Comment out if your using proper env variables)

class BotClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix=commands.when_mentioned_or(">"), intents=intents)
    async def setup_hook(self) -> None:
        pass
bot = BotClient()

try:
    testing = os.environ["TESTING"]
except:
    testing = "false"
try:
    testing_token = os.environ["TESTING_TOKEN"]
except:
    print("Testing token was not set.")

if testing == "false":
    mongo = pymongo.MongoClient("mongodb://mongodb/") # Production environments are expected to use docker compose
elif testing == "true":
    mongo = pymongo.MongoClient(os.environ["MONGO_TESTING"])

db = mongo.bloom