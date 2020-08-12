#!/usr/bin/env python3

"""
OrderMaid - Created by YuzuRyo61

Administrative support utilities for Discord server (guild)

@license: MIT
"""
import logging

from ordermaid import OM_BOT, OM_CONFIG
from ordermaid.cogs import UserManage

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    cogs = [
        UserManage(OM_BOT)
    ]
    for cog in cogs:
        OM_BOT.add_cog(cog)
    OM_BOT.run(OM_CONFIG["client"]["token"])
