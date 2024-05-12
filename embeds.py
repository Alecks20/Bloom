import discord
import traceback
from config import db, bot

def get(primary, category, content):
  try:

    if primary == "core":
      if category == "update":
        title = content[0]
        description = content[1]
        interaction = content[2]
        embed = discord.Embed(title=title, description=description, colour=0x3679F5)
        embed.set_author(name=interaction.user.name.capitalize() + "・Bot Developer", icon_url=interaction.user.avatar)
        embed.set_footer(text=interaction.guild.name)
      if category == "error":
        embed = discord.Embed(colour=0x4c7fff,description=f"Uh oh! An error occured, thankfully it was caught by our handler. If this error continues report it to our support server```{content}```")
      if category == "simple":
        embed = discord.Embed(colour=0x4c7fff,description=content)
      if category == "denied":
        embed = discord.Embed(colour=0xff3939,description=f"<:offline:1078291224840114186> {content}")
      if category == "success":
        embed = discord.Embed(colour=0x1fff8b,description=f"<:online:1078291279756136488>  {content}")

    return embed

  except Exception:
      embed = embedutil("error",traceback.format_exc())
      return embed
