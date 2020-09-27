import io
import json
import os
import random
from time import sleep
import discord
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import requests
from discord.ext import commands
import src.util as util
from src import const, config
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


@commands.command(name="spam")
async def spam(ctx: commands.Context, target):
    spam_count = 5
    for x in range(spam_count):
        await sleep(0.1)
        await ctx.send(target)


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
