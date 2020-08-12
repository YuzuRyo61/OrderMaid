from discord.ext import commands


def is_administrator():
    async def predicate(ctx):
        if ctx.guild.owner == ctx.message.author:
            return True
        elif ctx.message.author.guild_permissions.administrator:
            return True
        else:
            return False
    return commands.check(predicate)


def is_guild():
    async def predicate(ctx):
        return ctx.guild is not None
    return commands.check(predicate)
