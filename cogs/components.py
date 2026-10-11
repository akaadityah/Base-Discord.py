"""Persistent button / select-menu templates.

Port of src/buttons/base.js and src/aselect-menus/base.js, which were empty
placeholders keyed by custom_id "base". In discord.py a persistent component is
a View(timeout=None) whose items have fixed custom_ids and which is registered
with bot.add_view(); this replaces the JS customId -> handler maps.

For prefix-matched IDs (the JS handler special-cased "district_"), use
discord.ui.DynamicItem with a regex template instead.
"""
import discord
from discord.ext import commands


class BaseButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="base", custom_id="base", style=discord.ButtonStyle.secondary)

    async def callback(self, interaction: discord.Interaction):
        pass  # TODO: implement


class BaseSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            custom_id="base",
            placeholder="base",
            options=[discord.SelectOption(label="base", value="base")],
        )

    async def callback(self, interaction: discord.Interaction):
        pass  # TODO: implement


class BaseButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BaseButton())


class BaseSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BaseSelect())


async def setup(bot: commands.Bot):
    bot.add_view(BaseButtonView())
    bot.add_view(BaseSelectView())
