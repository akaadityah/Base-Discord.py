import re

import discord

_MENTION_RE = re.compile(r"@([\w.\-_]+)", re.IGNORECASE | re.ASCII)


def format_mentions(guild: discord.Guild, text: str) -> str:
    """Turn @name into a real role/user mention (role name first, then
    username / display name). Unknown names become **[name not found]**."""

    def repl(m: re.Match) -> str:
        name = m.group(1)
        lowered = name.lower()
        if lowered in ("everyone", "here"):
            return f"@{name}"

        role = next((r for r in guild.roles if r.name.lower() == lowered), None)
        if role:
            return role.mention

        member = next(
            (
                mem
                for mem in guild.members
                if mem.name.lower() == lowered or mem.display_name.lower() == lowered
            ),
            None,
        )
        if member:
            return member.mention

        return f"**[{name} not found]**"

    return _MENTION_RE.sub(repl, text)
