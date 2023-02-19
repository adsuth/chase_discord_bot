from dotenv import load_dotenv
import os

load_dotenv()
TOKEN                       = os.getenv( "TOKEN" )
SERVER_ID                   = int( os.getenv( "SERVER_ID" ) )
CHASE_VGM_SCOREBOARD_ID     = os.getenv( "CHASE_VGM_SCORBOARD_ID" )
CHASE_VGM_SCOREBOARD_RANGE  = os.getenv( "CHASE_VGM_SCOREBOARD_RANGE")

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

SCORES = {}

class COLORS:
  error = 0xff4063
  red   = 0xff4063
  score = 0xffd22e
  subs  = 0x2eff43