import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.checks import NEED_ADMIN, error_embed, has_access
from utils.text import format_mentions


class SayModal(discord.ui.Modal, title="Say Publish"):
    message = discord.ui.TextInput(
        label="Message",
        placeholder="Write something...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=4000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        text = self.message.value
        await interaction.response.defer()
        formatted = format_mentions(interaction.guild, text)
        await interaction.channel.send(formatted if formatted.strip() else text)


class Say(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="say", description="Say anything!!")
    @app_commands.guild_only()
    async def say(self, interaction: discord.Interaction):
        if not has_access(interaction.user, config.SAY_ROLE_IDS):
            return await interaction.response.send_message(
                embed=error_embed(NEED_ADMIN), ephemeral=True
            )
        await interaction.response.send_modal(SayModal())

    @app_commands.command(name="say-normal", description="Say anything!!")
    @app_commands.describe(message="type the content of message!!")
    @app_commands.guild_only()
    async def say_normal(self, interaction: discord.Interaction, message: str):
        if not has_access(interaction.user, config.STAFF_ROLE_IDS):
            return await interaction.response.send_message(
                embed=error_embed(NEED_ADMIN), ephemeral=True
            )
        await interaction.channel.send(message)
        await interaction.response.send_message(
            f"The message is successfully sent [{config.EMOJIS['success']}]",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Say(bot))
