from os.path import join as join
import os

WEATHER_API = "http://api.openweathermap.org/data/2.5/weather?q=CITY_NAME&appid=API_KEY"
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = join(join(SRC_DIR, ".."), "resources")
IMAGES_DIR = join(RESOURCE_DIR, "images")
CARD_DIR = join(IMAGES_DIR, "cards")
CONFIG_DIR = join(RESOURCE_DIR, "config")
ADMINS = join(RESOURCE_DIR, "admins.json")
RESPONSE_DIR = join(RESOURCE_DIR, "responses")
KEYWORD_DIR = join(RESOURCE_DIR, "keywords")
FFMPEG_DIR = join(RESOURCE_DIR, "ffmpeg")
AUDIO_DIR = join(RESOURCE_DIR, "audio")
AUDIO_MEMES_DIR = join(AUDIO_DIR, "memes")
CONFIG_FILE = join(CONFIG_DIR, "config.json")
