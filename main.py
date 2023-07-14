import requests

import discord
from discord.ext import commands
from discord.ui import Select, View

import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix="/", intents=discord.Intents.default())


@bot.event
async def on_ready():
    print("Bot is up and ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.tree.command(name="hey")
async def hello(interaction: discord.Interaction):
    """This command says hello!"""
    await interaction.response.send_message('hello')


@bot.tree.command(name="joke")
async def joke(interaction: discord.Interaction):
    """This command will tell a random joke"""
    url = 'https://v2.jokeapi.dev/joke/Any?type=single'
    r = requests.get(url)
    json = r.json()

    await interaction.response.send_message(json['joke'])


@bot.tree.command(name="joke_embed")
async def joke_embed(interaction: discord.Interaction):
    """This command will create an embed where you can select a joke category then it will tell that relevant joke"""
    select = Select(placeholder="Chose a joke category", options=[
        discord.SelectOption(label='All'),
        discord.SelectOption(label='Programming'),
        discord.SelectOption(label='Misc'),
        discord.SelectOption(label='Dark'),
        discord.SelectOption(label='Pun'),
        discord.SelectOption(label='Spooky'),
        discord.SelectOption(label='Christmas')
    ])

    async def my_callback(interaction):
        url = f'https://v2.jokeapi.dev/joke/{select.values[0]}?type=single'
        r = requests.get(url)
        json = r.json()

        await interaction.response.send_message(json['joke'], ephemeral=True, delete_after=30)

    select.callback = my_callback
    view = View()
    view.add_item(select)

    embed = discord.Embed(
        title='Generate a joke',
        description='Select a joke category below and then press the generate button and it will generate a joke for you using the https://jokeapi.dev API',
        colour=discord.Colour.dark_teal()
    )

    await interaction.response.send_message(embed=embed, view=view)


bot.run(token)
