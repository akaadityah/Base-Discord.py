"""Central configuration (port of src/config.js)."""
import discord

EMBED_COLOR = discord.Colour.from_str("#ffffce")
ERROR_COLOR = discord.Colour.red()
SUCCESS_COLOR = discord.Colour.green()

EMOJIS = {"success": "✅", "error": "🚫"}

# Roles allowed to use /announcement, /say-normal and /say-attachment
# (in addition to members with Administrator).
STAFF_ROLE_IDS = {
    1314681643453251727,
    1314690514653810719,
    1314690652893745213,
    1318141854608523354,
}

# Roles allowed to use /say (in addition to Administrator).
SAY_ROLE_IDS = {642053972428849202}

# Role pinged by /announcement.
ANNOUNCEMENT_PING_ROLE_ID = 1314681735946047488

ANNOUNCEMENT_GIFS = [
    "https://r2.fivemanage.com/DFoKiwmVyTTIk1MRmQKVF/animated-line-image-0378.gif",
]
