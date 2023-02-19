import hikari
import lightbulb

from pprint           import pprint
from tabulate         import tabulate

# My methods
from player_score     import PlayerScore
from global_variables import TOKEN
from global_variables import SERVER_ID
from global_variables import SCORES
from global_variables import COLORS

from retrieve_sheet   import retrieve_values
from player_score     import parse_raw_scores

import utils
from utils import error_embed

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
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  player.initialise_player_data()
  
  table_data = player.get_scores_dict_items()
  table      = tabulate( table_data, tablefmt="plain" ) 
  message    = f"```{table}```"
  
  embed      = hikari.Embed( title = f"Scores for { player.name }", color = COLORS.score )
  embed.add_field(f"🥇", f"{ message }")
  
  #send message
  await ctx.respond( embed )

@bot.command
@lightbulb.option( "player", "Player's Twitch username" )
@lightbulb.command( "subs", "Retrieves a list of the player's game submissions" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_submissions( ctx ):
  query = ctx.options.player.strip().lower()
  player = SCORES.get( query )
  
  # break: player not found
  if player == None:
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  player.initialise_player_data()
  
  data = utils.bullet_list_strings( player.get_submissions() )
  # maybe limit the number of list items?
  
  if len( data ) < 1:
    await ctx.respond( error_embed( f"{ player.name } hasn't submitted any games..." ) )
    return
  
  embed = hikari.Embed( title = f"{ player.name }'s submissions", color = COLORS.subs )
  embed.add_field(f"🎮", f"{ data }")
  
  #send message
  await ctx.respond( embed )


def main():
  global SCORES
  SCORES = parse_raw_scores( retrieve_values() )
  bot.run()
  
def test():
  print( utils.show_strings_on_new_line( "test1" ) )
  print( utils.show_strings_on_new_line( [ "a", "b", "c" ] ) )
  print( utils.show_strings_on_new_line( [  ] ) )

if __name__ == "__main__":
  main()