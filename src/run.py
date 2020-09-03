from asyncio import sleep
import discord
from discord.ext import commands
import src.const as const
from src.config import Config
from os.path import join as join

bot = commands.Bot(command_prefix='!', description="Minge")
config = Config()

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )


@bot.command(name="join")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(name="leave")
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command(name="audiotest")
async def audiotest(ctx):
    voice_channel = ctx.author.channel
    channel = None
    if voice_channel is not None:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable=const.FFMPEG_DIR, source=join(const.AUDIO_MEMES_DIR, 'dejavu.wav')))
        # Sleep while audio is playing.
        while vc.is_playing():
            sleep(.1)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.
    await ctx.message.delete()


try:
    bot.run(config.token)
except discord.errors.LoginFailure:
    print("Invalid token!\nPlease place a valid token in \"config.json\"")
