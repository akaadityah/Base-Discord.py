"""MongoDB connection (port of events/ready/mongodb.js).

The original only opened a mongoose connection and defined no models.
Here the Motor client is exposed as `bot.mongo` / `bot.db`.
"""
import os

from discord.ext import commands

from utils.log import green, red, yellow


class Database(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.mongo = None
        self.bot.db = None

    async def cog_load(self):
        uri = os.getenv("MongoURI")
        if not uri:
            print(yellow("[WARN]") + " Aborting MongoDB connection. (NO URI)")
            return
        try:
            from motor.motor_asyncio import AsyncIOMotorClient

            self.bot.mongo = AsyncIOMotorClient(uri, serverSelectionTimeoutMS=10_000)
            await self.bot.mongo.admin.command("ping")
            self.bot.db = self.bot.mongo.get_default_database(default="test")
            print(green("[MongoDB]") + " Connected to DB!")
        except Exception as err:
            print(red("[MongoDB ERR]") + f" DB ERR: \n{err}")

    async def cog_unload(self):
        if self.bot.mongo:
            self.bot.mongo.close()
            print(red("[MongoDB]") + " Disconnected from DB.")


async def setup(bot: commands.Bot):
    await bot.add_cog(Database(bot))
