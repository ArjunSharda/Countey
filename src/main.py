import nextcord
from nextcord import Interaction
from nextcord.ext import commands, application_checks
import json
import os

client = nextcord.Client()

bot = commands.Bot(command_prefix="count!", help_command=None)


@bot.event
async def on_ready():
  await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"the count"))


@bot.event
async def on_guild_join(guild):
  for channel in guild.text_channels:
    if channel.permissions_for(guild.me).send_messages:
      await channel.send(":wave: Hey! Thanks for choosing Countey as a discord bot for you to use in your server. Countey uses slash commands, so be sure to keep that in mind when using the bot. \n \n Thanks, \n Arjun Sharda \n Founder")
      break


@bot.slash_command(description="Add to the count!")
async def add(interaction: nextcord.Interaction):
  if os.path.isfile("count.json"):
    with open("count.json", "r") as f:
      number = json.load(f)
  else:
    with open("number.json", "w") as f:
      json.dump(0, f)
    number = 0

    
  number += 1

  with open("count.json", "w") as f:
    json.dump(number, f)

  embed = nextcord.Embed(title="Success!", description="Your request has been processed. The count has been increased by **one**.", color = nextcord.Color.green())
  embed.add_field(name="Current Count", value=number)
  await interaction.send(embed=embed)
  goal = 12

  if number == goal:
    embed = nextcord.Embed(title="**Congratulations**", description=f"Congratulations on getting to {goal}! You did it, and this is a personal congratulation from Countey.", color=nextcord.Color.green())
    await interaction.user.send(embed=embed)


@bot.slash_command(description="Check the current count!")
async def currentcount(interaction: nextcord.Interaction):
  if os.path.isfile("count.json"):
    with open("count.json", "r") as f:
      number = json.load(f)
  else:
    embed = nextcord.Embed(title="Error", description="There was an error with processing your request.", color=nextcord.Color.red())
    await interaction.send(embed=embed)

  embed = nextcord.Embed(title="Current Count", description=f"The current count is |{number}|!", color=nextcord.Color.green())
  await interaction.send(embed=embed)


bot.run(os.environ['TOKEN'])
