from asyncio import sleep
import discord
from discord.ext import commands
import src.const as const
from src.config import Config
from os.path import join as join


startup_extensions = ["audio"]
bot = commands.Bot(command_prefix='!', description="Minge")
bot.volume = 0.2

config = Config()


@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(
            f'{bot.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})\n'
        )


@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        test = bot
        for client in bot.voice_clients:
            if client.channel == after.channel:
                audio = discord.FFmpegPCMAudio(
                    executable="C:\\Users\\Leon\\PycharmProjects\MingeBotTwo\\resources\\ffmpeg\\bin\\ffmpeg.exe",
                    source="C:\\Users\\Leon\\PycharmProjects\\MingeBotTwo\\resources\\audio\\memes\\hellothere.wav")
                audio = discord.PCMVolumeTransformer(audio, bot.volume)
                client.channel.play(audio)



@bot.command(name="join")
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(name="leave")
async def leave(ctx):
    await ctx.voice_client.disconnect()


@bot.command(name="volume")
async def volume(ctx, _volume: int):
    bot.volume = float(_volume / 100)


@bot.command(name="audiotest")
async def audiotest(ctx):
    voice_channel = ctx.author.voice.channel
    channel = None
    if voice_channel is not None:
        channel = voice_channel.name
        vc = await voice_channel.connect()

        audio = discord.FFmpegPCMAudio(executable="C:\\Users\\Leon\\PycharmProjects\MingeBotTwo\\resources\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\Leon\\PycharmProjects\\MingeBotTwo\\resources\\audio\\memes\\dejavu.wav")
        audio = discord.PCMVolumeTransformer(audio, bot.volume)
        vc.play(audio)
        # Sleep while audio is playing.
        while vc.is_playing():
            
            await sleep(0.1)
        await vc.disconnect()
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.
    # await ctx.message.delete()


try:
    bot.run(config.token)
except discord.errors.LoginFailure:
    print("Invalid token!\nPlease place a valid token in \"config.json\"")
