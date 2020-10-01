import json
import os

from src import const


class Config:
    def __init__(self):
        self.token = ""
        self.weather_key = ""
        self.tesseract_location = ""
        self.owner_id = ""

        if not self.config_exist():
            self.create_config()
        config = json.loads(open(const.CONFIG_FILE, "r").read())
        self.read_properties(config)

    def read_properties(self, config):
        self.token = config["token"]
        self.weather_key = config["weather_key"]
        self.tesseract_location = config["tesseract_location"]
        self.owner_id = config["owner_id"]

    @staticmethod
    def config_exist() -> bool:
        return os.path.exists(const.CONFIG_FILE)

    @staticmethod
    def create_config():
        config = open(const.CONFIG_FILE, "w+")
        newConfig = {"token": "PLACEHOLDER",
                     "weather_key": "PLACEHOLDER",
                     "tesseract_location": "PLACEHOLDER",
                     "owner_id": "PLACEHOLDER"}
        json.dump(newConfig, config, indent=2)
        print('Empty config file generated.')
