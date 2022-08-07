import asyncpg
import asyncio


async def register_guild_users(bot, user_list: list, guild_id: int):
    db = bot.db
    await db.execute(f"""
        CREATE TABLE IF NOT EXISTS "{guild_id}"(
            number SERIAL,
            user_id BIGINT PRIMARY KEY,
            level INTEGER DEFAULT 0,
            xp INTEGER DEFAULT 0,
            commands_ran INTEGER DEFAULT 0 
        )""")

    for i in range(len(user_list)):
        await db.execute(f"""
            INSERT INTO "{guild_id}"(user_id) VALUES($1)
            """, user_list[i])

    await db.close()


async def delete_guild_users(bot, guild_id: int):
    db = bot.db
    await db.execute(f"""
        DROP TABLE "{guild_id}"
        """)

    await db.close()


async def get_val(bot, column, table, where):
    db = bot.db
    val = db.execute(f"""
    SELECT {column} FROM {table} WHERE {where}
    """)
    await db.close()
    return val


async def add_member(bot, guild_id, member_id):
    db = bot.db
    db.execute(f"""
    INSERT INTO {guild_id}(user_id) VALUES({member_id})
    """)
    db.close()


async def remove_member(bot, guild_id, member_id):
    db = bot.db
    db.execute(f"""""")
