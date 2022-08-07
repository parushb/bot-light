from discord.ext import commands
from configs.config import CoreConfig, Dev
import discord
import asyncio
import os
import asyncpg
import logging


# async def databse_pool(bot):
#     try:
#         bot.db = await asyncpg.connect("postgresql://bot_manager@localhost/bot_server")
#     except Exception as e:
#         await log(bot, f"Connecting to database failed!\n {e}")


async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(CoreConfig.PREFIX)(bot, message)

    prefix = await bot.db.fetch(f"""
        SELECT prefix FROM guild_config WHERE guild_id = {message.guild.id}
    """)
    if len(prefix) == 0:
        await bot.db.execute(f"""
            INSERT INTO guild_config(guild_id, prefix) VALUES({message.guild.id},{CoreConfig.PREFIX})
        """)
        prefix = CoreConfig.PREFIX
    else:
        prefix = prefix[0].get("prefix")
    return commands.when_mentioned_or(prefix)(bot, message)


def logger() -> logging.Logger:
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    handler = logging.FileHandler('broken.log')
    handler.setFormatter(logging.Formatter('%(levelname)s:%(name)s: %(message)s'))
    log.addHandler(handler)
    return log


async def log(bot, message):
    channel = bot.get_channel(Dev.LOGGING_CHANNEL)
    await channel.send(f"```{message}```")


def main():
    # Check for some basic errors
    if CoreConfig.TOKEN == "":
        return "Please set the bot token in configs/config.py"

    elif CoreConfig.PREFIX == "":
        return "Please set the bot prefix in configs/config.py"

    # set the bot intents
    intents = discord.Intents.default()
    intents.guilds = True
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix=CoreConfig.PREFIX, intents=intents)
    bot.owner_id = CoreConfig.OWNER_ID

    @bot.command(name="shut")
    async def _stop(ctx: commands.Context, *, key: str):
        if ctx.author.id == CoreConfig.OWNER_ID:
            await bot.db.close()
            await bot.close()
        else:
            await ctx.send('You are not the owner of the bot')

    asyncio.run(load_cogs(bot))  # load the bot modules

    async def run():
        async with bot:
            print(CoreConfig.TOKEN)
            await bot.start(CoreConfig.TOKEN)

    # Run the bot
    asyncio.run(run())


async def load_cogs(bot):
    for filename in os.listdir("./src/cogs/"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded cogs.{filename[:-3]}")

    for filename in os.listdir("./src/cogs/moderation/"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.moderation.{filename[:-3]}")
            print(f"Loaded cogs.moderation.{filename[:-3]}")

    for filename in os.listdir("./src/cogs/dev/"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.dev.{filename[:-3]}")
            print(f"Loaded cogs.moderation.{filename[:-3]}")

    for filename in os.listdir("./src/cogs/apis/"):
        if filename.endswith(".py") and not filename.startswith("_"):
            await bot.load_extension(f"cogs.apis.{filename[:-3]}")
            print(f"Loaded cogs.apis.{filename[:-3]}")

    # for py_file in os.walk(f'cogs'):
    #     for py_file in os.walk(f"{py_file}/"):
    #         if py_file.endswith('.py') and not py_file.startswith('_'):
    #             py_file = py_file[:-3]
    #             print(py_file)
    #             print(f"Loaded " + py_file.replace('\\', '.'))
    #             bot.load_extension("cogs." + py_file.replace('\\', '.'))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
