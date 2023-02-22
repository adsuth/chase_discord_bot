import hikari
import lightbulb
import miru

from pprint           import pprint
from tabulate         import tabulate

# My methods
from player_data      import Player

from global_variables import TOKEN
from global_variables import SERVER_ID
from global_variables import NON_BREAK_SPACE
from global_variables import DEBUG_LOGGING_INCLUDED
from classes import EMBED_COLORS as COLORS


import config as cfg

from views.sel_submission_game import SubmissionGameSelect

from retrieve_sheet   import retrieve_values
from player_data      import parse_raw_data

import utils
from   utils import error_embed
from   utils import find_player
from   utils import format_submissions_as_strings
from   utils import dlog

bot = lightbulb.BotApp (
  token=TOKEN,
  intents=hikari.Intents.ALL,
  default_enabled_guilds=( SERVER_ID ) 
)

# # # # # # # # # # # # # # # # # # # # # # # #
#     SpiritBomb  -  /spiritbomb
# # # # # # # # # # # # # # # # # # # # # # # #
@bot.command
@lightbulb.option( "player", "Player's Twitch username" )
@lightbulb.command( "spiritbomb", "Reveals a player's :spiritbomb: power (total bonus points)" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_spiritbomb( ctx ):
  """ 
  Gets given player's Spiritbomb power. \n
  A "Spiritbomb" uses *all of the player's bonus points*
  """
  query = ctx.options.player.strip().lower()
  player = find_player( query )
  
  # break: player not found
  if player == None:
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  embed = hikari.Embed( title = f"Spiritbomb Power", color = COLORS.spiritbomb )
  embed.add_field( f"{ player.name }'s :spiritbomb: is worth `\cyan {player.total_bonus_points} Points `", NON_BREAK_SPACE )

  await ctx.respond( embed )



@bot.command
@lightbulb.option( "player", "Player's Twitch username" )
@lightbulb.command( "score", "Retrieves a player's score from the scoreboard" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_score( ctx ):
  query = ctx.options.player.strip().lower()
  player = find_player( query )
  
  # break: player not found
  if player == None:
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
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
  player = cfg.DATABASE.get( query )
  
  # break: player not found
  if player == None:
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  player.initialise_player_data()
  
  data = utils.bullet_list_strings( format_submissions_as_strings( player.get_submissions() ) )
  # maybe limit the number of list items?
  
  if len( data ) < 1:
    await ctx.respond( error_embed( f"{ player.name } hasn't submitted any games..." ) )
    return
  
  embed = hikari.Embed( title = f"{ player.name }'s submissions", color = COLORS.subs )
  embed.add_field(f"🎮", f"{ data }")
  
  #send message
  await ctx.respond( embed )


@bot.command
@lightbulb.command( "test user command", "DEBUG COMMAND > This is just to test certain functionality" )
@lightbulb.implements( lightbulb.UserCommand )
async def debug_cmd( ctx ):
  """ DEBUG METHOD
  """
  await ctx.respond( f"Your user ID is >> { ctx.options.target.id }" )

@bot.command
@lightbulb.command( "debug", "DEBUG COMMAND > This is just to test certain functionality" )
@lightbulb.implements( lightbulb.SlashCommand )
async def debug_cmd( ctx ):
  """ DEBUG METHOD
  """
  view = SubmissionGameSelect( timeout = 15 )  # Create a new view
  embed = hikari.Embed( title = f"Select a game from the list below", color = COLORS.subs )
  
  message = await ctx.respond( embed, components=view )
  
  await view.start( message )  # Start listening for interactions
  await view.wait() # Optionally, wait until the view times out or gets stopped
  await ctx.delete_last_response()


def main():
  cfg.DATABASE = parse_raw_data( retrieve_values() )
  miru.install( bot ) # Load miru and attach it to the bot instance.
  bot.run()
  
def test():
  """ Debug method, dont use this in production.
  """
  print( utils.show_strings_on_new_line( "test1" ) )
  print( utils.show_strings_on_new_line( [ "a", "b", "c" ] ) )

if __name__ == "__main__":
  main()
  # test()