# ------------------------------------------- #
#     Global Variables
# ------------------------------------------- #
# 
# Contains IMMUTABLE global variables (see config for mutable vars)
# 

from dotenv import load_dotenv
import os

load_dotenv()
TOKEN                       = os.getenv( "TOKEN" )
SERVER_ID                   = int( os.getenv( "SERVER_ID" ) )
CHASE_VGM_SCOREBOARD_ID     = os.getenv( "CHASE_VGM_SCOREBOARD_ID" )
CHASE_VGM_SCOREBOARD_RANGE  = os.getenv( "CHASE_VGM_SCOREBOARD_RANGE")

DEBUG_LOGGING_INCLUDED = True

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
