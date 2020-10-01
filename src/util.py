import discord.ext.commands as commands
import discord

from src import config, db_access


async def join_if_not_in_channel(ctx: discord.ext.commands.Context, target_channel: discord.VoiceChannel) -> discord.voice_client.VoiceClient:
    voice = ctx.me.voice

    if target_channel is None:
        await ctx.send('User is not in any channel.')
        return None

    if voice is None:
        return await target_channel.connect()
    else:
        current_channel: discord.VoiceChannel = voice.channel
        if target_channel == current_channel:
            await ctx.voice_client.disconnect()
            return await current_channel.connect()
        if target_channel != current_channel:
            if ctx.voice_client is not None:
                await ctx.voice_client.disconnect()
            else:
                con = await current_channel.connect()
                await con.disconnect()
            return await target_channel.connect()


def user_is_admin(user_id):
    _config = config.Config()
    if str(_config.owner_id) == str(user_id):
        return True
    else:
        conn = db_access.create_connection()
        return db_access.is_admin(conn, user_id)


def write_bytes_io_to_file(filename, bytes_io):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet.
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytes_io.getbuffer())
