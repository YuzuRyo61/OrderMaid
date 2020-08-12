"""
OrderMaid internal package
"""

import logging
import discord
import dataset
from discord.ext import commands

from .config import OM_CONFIG

__version__ = "0.0.0"

OM_DB = dataset.connect(OM_CONFIG["database"]["url"])

OM_BOT = commands.Bot(
    command_prefix=commands.when_mentioned_or("om "),
    activity=discord.Game("OrderMaid")
)


from .checker import checker  # noqa: F401, E402


def get_oauth_url():
    return discord.utils.oauth_url(
        OM_CONFIG["client"]["client_id"],
        permissions=discord.Permissions(
            administrator=True
        )
    )


@OM_BOT.event
async def on_ready():
    logging.info(f"{OM_BOT.user} is getting ready")
    if len(OM_BOT.guilds) == 0:
        logging.warning(
            "Bot is not joined any guilds. Please join first guild.")

    logging.info(f"Add bot URL: {get_oauth_url()}")


@OM_BOT.event
async def on_guild_join(guild):
    logging.info(f"New guild joined: {guild.name} ({guild.id})")
    if len(guild.text_channels) > 0:
        embed = discord.Embed(
            title="Thank you adding OrderMaid!",
            description="This bot's command prefix is `om `.",
            color=discord.Colour.green()
        )
        embed.set_author(
            name="OrderMaid",
            url="https://github.com/YuzuRyo61/OrderMaid"
        )
        embed.set_footer(
            text=f"OrderMaid version: {__version__}"
        )
        try:
            await guild.text_channels[0].send(embed=embed)
        except (discord.Forbidden, discord.HTTPException):
            logging.error(
                "Can't send message. It may not enough permission.")


@OM_BOT.command()
@commands.is_owner()
async def add_server(ctx):
    try:
        await ctx.message.author.send(
            get_oauth_url()
        )
    except discord.Forbidden:
        await ctx.send(
            f"{ctx.message.author.mention} "
            "Can't send message to your DM. "
            "Please enable DM privacy from server's privacy setting.")


@OM_BOT.event
async def on_command_error(ctx, error):
    logging.warning(f"on_command_error: {str(error)} ({type(error)})")
    if isinstance(error, commands.CheckFailure) or \
            isinstance(error, commands.NotOwner):
        embed = discord.Embed(
            title="Forbidden",
            description=f"You don't have permission in {ctx.guild}",
            color=discord.Colour.red()
        )
        await ctx.send(
            ctx.message.author.mention,
            embed=embed
        )
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="Not Found",
            description="This command is not found.",
            color=discord.Colour.red()
        )
        await ctx.send(
            ctx.message.author.mention,
            embed=embed
        )
    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(
            title="Internal error",
            description=(
                "It occurred error in internal system.\n"
                f"`{str(error)}`"
            ),
            color=discord.Colour.dark_purple()
        )
        await ctx.send(
            embed=embed
        )

__all__ = [
    "OM_BOT",
    "OM_CONFIG",
    "get_oauth_url"
]
