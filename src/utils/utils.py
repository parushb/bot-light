import json
from pathlib import Path
from discord.ext import commands
import requests


def return_default_config():
    with open(Path(__file__).parent.parent / 'utils/files/config.json') as f:
        return json.loads(f.read())


def return_cmd_config():
    with open(Path(__file__).parent.parent / 'utils/files/cmds.json') as f:
        return json.load(f)


cmdCfg = return_cmd_config()
config = return_default_config()


def is_enabled(group):
    if cmdCfg[group]["enabled"]:
        return True
    else:
        return False


def get_meme(memes):
    # get memmes from tenor api

    url = f'https://api.tenor.com/v1/search?q={memes}&key={config["tenor"]["key"]}&limit={config["tenor"]["limit"]}'
    r = requests.get(url)
    if r.status_code == 200:
        data = json.loads(r.content)
        return data
