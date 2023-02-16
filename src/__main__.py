import hikari
import lightbulb

from pprint           import pprint

# My methods
from player_score     import PlayerScore
from global_variables import TOKEN
from global_variables import SERVER_ID
from global_variables import SCORES

from retrieve_sheet   import retrieve_values
from player_score     import parse_raw_scores

bot = lightbulb.BotApp (
  token=TOKEN,
  intents=hikari.Intents.ALL,
  default_enabled_guilds=( SERVER_ID ) 
)

@bot.command
@lightbulb.option( "player", "Player's Twitch username" )
@lightbulb.command( "score", "Retrieves a player's score from the scoreboard" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_score( ctx ):
  query = ctx.options.player.strip().lower()
  player = SCORES.get( query )
  
  # break: player not found
  if player == None:
    await ctx.respond( f"Unable to find player: \"{query}\"" )
    return
  
  name  = player.name
  score = player.score
  
  await ctx.respond( f"{name}'s score >> {score} points" )


def main():
  global SCORES
  SCORES = parse_raw_scores( retrieve_values() )
  bot.run()
  
if __name__ == "__main__":
  main()