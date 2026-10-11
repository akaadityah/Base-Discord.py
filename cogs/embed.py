from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.checks import is_admin


class EmbedCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="embed", description="Build a custom embed message")
    @app_commands.describe(
        description="Description of the embed",
        title="Title of the embed",
        footer="Footer text of the embed",
        image="Select an attachment!!",
        thumbnail="Select an attachment!!",
        message="Mention role, user, custom message",
        author="Include embed author",
        button_label="Label of the button",
        button_url="URL of the button",
        button_emoji="Emoji for the button",
    )
    @app_commands.guild_only()
    async def embed(
        self,
        interaction: discord.Interaction,
        description: str,
        title: Optional[str] = None,
        footer: Optional[str] = None,
        image: Optional[discord.Attachment] = None,
        thumbnail: Optional[discord.Attachment] = None,
        message: Optional[str] = None,
        author: Optional[bool] = None,
        button_label: Optional[str] = None,
        button_url: Optional[str] = None,
        button_emoji: Optional[str] = None,
    ):
        await interaction.response.defer(ephemeral=True)

        if not is_admin(interaction.user):
            return await interaction.followup.send(
                embed=discord.Embed(
                    colour=discord.Colour.from_str("#FF0000"),
                    description="🔴 **You need `Administrator` to use this command!**",
                )
            )

        guild = interaction.guild
        embed = discord.Embed(description=description, colour=config.EMBED_COLOR)

        if author:
            embed.set_author(
                name="base", icon_url=guild.icon.url if guild.icon else None
            )
        if title:
            embed.title = title
        if footer:
            embed.set_footer(text=footer)
            embed.timestamp = discord.utils.utcnow()
        if image:
            embed.set_image(url=image.url)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail.url)

        view = discord.utils.MISSING
        if button_label and button_url:
            view = discord.ui.View()
            view.add_item(
                discord.ui.Button(
                    style=discord.ButtonStyle.link,
                    label=button_label,
                    url=button_url,
                    emoji=button_emoji or None,
                )
            )

        await interaction.followup.send("Published")
        await interaction.channel.send(content=message or None, embed=embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(EmbedCog(bot))
