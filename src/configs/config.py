from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/.env")


class CoreConfig:
    PREFIX = "!"
    enabled_commands = [
        "profile",
        "ban",
        "unban",
        "mute",
        "unmute",
        "translate",
        "meme",
        "prefix",
        "kick",
        "clear"
    ]
    OWNER_ID = 756144925086711905
    TOKEN: str = os.getenv("TOKEN")
    CLIENT_ID: int = os.getenv("CLIENT_ID")
    GUILD_ID = int(os.getenv("GUILD_ID"))


class Tenor:
    API_KEY = os.getenv("TENOR_KEY")
    LIMIT = 2


class Dev:
    LOGGING_CHANNEL = 983218934088101969
    developers = [756144925086711905]
