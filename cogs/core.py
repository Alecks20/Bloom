import discord
from discord.ext import commands
from discord import app_commands
from config import db, bot
import io
import embeds
from typing import Optional
import traceback

class core(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
        print("┃  Loaded the Core Cog           ┃")
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

    @app_commands.command(name="update", description="Send an update for Bloom to the updates channel")
    @app_commands.describe(title="The title of the Update", description="What the update is about", mention="What role to mention on the update message", file="What file to attach to the update")
    async def updateslash(self, interaction: discord.Interaction, title: str, description: str, mention: Optional[discord.Role], file: Optional[discord.Attachment], channel: Optional[discord.TextChannel]):
      await interaction.response.defer(ephemeral=True)
      try:

         if interaction.user.id == 612522818294251522:
           if channel == None:
             channel = self.bot.get_channel(1239174746801836032)
           embed = embeds.get("core","update",(f"{title} <:9582_announce:1173479624412508202>",description,interaction))

           if mention:
            content = f"<@&{mention.id}>"
           else:
            content = None

           if content:
            await channel.send(content, embed=embed)
           else:
            await channel.send(embed=embed)

            if file:
                file_data = await file.read()
                file_obj = discord.File(io.BytesIO(file_data), filename=file.filename)
                try:
                   await channel.send(file=file_obj)
                except:
                   pass
            
            if db.updates.find({}):
              db.updates.delete_many({})
              
            db.updates.insert_one({"title": title,"description": description,"name": interaction.user.name.capitalize(),})
            
           await interaction.followup.send(embed=embeds.get("core","success",f"Successfully sent the update for Cloudy"))

         else:
          await interaction.followup.send(embed=embeds.get("core","denied","Only official Cloudy developers have access to this command"))

      except Exception:
         await interaction.followup.send(embeds.get("core","error",traceback.format_exc()))

    @app_commands.command(name="alert",description="View the latest update we have sent to the Bloom Support server")
    async def alert(self, interaction: discord.Interaction):
      await interaction.response.defer()
      for document in db.updates.find():
         embed = discord.Embed(title=document["title"], description=document["description"], colour=0x3679F5)
         embed.set_author(name=document["name"] + "・Bot Developer")
         await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(core(bot))
