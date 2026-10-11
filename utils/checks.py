import discord

import config


def has_access(member: discord.abc.User, role_ids: set[int]) -> bool:
    """Administrator, or holding any of `role_ids`."""
    if not isinstance(member, discord.Member):
        return False
    if member.guild_permissions.administrator:
        return True
    return any(r.id in role_ids for r in member.roles)


def is_admin(member: discord.abc.User) -> bool:
    return isinstance(member, discord.Member) and member.guild_permissions.administrator


def error_embed(text: str) -> discord.Embed:
    return discord.Embed(
        colour=config.ERROR_COLOR,
        description=f"{config.EMOJIS['error']} **{text}**",
    )


NEED_ADMIN = "You need `Administrator` to use this command!"
