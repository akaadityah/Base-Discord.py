from datetime import datetime
from random import choice
from zoneinfo import ZoneInfo

import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.checks import NEED_ADMIN, error_embed, has_access


class AnnouncementModal(discord.ui.Modal, title="Announcement Publish"):
    message = discord.ui.TextInput(
        label="Message",
        placeholder="Write something...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=4000,
    )

    async def on_submit(self, interaction: discord.Interaction):
        bot = interaction.client
        now = datetime.now(ZoneInfo("Asia/Kolkata"))
        date = now.strftime("%d/%m/%Y")
        time = now.strftime("%I:%M %p").lstrip("0")  # e.g. 3:07 PM

        avatar = bot.user.display_avatar.url
        embed = (
            discord.Embed(
                title="Announcement",
                description=f"```{self.message.value}```",
                colour=config.EMBED_COLOR,
            )
            .set_author(name="Eagle Gaming", icon_url=avatar)
            .set_thumbnail(url=avatar)
            .set_image(url=choice(config.ANNOUNCEMENT_GIFS))
            .set_footer(text=f"Eagle Gaming™ • {date}, {time}", icon_url=avatar)
        )

        await interaction.response.defer()
        await interaction.channel.send(
            content=f"<@&{config.ANNOUNCEMENT_PING_ROLE_ID}>", embed=embed
        )


class Announcement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="announcement", description="Send announcement anything!!")
    @app_commands.guild_only()
    async def announcement(self, interaction: discord.Interaction):
        if not has_access(interaction.user, config.STAFF_ROLE_IDS):
            return await interaction.response.send_message(
                embed=error_embed(NEED_ADMIN), ephemeral=True
            )
        await interaction.response.send_modal(AnnouncementModal())


async def setup(bot: commands.Bot):
    await bot.add_cog(Announcement(bot))
