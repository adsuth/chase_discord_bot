# ------------------------------------------- #
#     Global Variables
# ------------------------------------------- #
# 
# Contains IMMUTABLE global variables (see config for mutable vars)
# 

from dotenv import load_dotenv
import os

from classes import Alias, AliasType, duodict

load_dotenv()
TOKEN                       = os.getenv( "TOKEN" )
SERVER_ID                   = int( os.getenv( "SERVER_ID" ) )
CHASE_VGM_SCOREBOARD_ID     = os.getenv( "CHASE_VGM_SCOREBOARD_ID" )
CHASE_VGM_SCOREBOARD_RANGE  = os.getenv( "CHASE_VGM_SCOREBOARD_RANGE" )

NON_BREAK_SPACE             = "** **"
NO_OF_SCORE_DATA_COLUMNS    = 20
MAX_NO_OF_SELECT_OPTIONS    = 25

"""Can add permissions if needed (eg, if Chasers should be able to refresh data)"""
# unused
ADMIN_ROLES = [
  520207923763347471,    # Quizmaster - Quetz
]

# unused
CHANNELS = {
  "register_channel": 1080278638286622791,  # This is where register requests are sent (should be hidden, accessible only to Quetz)
  "bot_channel":      1079817162685956176,  # This is where commands can be used
}

DEBUG_LOGGING_INCLUDED    = False
IN_DEBUG_MODE             = False
ERROR_HANDLING_ENABLED    = False

PATH_TO_LEGACY_GAME_LIST  = "./src/public/legacy_games.txt"

CHASER_ALIASES         = duodict({
   Alias( "Rogue", AliasType.CHASER ):        Alias( "marleebrianna", AliasType.PLAYER ),
   Alias( "The Artist", AliasType.CHASER ):   Alias( "DekuTri", AliasType.PLAYER ),
   Alias( "The Designer", AliasType.CHASER ): Alias( "Rensillius", AliasType.PLAYER ),
   
   Alias( "The Collector", AliasType.CHASER ): Alias( "Aakadarr", AliasType.PLAYER ),
   Alias( "The Machine", AliasType.CHASER ):   Alias( "CogBog", AliasType.PLAYER ),
   Alias( "The Detective", AliasType.CHASER ): Alias( "sut_son", AliasType.PLAYER ),

   Alias( "The Gunner", AliasType.CHASER ):    Alias( "deogenerate", AliasType.PLAYER ),
   Alias( "The Phantom", AliasType.CHASER ):   Alias( "MysteriousMrLeak", AliasType.PLAYER ),
   Alias( "The Sorcerer", AliasType.CHASER ):  Alias( "NamirrhaTheSorcerer", AliasType.PLAYER ),

   Alias( "The Composer", AliasType.CHASER ):  Alias( "JNuts24", AliasType.PLAYER ),
})

SCOPES = [ "https://www.googleapis.com/auth/spreadsheets.readonly" ]

