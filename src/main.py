import nextcord
from nextcord import Interaction
from nextcord.ext import commands, application_checks
import json
import os
import aiohttp

client = nextcord.Client()

bot = commands.Bot(command_prefix="count!", help_command=None)

goal = 12


@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="the count"))


@bot.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(":wave: Hey! Thanks for choosing Countey as a discord bot for you to use in your server. Countey uses slash commands, so be sure to keep that in mind when using the bot. \n \n Thanks, \n Arjun Sharda \n Founder")
            break


@bot.slash_command(description="Add to the count!")
async def add(interaction: nextcord.Interaction):
    if os.path.isfile("src/count.json"):
        with open("src/count.json", "r") as f:
            number = json.load(f)
    else:
        with open("src/count.json", "w") as f:
            json.dump(0, f)
        number = 0

    number += 1

    with open("src/count.json", "w") as f:
        json.dump(number, f)

    embed = nextcord.Embed(
        title="Success!",
		description="Your request has been processed. The count has been increased by **one**.",
		color=nextcord.Color.green()
	)
    embed.add_field(name="Current Count", value=number)
    await interaction.send(embed=embed)

    if number == goal:
        embed = nextcord.Embed(
			title="**Congratulations**",
			description=f"Congratulations on getting to {goal}! You did it, and this is a personal congratulation from Countey.",
			color=nextcord.Color.green()
		)
        await interaction.user.send(embed=embed)


@bot.slash_command(description="Check the current count!")
async def currentcount(interaction: nextcord.Interaction):
    if os.path.isfile("src/count.json"):
        with open("src/count.json", "r") as f:
            number = json.load(f)
    else:
        embed = nextcord.Embed(
            title="Error",
			description="There was an error with processing your request.", 
			color=nextcord.Color.red()
		)
        await interaction.send(embed=embed)

    embed = nextcord.Embed(
        title="Current Count",
		description=f"The current count is ||{number}||!",
		color=nextcord.Color.green()
	)
    await interaction.send(embed=embed)


async def CurrentVersionName():
    url = "https://api.github.com/repos/ArjunSharda/Countey/releases/latest"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json()
    return data["name"]


async def CurrentVersionDescription():
    url = "https://api.github.com/repos/ArjunSharda/Countey/releases/latest"
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json()
    return data["body"]


@bot.slash_command(description="View the changelog")
async def changelog(interaction: nextcord.Interaction):
    embed = nextcord.Embed(
		title=await CurrentVersionName(),
		description=await CurrentVersionDescription(),
		color=nextcord.Color.green()
	)
    await interaction.send(embed=embed, ephemeral=True)


@bot.slash_command(description="Reset your count!")
async def resetcount(interaction: Interaction, num: int):
    if os.path.isfile("src/count.json"):
        with open("src/count.json", "w") as f:
            number = num
            json.dump(number, f)
            embed = nextcord.Embed(
                title="Count Reset",
				description=f"Your request has been processed. The count has been reset to **{number}**.",
				color=nextcord.Color.green()
			)
            await interaction.send(embed=embed)
    else:
        embed = nextcord.Embed(
            title="Error",
			description="There was an error with processing your request.",
			color=nextcord.Color.red()
		)
        await interaction.send(embed=embed)


bot.run(os.environ['TOKEN'])
