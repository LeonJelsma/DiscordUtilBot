from os.path import join as join
import os

WEATHER_API = "http://api.openweathermap.org/data/2.5/weather?q=CITY_NAME&appid=API_KEY"
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = join(join(SRC_DIR, ".."), "db")
DB_FILE = os.path.join(DB_DIR, 'db.db')
RESOURCE_DIR = join(join(SRC_DIR, ".."), "resources")
IMAGES_DIR = join(RESOURCE_DIR, "images")
CARD_DIR = join(IMAGES_DIR, "cards")
CONFIG_DIR = join(RESOURCE_DIR, "config")
ADMINS = join(RESOURCE_DIR, "admins.json")
RESPONSE_DIR = join(RESOURCE_DIR, "responses")
KEYWORD_DIR = join(RESOURCE_DIR, "keywords")
FFMPEG_DIR = join(RESOURCE_DIR, "ffmpeg")
FFMPG_EXE = join(join(FFMPEG_DIR, "bin"), "ffmpeg.exe")
AUDIO_DIR = join(RESOURCE_DIR, "audio")
UPLOADED_AUDIO_DIR = join(AUDIO_DIR, "uploaded")
AUDIO_MEMES_DIR = join(AUDIO_DIR, "memes")
CONFIG_FILE = join(CONFIG_DIR, "config.json")
