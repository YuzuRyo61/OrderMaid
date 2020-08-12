import logging

import discord
from discord.ext import commands


class UserManage(commands.Cog, name="User Management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info("User Management cog is loaded.")

    @commands.command()
    async def fetch_user(self, ctx, target_id: int):
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
        if isinstance(error, commands.BadArgument):
            error_embed = discord.Embed(
                title="Bad Argument",
                description=(
                    "There are not enough arguments or "
                    "they are invalid arguments."
                ),
                color=discord.Colour.red()
            )
            error_embed.set_footer(
                text="OrderMaid"
            )
            await ctx.send(embed=error_embed)
            return
        elif isinstance(error, commands.MissingRequiredArgument):
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
            return
