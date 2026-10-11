import discord
from discord import app_commands
from discord.ext import commands

import config
from utils.checks import NEED_ADMIN, error_embed, has_access
from utils.text import format_mentions


class AttachmentModal(discord.ui.Modal, title="Attachment Publish"):
    message = discord.ui.TextInput(
        label="Message",
        placeholder="Write the reason...",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=4000,
    )

    def __init__(self, attachment: discord.Attachment):
        super().__init__()
        # The modal instance carries the attachment, so no global
        # attachmentStorage map is needed (unlike the JS version).
        self.attachment = attachment

    async def on_submit(self, interaction: discord.Interaction):
        text = self.message.value
        await interaction.response.defer()
        formatted = format_mentions(interaction.guild, text)
        file = await self.attachment.to_file()
        await interaction.channel.send(
            content=formatted if formatted.strip() else text, file=file
        )


class AttachmentCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="say-attachment", description="Send any attachments!!")
    @app_commands.describe(attachment="Select an attachment!!")
    @app_commands.guild_only()
    async def say_attachment(
        self, interaction: discord.Interaction, attachment: discord.Attachment
    ):
        if not has_access(interaction.user, config.STAFF_ROLE_IDS):
            return await interaction.response.send_message(
                embed=error_embed(NEED_ADMIN), ephemeral=True
            )
        await interaction.response.send_modal(AttachmentModal(attachment))


async def setup(bot: commands.Bot):
    await bot.add_cog(AttachmentCog(bot))
