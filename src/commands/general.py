import io
import json
import os
import random
import sqlite3
from time import sleep
import discord
from discord import member

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import requests
from discord.ext import commands
import src.util as util
from src import const, config, db_access

config = config.Config()
pytesseract.pytesseract.tesseract_cmd = config.tesseract_location
bot: discord.ext.commands.Bot = None
pic_ext = ['.jpg', '.png', '.jpeg']


def setup(_bot: discord.ext.commands.Bot):
    global bot
    bot = _bot
    bot.add_command(spam)
    bot.add_command(roll)
    bot.add_command(pick_card)
    bot.add_command(random_cat_fact)
    bot.add_command(get_weather_report)
    bot.add_command(read_image)
    bot.add_command(add_admin)
    bot.add_command(remove_admin)
    bot.add_command(add_response)
    bot.add_command(delete_response)
    bot.add_command(add_keyword)
    bot.add_command(delete_keyword)
    bot.add_listener(on_message, "on_message")


async def on_message(message: discord.message):
    if message.author != bot.user:
        conn = db_access.create_connection()
        keywords = db_access.get_all_keywords(conn)
        for word in message.content.split():
            if word in keywords:
                responses = db_access.get_all_responses(conn)
                return await message.channel.send(responses[random.randint(0, len(responses)-1)])


@commands.command(name="spam")
async def spam(ctx: commands.Context, target):
    spam_count = 5
    for x in range(spam_count):
        await sleep(0.1)
        await ctx.send(target)


@commands.command(name="addadmin")
async def add_admin(ctx: commands.Context, args):
    conn = db_access.create_connection()
    if not util.user_is_admin(ctx.author.id):
        return await ctx.send(str(ctx.message.author.mention) + ", you are not authorized.")
    if len(ctx.message.mentions) < 1:
        return await ctx.send(str(ctx.message.author.mention) + ", please mention at least one user to promote to admin.")
    for mention in ctx.message.mentions:
        try:
            db_access.add_admin(conn, mention.id)
            await ctx.send(str(ctx.message.author.mention) + ", user " + mention.mention + " is now an admin.")
        except sqlite3.IntegrityError:
            return await ctx.send(str(ctx.message.author.mention) + ", user " + mention.mention + " is already an admin.")


@commands.command(name="removeadmin")
async def remove_admin(ctx: commands.Context, args):
    conn = db_access.create_connection()
    if not util.user_is_admin(ctx.author.id):
        return await ctx.send(str(ctx.message.author.mention) + ", you are not authorized.")
    if len(ctx.message.mentions) < 1:
        return await ctx.send(str(ctx.message.author.mention) + ", please mention at least one user to demote from admin.")
    for mention in ctx.message.mentions:
        if not db_access.is_admin(conn, mention.id):
            return await ctx.send(str(ctx.message.author.mention) + ", user " + mention.mention + " isn't an admin.")
        try:
            db_access.delete_admin(conn, mention.id)
            await ctx.send(str(ctx.message.author.mention) + ", user " + mention.mention + " is no longer an admin.")
        except sqlite3.IntegrityError:
            return await ctx.send(str(ctx.message.author.mention) + ", user " + mention.mention + " isn't an admin.")


@commands.command(name="addkeyword")
async def add_keyword(ctx: commands.Context, args):
    if not util.user_is_admin(ctx.author.id):
        return await ctx.send(str(ctx.message.author.mention) + ", you are not authorized.")
    conn = db_access.create_connection()
    try:
        db_access.add_keyword(conn, args)
        return await ctx.send(str(ctx.message.author.mention) + " added keyword: \"" + args + "\".")
    except sqlite3.IntegrityError:
        return await ctx.send(str(ctx.message.author.mention) + ", this keyword already exists")


@commands.command(name="deletekeyword")
async def delete_keyword(ctx: commands.Context, args):
    if not util.user_is_admin(ctx.author.id):
        return await ctx.send(str(ctx.message.author.mention) + ", you are not authorized.")
    conn = db_access.create_connection()
    if db_access.is_keyword(conn, args):
        db_access.delete_keyword(conn, args)
        return await ctx.send(str(ctx.message.author.mention) + " removed keyword: \"" + args + "\".")
    else:
        return await ctx.send(str(ctx.message.author.mention) + " \"" + args + "\" is not a keyword.")


@commands.command(name="addresponse")
async def add_response(ctx: commands.Context, args):
    if not util.user_is_admin(ctx.author.id):
        return await ctx.send(str(ctx.message.author.mention) + ", you are not authorized.")
    conn = db_access.create_connection()
    try:
        db_access.add_response(conn, args)
        return await ctx.send(str(ctx.message.author.mention) + " added keyword: \"" + args + "\".")
    except sqlite3.IntegrityError:
        return await ctx.send(str(ctx.message.author.mention) + ", this response already exists")


@commands.command(name="deleteresponse")
async def delete_response(ctx: commands.Context, args):
    if not util.user_is_admin(ctx.author.id):
        return await ctx.send(str(ctx.message.author.mention) + ", you are not authorized.")
    conn = db_access.create_connection()
    if db_access.is_response(args):
        db_access.delete_response(conn, args)
        return await ctx.send(str(ctx.message.author.mention) + " removed response: \"" + args + "\".")
    else:
        return await ctx.send(str(ctx.message.author.mention) + " \"" + args + "\" is not a response*.")


@commands.command()
async def roll(ctx):
    await ctx.send(str(ctx.message.author.mention) + " rolled: " + str(random.randint(1, 6)))


@commands.command(name="pickcard")
async def pick_card(ctx):
    cards = []
    for file in os.listdir(const.CARD_DIR):
        cards.append(file)
    await ctx.send(file=discord.File(os.path.join(const.CARD_DIR, cards[random.randint(0, len(cards)-1)])))


@commands.command(name="catfact")
async def random_cat_fact(ctx):
    response = requests.get("https://cat-fact.herokuapp.com/facts").text
    facts = json.loads(response)
    fact = facts["all"][random.randint(0, len(facts["all"]))-1]
    await ctx.send(fact["text"])


@commands.command(name="weather")
async def get_weather_report(ctx, args):
    response = requests.get(const.WEATHER_API.replace("CITY_NAME", args).replace("API_KEY", config.weather_key))
    weatherReport = json.loads(response.text)
    if "cod" in weatherReport and weatherReport["cod"] is "404":
        await ctx.send("Location not found!")
    else:
        await ctx.send("Weather report for: " + weatherReport["name"] +
                       "\n---\nWeather: " + weatherReport["weather"][0]["description"] +
                       "\nTimezone offset: " + str(weatherReport["timezone"]) +
                       "\nTemperature: " + str(float("{:.2f}".format(weatherReport["main"]["temp"] - 273.15))) + "°C"
                       )


@commands.command(name="read")
async def read_image(ctx):
    for arg in ctx.args:
        for attachment in arg.message.attachments:
            for ext in pic_ext:
                if attachment.url.endswith(ext):
                    try:
                        response = requests.get(attachment.url, stream=True)
                        image_data = io.BytesIO(response.raw.read())
                        content = pytesseract.image_to_string(Image.open(image_data))
                        print(content)
                        if str(content) is not None:
                            await ctx.send("```" + str(content) + "```")
                        else:
                            await ctx.send("No text found!")
                    except IndexError:
                        await ctx.send("Image invalid")
                        pass


@commands.command(name="scramble")
async def scramble_nick(ctx):
    name = ctx.author.name
    scrambled = util.scramble_consonants(name)
    await member.edit(nick=scrambled)
