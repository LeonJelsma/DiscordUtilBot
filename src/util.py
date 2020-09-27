import discord.ext.commands as commands
import discord


async def join_if_not_in_channel(ctx: commands.Context, channel: discord.VoiceChannel):
    if ctx.voice_client.channel != channel:
        await ctx.voice_client.disconnect()
