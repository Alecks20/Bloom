import os
import shlex
import traceback
import config
import discord
import asyncio


#Login Messages
@config.bot.event
async def on_ready():

  print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
  print(f"┃  Connected to Discord API           ┃")
  print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
  print(f"\nLogged in as {config.bot.user}")
  print("\nLoading Bot Cogs..\n")
  
  #Syncing the Slash Command Tree
  try:
    synced = await config.bot.tree.sync()
    print(f"\n{len(synced)} slash commands Synced\n")
  except Exception as e:
    print(traceback.format_exc())


  #Updating the bots presence
  await config.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="/help"))


async def main():
  try:
    testing = os.environ["TESTING"]
  except:
    testing = "true"
    
  if testing == "true":

    #Asking the user what cogs to load
    cogschoices = input("List cogs you want to load: ")
    if cogschoices == "all" or cogschoices == "":
      await load()
    else:
      cogschoices = shlex.split(cogschoices)
      for item in cogschoices:
        try:
          await config.bot.load_extension(f'cogs.{item}')
        except Exception:
          print(traceback.format_exc())

    await config.bot.start(config.testing_token)

  else:
    #dashboard()
    await load()
    if config.TOKEN == None:
      print("Token environment variable was not set.")
    else:
      await config.bot.start(config.TOKEN)
      

#Loading Bot Cogs on Production Server
async def load():
  for file in os.listdir('./cogs'):
    if file.endswith('.py'):
      await config.bot.load_extension(f'cogs.{file[:-3]}')
    

# Initialize Bot
asyncio.run(main())
