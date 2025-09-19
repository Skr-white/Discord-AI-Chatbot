import os, logging
from typing import Any
import discord
from discord.ext import commands
from dotenv import load_dotenv
from cogs import COMMANDS, EVENT_HANDLERS
from bot_utilities.config_loader import config

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("discord")

load_dotenv(".env")

class AIBot(commands.AutoShardedBot):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if config.get("AUTO_SHARDING", False):
            super().__init__(*args, **kwargs)
        else:
            super().__init__(shard_count=1, *args, **kwargs)

    async def setup_hook(self) -> None:
        for cog in COMMANDS:
            try:
                await self.load_extension(cog)
                log.info(f"Loaded Command {cog.split('.')[-1]}")
            except Exception as e:
                log.error(f"Failed to load {cog}: {e}")
        for cog in EVENT_HANDLERS:
            try:
                await self.load_extension(cog)
                log.info(f"Loaded Event Handler {cog.split('.')[-1]}")
            except Exception as e:
                log.error(f"Failed to load {cog}: {e}")
        log.info("If syncing commands is taking longer than usual you may be rate limited")
        await self.tree.sync()
        log.info(f"Loaded {len(self.commands)} commands")

bot = AIBot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

TOKEN = os.getenv("DISCORD_TOKEN") or input("Please enter your Discord token: ")
bot.run(TOKEN, reconnect=True)