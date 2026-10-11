import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.checks import NEED_ADMIN, error_embed, is_admin


class DM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="dm", description="Dm to a user!!")
    @app_commands.describe(
        user="Select a user!!", message="type the content of message!!"
    )
    @app_commands.guild_only()
    async def dm(self, interaction: discord.Interaction, user: discord.User, message: str):
        if not is_admin(interaction.user):
            return await interaction.response.send_message(
                embed=error_embed(NEED_ADMIN), ephemeral=True
            )

        embed = discord.Embed(
            title="A Message From base Inbox",
            description=message,
            colour=config.EMBED_COLOR,
        ).set_footer(
            text="base",
            icon_url=interaction.guild.icon.url if interaction.guild.icon else None,
        )

        try:
            await user.send(content=user.mention, embed=embed)
        except discord.Forbidden:
            return await interaction.response.send_message(
                f"{config.EMOJIS['error']} Couldn't DM that user (their DMs are closed).",
                ephemeral=True,
            )

        await interaction.response.send_message(
            f"The direct-message is successfully sent [{config.EMOJIS['success']}]",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(DM(bot))
