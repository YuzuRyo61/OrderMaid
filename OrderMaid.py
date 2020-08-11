#!/usr/bin/env python3

"""
OrderMaid - Created by YuzuRyo61

Administrative utilities for Discord server (guild)

@license: MIT
"""
import logging

from ordermaid import OM_BOT, OM_CONFIG

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    OM_BOT.run(OM_CONFIG["client"]["token"])
