from asyncio import sleep
import discord
from discord.ext import commands
import discord.ext.tasks
import src.const as const
from src.config import Config
import src.db_access

startup_extensions = ["commands.audio", "commands.general"]
bot = commands.Bot(command_prefix='!', description="Minge")

src.db_access.init_database()
config = Config()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )


try:
    for extension in startup_extensions:
        bot.load_extension(extension)
    bot.run(config.token)
except discord.errors.LoginFailure:
    print("Invalid token!\nPlease place a valid token in \"config.json\"")
