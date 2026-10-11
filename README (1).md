<div align="center">

# 🦅 Base Bot

**A clean, cog-based Discord moderation & publishing bot built on `discord.py` 2.x**

Announcements · Say · Attachments · Embeds · Direct Messages

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-2.4%2B-5865F2?logo=discord&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-optional-47A248?logo=mongodb&logoColor=white)
![Slash Commands](https://img.shields.io/badge/Commands-Slash-brightgreen)

Made by **[@akaadityah](https://github.com/akaadityah)**

</div>

---

## Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Commands](#-commands)
- [Permissions](#-permissions)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Discord Developer Portal Setup](#-discord-developer-portal-setup)
- [Running the Bot](#-running-the-bot)
- [Extending the Bot](#-extending-the-bot)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Credits](#-credits)

---

## Overview

**Base Bot** gives your staff team a polished way to publish content in any channel as the bot: announcements with a role ping, plain messages, messages with attachments, custom embeds with link buttons, and DMs to members. Everything is driven by slash commands and modals, with role-based access control so only the right people can use each command.

It is a Python / `discord.py` rewrite of the original discord.js base handler, restructured around **cogs** so adding a feature is as simple as dropping a file into `cogs/`.

---

## Features

| | Feature | Details |
|---|---|---|
| 📢 | **Announcements** | Modal-based announcement with a themed embed, random banner GIF, IST timestamp, and automatic role ping |
| 💬 | **Say (modal)** | Multi-line message through a modal; `@name` is converted to a real role/user mention |
| ⚡ | **Say (quick)** | One-line `/say-normal` for fast messages |
| 📎 | **Say with attachment** | Upload a file, write a message in a modal, bot posts both |
| 🧩 | **Embed builder** | Title, description, footer, image, thumbnail, author, optional content, and a link button with emoji |
| ✉️ | **Direct messages** | Admin-only branded DM to any user, with graceful handling of closed DMs |
| 🔐 | **Role-based access** | Administrator **or** a configured staff role |
| 🧱 | **Auto-loading cogs** | Every `.py` file in `cogs/` is loaded on startup |
| 🛡️ | **Global error handler** | Friendly ephemeral error embed + full traceback in the console |
| 🗄️ | **Optional MongoDB** | Async `motor` client exposed as `bot.db` when `MongoURI` is set |
| 🔘 | **Persistent components** | Ready-to-fill templates for buttons & select menus that survive restarts |

---

## Commands

| Command | Options | Who can use it | What it does |
|---|---|---|---|
| `/announcement` | — | Admin or staff roles | Opens a modal, then posts a themed **Announcement** embed and pings the announcement role |
| `/say` | — | Admin or the *say* role | Opens a modal and posts the message. `@RoleName` / `@username` become real mentions |
| `/say-normal` | `message` | Admin or staff roles | Posts the message exactly as typed |
| `/say-attachment` | `attachment` | Admin or staff roles | Opens a modal for the message, then posts it with the uploaded file |
| `/dm` | `user`, `message` | Admin only | Sends a branded embed DM to the selected user |
| `/embed` | `description` *(required)*, `title`, `footer`, `image`, `thumbnail`, `message`, `author`, `button_label`, `button_url`, `button_emoji` | Admin only | Builds and posts a custom embed, optionally with a link button |

All commands are **guild-only** and every confirmation/error reply is **ephemeral** (only the invoker sees it).

### Smart mentions

In `/say` and `/say-attachment`, write `@name` and the bot resolves it for you:

1. `@everyone` / `@here` are kept as is
2. A **role** whose name matches (case-insensitive) becomes a role mention
3. Otherwise a **member** whose username or display name matches becomes a user mention
4. If nothing matches, you get `**[name not found]**` so typos are obvious

---

## Permissions

Access is checked in code (`utils/checks.py`) using the IDs in `config.py`:

| Group | Config key | Used by |
|---|---|---|
| Staff roles | `STAFF_ROLE_IDS` | `/announcement`, `/say-normal`, `/say-attachment` |
| Say role | `SAY_ROLE_IDS` | `/say` |
| Admin only | *(Administrator permission)* | `/dm`, `/embed` |

Members with the **Administrator** permission always pass. Replace the example IDs in `config.py` with your own server's role IDs.

### Bot permissions required

In the channels where the bot posts: **View Channel**, **Send Messages**, **Embed Links**, **Attach Files**, **Mention Everyone** (needed for role pings).

---

## Project Structure

```text
base_py/
├── bot.py                 # Entry point: client setup, cog loader, command sync, error handler
├── config.py              # Colours, emojis, role IDs, announcement settings
├── requirements.txt
├── .env.example           # Copy to .env and fill in
├── cogs/
│   ├── announcement.py    # /announcement + modal
│   ├── say.py             # /say (modal) and /say-normal
│   ├── attachment.py      # /say-attachment + modal
│   ├── embed.py           # /embed builder
│   ├── dm.py              # /dm
│   ├── components.py      # Persistent button & select-menu templates
│   └── database.py        # Optional MongoDB (motor) connection
└── utils/
    ├── checks.py          # Permission helpers + error embed
    ├── text.py            # @mention formatter
    └── log.py             # Coloured console output
```

---

## Installation

**Requirements:** Python **3.10+** and a Discord bot application.

```bash
# 1. Get the code
cd base_py

# 2. (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Configuration

### 1. Environment variables

```bash
cp .env.example .env
```

| Variable | Required | Description |
|---|---|---|
| `Token` | ✅ | Your bot token from the Developer Portal |
| `ClientID` | ✅ | Your application (client) ID |
| `MongoURI` | ❌ | MongoDB connection string. Leave empty to skip the database |

> ⚠️ **Never commit `.env` or share your token.** If a token is ever exposed, reset it immediately in the Developer Portal.

### 2. `config.py`

| Setting | Purpose |
|---|---|
| `EMBED_COLOR` | Default embed colour (`#ffffce`) |
| `ERROR_COLOR` / `SUCCESS_COLOR` | Colours for error / success embeds |
| `EMOJIS` | Success and error emojis used in replies |
| `STAFF_ROLE_IDS` | Roles allowed to use staff commands |
| `SAY_ROLE_IDS` | Roles allowed to use `/say` |
| `ANNOUNCEMENT_PING_ROLE_ID` | Role pinged by `/announcement` |
| `ANNOUNCEMENT_GIFS` | Banner image(s); one is chosen at random per announcement |

The announcement branding ("Eagle Gaming", footer text) is set in `cogs/announcement.py`, and the DM/embed author branding ("base") in `cogs/dm.py` and `cogs/embed.py`. Change these to match your server.

---

## Discord Developer Portal Setup

1. Open the [Developer Portal](https://discord.com/developers/applications), create or select your application, and go to **Bot**.
2. Enable these **Privileged Gateway Intents**:
   - ✅ **Server Members Intent**
   - ✅ **Message Content Intent**
   - ✅ **Presence Intent**
3. Under **OAuth2 → URL Generator**, select scopes **`bot`** and **`applications.commands`**, add the permissions listed above, and use the generated link to invite the bot.

---

## Running the Bot

```bash
python bot.py
```

On startup you will see the cogs load, MongoDB connect (if configured), and the slash commands sync. Global commands can take a short while to appear the first time.

---

## Extending the Bot

### Add a command

Create `cogs/hello.py`. It is loaded automatically on the next start:

```python
import discord
from discord import app_commands
from discord.ext import commands


class Hello(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Say hello")
    @app_commands.guild_only()
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello! 👋", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Hello(bot))
```

### Add a modal

Subclass `discord.ui.Modal`, add `discord.ui.TextInput` fields, handle `on_submit`, and open it with `interaction.response.send_modal(...)`. See `cogs/say.py` for a minimal example.

### Add persistent buttons or select menus

Use `cogs/components.py` as a template: give each item a fixed `custom_id`, put them in a `View(timeout=None)`, and register it with `bot.add_view()` in `setup()`. For prefix-matched IDs (e.g. `district_123`), use `discord.ui.DynamicItem`.

### Use the database

When `MongoURI` is set, `self.bot.db` is a Motor database:

```python
await self.bot.db.users.update_one({"_id": user.id}, {"$set": {"seen": True}}, upsert=True)
```

---

## Deployment

Any host that can run a long-lived Python process works (VPS, Raspberry Pi, a bot host, Docker). Keep it running with a process manager, for example `systemd`:

```ini
[Unit]
Description=Base Discord Bot
After=network-online.target

[Service]
WorkingDirectory=/opt/base_py
ExecStart=/opt/base_py/.venv/bin/python bot.py
Restart=always
User=bot

[Install]
WantedBy=multi-user.target
```

Provide `Token`, `ClientID` and `MongoURI` through a `.env` file or the host's environment settings.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `PrivilegedIntentsRequired` on startup | Enable the three privileged intents in the Developer Portal (see above) |
| Slash commands don't show up | Re-invite with the `applications.commands` scope; wait a few minutes for global sync; restart Discord |
| `Missing Token in .env` | Make sure `.env` exists next to `bot.py` and uses the exact key `Token` |
| Role ping doesn't ping | Give the bot **Mention Everyone** permission, or make the role mentionable |
| `@name` says "not found" | Check the spelling; the Server Members intent must be enabled so the member cache is populated |
| `/dm` says DMs are closed | The user has server DMs disabled; nothing the bot can do |
| `Failed to load <cog>` in console | Read the traceback printed under it; usually a typo or missing dependency |
| MongoDB won't connect | Verify `MongoURI`, network access/IP allowlist, and that `motor` is installed |

---

## Credits

- **Developed and maintained by [@akaadityah](https://github.com/akaadityah)**
- Built with [discord.py](https://github.com/Rapptz/discord.py) and [Motor](https://github.com/mongodb/motor)
- Ported from the original discord.js base handler by NotSK

---

<div align="center">

**Made with ❤️ by [@akaadityah](https://github.com/akaadityah)**

</div>
