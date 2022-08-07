import asyncpg
import asyncio
from pathlib import Path
import sqlite3

def base_path(file):
    return Path(__file__).parent.absolute()/ file

GUILD_CONFIG_FILE = base_path(file="local_files/guild_config.db")

async def load_config_data():
    db = await asyncpg.connect("postgresql://bot_manager@localhost/bot_server")

    local_db = sqlite3.connect(GUILD_CONFIG_FILE)
    bot_table_list = await db.execute("SELECT * FROM guild_config")

    print(bot_table_list)
    local_db.close()
    await db.close()

