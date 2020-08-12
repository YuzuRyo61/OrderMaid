from . import OM_BOT


@OM_BOT.check
async def checker(ctx):
    if ctx.guild.owner == ctx.message.author:
        return True
    elif ctx.message.author.guild_permissions.administrator:
        return True
    else:
        return False
