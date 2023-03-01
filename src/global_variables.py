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
ADMIN_ROLE_IDS = [
  1079849502313291927,   # test enviro admin
  # 520207923763347471,    # Quizmaster - Quetz
]

BOT_ALLOWED_CHANNELS = [
  1079817162685956176  # debug
]

CHANNELS = {
  "test_register": 1080278638286622791
}

DEBUG_LOGGING_INCLUDED    = True
IN_DEBUG_MODE             = False
ERROR_HANDLING_ENABLED    = False

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

  #  Alias( "Retro", AliasType.CHASER ):         Alias( "retronika", AliasType.PLAYER ), # removed as her player 
   Alias( "The Composer", AliasType.CHASER ):  Alias( "JNuts24", AliasType.PLAYER ),
   
  #  Alias( "The Boss", AliasType.CHASER ):      Alias( "???", AliasType.PLAYER ), # TODO: Determine proper username
  #  Alias( "Maestro", AliasType.CHASER ):       Alias( "???", AliasType.PLAYER ), # TODO: Determine proper username
  #  Alias( "Quetz", AliasType.CHASER ): Alias( "TheChaseVGM", AliasType.PLAYER ), # TODO: Determine if Quetz has row entry...
  
})

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

