import logging
from typing import Optional

import discord
from discord.ext import commands

from ..checker import is_administrator, is_guild


class UserManage(commands.Cog, name="User Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("User Management cog is loaded.")

    @commands.command()
    @is_administrator()
    @is_guild()
    async def fetch_user(self, ctx, target_id: int):
        """
        Get user information.
        target_id: Specify the user ID of Discord.
                   Tips: The user ID can be copied when
                         the developer mode is enabled.
        """
        async with ctx.typing():
            try:
                target = await self.bot.fetch_user(target_id)
            except discord.NotFound:
                error_embed = discord.Embed(
                    title="Fetch failed",
                    description="The specified user ID was not found.",
                    color=discord.Colour.red()
                )
                error_embed.set_footer(
                    text="OrderMaid"
                )
                await ctx.send(embed=error_embed)
                return

            embed = discord.Embed(
                title="User Information",
                description=f"This is {str(target)}'s user information.",
                color=discord.Colour.blue()
            )
            embed.set_author(
                name=str(target),
                icon_url=str(target.avatar_url)
            )
            embed.add_field(
                name="User ID",
                value=str(target.id),
                inline=True
            )
            embed.add_field(
                name="Name",
                value=str(target.name),
                inline=True
            )
            embed.add_field(
                name="Discriminator",
                value=str(target.discriminator),
                inline=True
            )
            embed.add_field(
                name="Registered at (UTC)",
                value=target.created_at.strftime("%Y/%m/%d %H:%M:%S %A"),
                inline=True
            )
            embed.add_field(
                name="BOT",
                value="✅" if target.bot else "❎",
                inline=True
            )
            embed.add_field(
                name=f"{ctx.guild.name}'s member?",
                value="✅" if target in ctx.guild.members else "❎",
            )
            embed.set_footer(
                text="OrderMaid"
            )

            await ctx.send(embed=embed)

    @fetch_user.error
    async def fetch_user__error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = discord.Embed(
                title="Usage",
                description=(
                    "`om fetch_user <user_id:int>`"
                ),
                color=discord.Colour.red()
            )
            error_embed.set_footer(
                text="OrderMaid"
            )
            await ctx.send(embed=error_embed)

    @commands.command()
    @is_administrator()
    @is_guild()
    async def ban(self, ctx, target_id: int, *, reason: Optional[str] = None):
        """
        BAN the user.
        If you use this command, users who are not in
        this server (guild) can also perform BAN.
        target_id: Specify the user ID of Discord.
                   Tips: The user ID can be copied when
                         the developer mode is enabled.
        reason: It's optional. You can enter the reason for BAN.
                It does not matter if there is a space.
        """
        async with ctx.typing():
            try:
                target = await self.bot.fetch_user(target_id)
            except discord.NotFound:
                error_embed = discord.Embed(
                    title="Fetch failed",
                    description="The specified user ID was not found.",
                    color=discord.Colour.red()
                )
                error_embed.set_footer(
                    text="OrderMaid"
                )
                await ctx.send(embed=error_embed)
                return

            await ctx.guild.ban(
                target,
                reason=reason
            )

            embed = discord.Embed(
                title="BANNED",
                description=(
                    f"{target} is banned this server.\n"
                    f"Reason: {reason}"
                ),
                color=discord.Colour.dark_red()
            )
            embed.set_author(
                name=str(target),
                icon_url=str(target.avatar_url)
            )
            embed.add_field(
                name="User ID",
                value=str(target.id),
                inline=True
            )
            embed.add_field(
                name="Name",
                value=str(target.name),
                inline=True
            )
            embed.add_field(
                name="Discriminator",
                value=str(target.discriminator),
                inline=True
            )
            embed.add_field(
                name="Registered at (UTC)",
                value=target.created_at.strftime("%Y/%m/%d %H:%M:%S %A"),
                inline=True
            )
            embed.add_field(
                name="BOT",
                value="✅" if target.bot else "❎",
                inline=True
            )
            embed.set_footer(
                text="OrderMaid"
            )

            await ctx.send(embed=embed)

    @ban.error
    async def ban__error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = discord.Embed(
                title="Usage",
                description=(
                    "`om ban <user_id:int> [reason]`"
                ),
                color=discord.Colour.red()
            )
            error_embed.set_footer(
                text="OrderMaid"
            )
            await ctx.send(embed=error_embed)
