import io
import os
import sqlite3
from time import sleep

import discord
import requests
from discord.ext import commands
import src.util as util
import src.db_access as db_access
from src import const

bot: discord.ext.commands.Bot = None


def setup(_bot: discord.ext.commands.Bot):

    try:
        os.mkdir(const.AUDIO_DIR)
    except FileExistsError:
        pass
    try:
        os.mkdir(const.UPLOADED_AUDIO_DIR)
    except FileExistsError:
        pass

    global bot
    bot = _bot
    bot.volume = 1
    bot.add_command(play_audio)
    bot.add_command(join)
    bot.add_command(leave)
    bot.add_command(add_audio_fragment)
    bot.add_command(delete_audio_fragment)
    bot.add_command(play_audio_fragment)
    bot.add_listener(on_voice_state_update, "on_voice_state_update")


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


@commands.command(name="volume")
async def volume(ctx, _volume: int):
    bot.volume = float(_volume / 100)


@commands.command(name="join")
async def join(ctx: commands.Context):
    channel = ctx.author.voice.channel
    await channel.connect()


@commands.command(name="leave")
async def leave(ctx: commands.Context):
    await ctx.voice_client.disconnect()


@commands.command(name="audiotest")
async def audio_test(ctx: commands.Context):
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


@commands.command(name="play")
async def play_audio(ctx: commands.Context, args=''):
    if args is '':
        return await ctx.send(str(ctx.message.author.mention) + ', please specify a name.')
    voice_channel: discord.VoiceChannel = ctx.author.voice.channel
    if voice_channel is not None:
        vc = await util.join_if_not_in_channel(ctx, voice_channel)
        audio = discord.FFmpegPCMAudio(
            executable=const.FFMPG_EXE,
            source="C:\\Users\\Leon\\PycharmProjects\\MingeBotTwo\\resources\\audio\\memes\\dejavu.wav")
        audio = discord.PCMVolumeTransformer(audio, bot.volume)
        vc.play(audio)


@commands.command(name="addfragment")
async def add_audio_fragment(ctx: commands.Context, args=''):
    if args is '':
        return await ctx.send(str(ctx.message.author.mention) + 'Please specify a name.')
    if ctx.message.attachments is None:
        return await ctx.send(str(ctx.message.author.mention) + ", please attach a fragment.")
    if len(ctx.message.attachments) > 1:
        return await ctx.send(str(ctx.message.author.mention) + ", please attach a single fragment.")
    attachment = ctx.message.attachments[0]
    if not attachment.url.endswith('.wav'):
        return await ctx.send(str(ctx.message.author.mention) + ' Invalid file. Please use a .wav file.')

    response = requests.get(attachment.url, stream=True)
    audio_fragment = io.BytesIO(response.raw.read())
    conn = db_access.create_connection()
    try:
        db_access.add_fragment(conn, ctx.author.id, args)
    except sqlite3.IntegrityError:
        return await ctx.send(str(ctx.message.author.mention) + ' This name has already been used.')
    except sqlite3.OperationalError:
        return await ctx.send(str(ctx.message.author.mention) + ' Database error.')
    res = db_access.get_fragment_id_by_name(conn, args)
    util.write_bytes_io_to_file(os.path.join(const.UPLOADED_AUDIO_DIR, str(res[0][0]) + '.wav'), audio_fragment)
    return await ctx.send(str(ctx.message.author.mention) + ' Fragment added successfully.')


@commands.command(name="playfragment")
async def play_audio_fragment(ctx: commands.Context, args=''):
    if args is '':
        return await ctx.send(str(ctx.message.author.mention) + ', please specify a name.')
    voice_channel: discord.VoiceChannel = ctx.author.voice.channel
    if voice_channel is not None:
        conn = db_access.create_connection()
        fragment_id = db_access.get_fragment_id_by_name(conn, args)
        vc = await util.join_if_not_in_channel(ctx, voice_channel)
        audio = discord.FFmpegPCMAudio(
            executable=const.FFMPG_EXE,
            source=os.path.join(const.UPLOADED_AUDIO_DIR, str(fragment_id[0][0]) + '.wav'))
        audio = discord.PCMVolumeTransformer(audio, bot.volume)
        vc.play(audio)


@commands.command(name="deletefragment")
async def delete_audio_fragment(ctx: commands.Context, args=''):
    if args is '':
        return await ctx.send(str(ctx.message.author.mention) + ', please specify a name.')
    conn = db_access.create_connection()
    res = db_access.get_fragment_id_by_name(conn, args)
    os.remove(os.path.join(const.UPLOADED_AUDIO_DIR, str(res[0][0]) + '.wav'))
    db_access.delete_fragment(conn, res[0][0])
    return await ctx.send(str(ctx.message.author.mention) + ' successfully deleted fragment ' + args + '\'.')


