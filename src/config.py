# ------------------------------------------- #
#     Config.py
# ------------------------------------------- #
# 
# Contains MUTABLE global variables ( set global_variables for IMMUTABLE ones )
# 

import hikari

bot : hikari.GatewayBot = None
DATABASE                = {}  # str -> Player
HANDLED_CHASERS         = []  # str
GAME_LIST               = []  # Submission