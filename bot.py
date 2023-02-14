
import hikari
import lightbulb
from dotenv import load_dotenv
import os
import requests as req
import csv

from functools import cache
from time import time
from pprint import pprint

load_dotenv()
TOKEN     = os.getenv( "TOKEN" )
CHASE_SCORES_SHEET_URI = os.getenv( "CHASE_SCORES_SHEET_URI" )
SERVER_ID = int( os.getenv( "SERVER_ID" ) )

CHASE_URI = f"https://docs.google.com/spreadsheets/d/{CHASE_SCORES_SHEET_URI}/export?format=csv"
SCOREBOARD = {}

bot = lightbulb.BotApp (
  token=TOKEN,
  intents=hikari.Intents.ALL,
  default_enabled_guilds=( SERVER_ID ) 
)

def parseScoreboard( lines ):
  output = {}
  
  for line in lines:
    if line[1] == "Round Points" or line[0] == "Total":
      continue
    
    name        = line[  0 ]
    key         = name.strip().lower()
    score       = line[ -1 ]
    
    output[ key ] = {
      "score":  int( score ),
      "name" :  name
    }

  return output

def func_timer( func ):
  """
  Decorator that returns the time taken for a function to complete
  """
  def wrapper():
    start_time = time()
    output = func()
    end_time   = time()
    
    print( f"Total time to run {func.__name__} >> {end_time - start_time}" )
    return output
  return wrapper

@bot.command
@lightbulb.option( "player", "Player's Twitch username" )
@lightbulb.command( "score", "Retrieves a player's score from the scoreboard" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_score( ctx ):
  query = ctx.options.player.strip().lower()
  player_data = SCOREBOARD.get( query )
  
  # break: player not found
  if player_data == None:
    await ctx.respond( f"Unable to find player: \"{query}\"" )
    return
  
  score = player_data.get( "score" )
  name  = player_data.get( "name" )
  
  await ctx.respond( f"{name}'s score >> {score} points" )


def main():
  global SCOREBOARD
  
  # get the scoreboard
  with req.Session() as sesh:
    file = sesh.get( CHASE_URI )
    
    decoded = file.content.decode( "utf-8" )  
    
    cr = csv.reader( decoded.splitlines(), delimiter="," )
    my_list = list( cr )
    
  SCOREBOARD = parseScoreboard( my_list )
  
  bot.run()
  
main()