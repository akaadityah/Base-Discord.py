import asyncio
import os
import traceback
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

import config
from utils.log import blue, green, red, yellow

load_dotenv()


class Base(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()  # guilds, guild_messages, voice_states, dm_messages, ...
        intents.members = True          # GuildMembers   (privileged)
        intents.message_content = True  # MessageContent (privileged)
        intents.presences = True        # GuildPresences (privileged)

        app_id = os.getenv("ClientID")
        super().__init__(
            command_prefix=commands.when_mentioned,  # slash-only bot
            intents=intents,
            application_id=int(app_id) if app_id else None,
            activity=discord.CustomActivity(name="Hey there ."),
            status=discord.Status.online,
        )
        self.config = config

    async def setup_hook(self):
        self.tree.on_error = self.on_app_command_error

        # Auto-load every cog in ./cogs (replaces the JS folder-scanning handlers).
        for path in sorted(Path(__file__).parent.joinpath("cogs").glob("*.py")):
            if path.name.startswith("_"):
                continue
            try:
                await self.load_extension(f"cogs.{path.stem}")
            except Exception:
                print(red(f"[COGS] Failed to load {path.name}"))
                traceback.print_exc()

        count = len(self.tree.get_commands())
        print(red("[COMMANDS]") + f" Started refreshing {count} application ( / ) commands")
        try:
            await self.tree.sync()
            print(green("[COMMANDS]") + f" Successfully refreshed {count} application ( / ) commands")
        except Exception as err:
            print(red(f"Error while registering application commands: \n{err}"))


    async def on_ready(self):
        print(blue(str(self.user)) + " is online!")

    async def on_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        original = getattr(error, "original", error)
        traceback.print_exception(type(original), original, original.__traceback__)

        embed = discord.Embed(
            colour=config.ERROR_COLOR,
            title="An Error Occured While Using This Command.",
            description=f"Please report this error: \n```py\n{original}```",
        )
        if interaction.response.is_done():
            await interaction.followup.send(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def main():
    token = os.getenv("Token")
    if not token:
        raise SystemExit("Missing `Token` in .env")
    async with Base() as bot:
        await bot.start(token)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
