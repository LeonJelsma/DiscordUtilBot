from time import sleep

import discord
from discord.ext import commands
import src.util as util

bot: discord.ext.commands.Bot = None


def setup(_bot: discord.ext.commands.Bot):
    global bot
    bot = _bot
    bot.volume = 0.2
    bot.add_command(test)
    bot.add_listener(on_voice_state_update, "on_voice_state_update")


@commands.command(name="test")
async def test(ctx):
    await ctx.send("nigga")


async def on_voice_state_update(member, before, after):
    if before.channel is None:
        for client in bot.voice_clients:
            if client.channel == after.channel:

                audio = discord.FFmpegPCMAudio(
                    executable="C:\\Users\\Leon\\PycharmProjects\MingeBotTwo\\resources\\ffmpeg\\bin\\ffmpeg.exe",
                    source="C:\\Users\\Leon\\PycharmProjects\\MingeBotTwo\\resources\\audio\\memes\\hellothere.wav")
                audio = discord.PCMVolumeTransformer(audio, bot.volume)
                client.channel.play(audio)
                # Sleep while audio is playing.
                while client.channel.is_playing():
                    await sleep(0.1)
                await client.channel.disconnect()


@commands.command(name="volume")
async def volume(ctx, _volume: int):
    bot.volume = float(_volume / 100)


@commands.command(name="audiotest")
async def audiotest(ctx: commands.Context):
    voice_channel = ctx.author.voice.channel
    util.join_if_not_in_channel(ctx, voice_channel)
    channel = None
    if voice_channel is not None:
        channel = voice_channel.name
        vc = await voice_channel.connect()

        audio = discord.FFmpegPCMAudio(
            executable="C:\\Users\\Leon\\PycharmProjects\MingeBotTwo\\resources\\ffmpeg\\bin\\ffmpeg.exe",
            source="C:\\Users\\Leon\\PycharmProjects\\MingeBotTwo\\resources\\audio\\memes\\dejavu.wav")
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
