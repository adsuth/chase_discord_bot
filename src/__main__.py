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
from   utils import error_embed, pad_string, pl
from   utils import find_player
from   utils import player_not_found
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
  
  point_word_string = pl( "Point", player.total_bonus_points )
  embed = hikari.Embed( title = f"Spiritbomb Power", color = COLORS.spiritbomb )
  embed.add_field( f"{ player.name }'s :spiritbomb: is worth ` {player.total_bonus_points} {point_word_string} `", NON_BREAK_SPACE )
  embed.set_footer( f"Requested by: {ctx.author.username}" )

  await ctx.respond( embed )


# # # # # # # # # # # # # # # # # # # # # # # #
#     Balance - /balance
# # # # # # # # # # # # # # # # # # # # # # # #
@bot.command
@lightbulb.option( "player", "Player's Twitch username" )
@lightbulb.command( "balance", "Reveals a player's total spendable points" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_spiritbomb( ctx ):
  """ 
  Gets given player's total spendable points. \n
  This includes Total Points, and the sum of all bonus point categories.
  """
  query = ctx.options.player.strip().lower()
  player = find_player( query )
  
  # break: player not found
  if player_not_found( player ):
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  point_word_string = pl( "Point", player.balance )
  embed = hikari.Embed( title = f"💰 Total Point Balance", color = COLORS.balance )
  embed.add_field( f"{ player.name } has ` {player.balance} {point_word_string} ` to spend. ", NON_BREAK_SPACE )
  embed.set_footer( f"Requested by: {ctx.author.username}" )

  # success: send message
  await ctx.respond( embed )

# # # # # # # # # # # # # # # # # # # # # # # #
#     Bonus Points    - /bonus
# # # # # # # # # # # # # # # # # # # # # # # #
@bot.command
@lightbulb.option( "player", "Player's Twitch username" )
@lightbulb.command( "bonus", "Retrieves player's bonus point categories from the scoreboard as a table" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_score( ctx ):
  query = ctx.options.player.strip().lower()
  player = find_player( query )
  
  # break: player not found
  if player_not_found( player ):
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  table_data   = player.get_bonus_dict_items()
  table        = tabulate( table_data, tablefmt="plain" ) 
  title_string = ":spiritbomb: Spiritbomb is worth ` %d %s `" % ( player.total_bonus_points, pl( "Point", player.total_bonus_points ) )
  
  embed        = hikari.Embed( title = f"🎁  Bonus Points of { player.name }", color = COLORS.bonus )
  
  embed.add_field( title_string, f"```{table}```" )
  embed.set_footer( f"Requested by: {ctx.author.username}" )
  
  # success: send message
  await ctx.respond( embed )


# # # # # # # # # # # # # # # # # # # # # # # #
#     Submissions   - /subs 
# # # # # # # # # # # # # # # # # # # # # # # #
@bot.command
@lightbulb.option( "player", "Player's Twitch username" )
@lightbulb.command( "subs", "Retrieves a list of the player's game submissions" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_submissions( ctx ):
  """ Retrieves a list of player submissions.
  """
  query = ctx.options.player.strip().lower()
  player = find_player( query )
  
  # break: player not found
  if player_not_found( player ):
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  # break: player has no submissions
  if len( player.submissions ) < 1:
    await ctx.respond( error_embed( f"{ player.name } hasn't submitted any games..." ) )
    return

  data = utils.bullet_list_strings( format_submissions_as_strings( player.submissions ) )
  
  padding_amount     = len( max( ( str( len( player.regular_submissions ) ), str( len( player.micro_submissions ) ) ) ) )
 
  no_of_regular_subs = pad_string( str( len( player.regular_submissions ) ), padding_amount, True )
  no_of_micro_subs   = pad_string( str( len( player.micro_submissions   ) ), padding_amount, True )
  no_of_submissions  = len( player.submissions )
  
  regular_word_formatted = "` %s Normal %s `"  % ( no_of_regular_subs, pl( "Submission", len( player.regular_submissions ) ) )
  micro_word_formatted   = "` %s Micro  %s `"  % ( no_of_micro_subs,   pl( "Submission", len( player.micro_submissions   ) ) )
  
  # step: create strings
  desc_string  = f"{ regular_word_formatted } \n{ micro_word_formatted }\n```{data}```"
  title_string = "%s has submitted %d %s" % ( player.name, no_of_submissions, pl( "Game", no_of_submissions ) )
  
  # step: create embed
  embed = hikari.Embed( title = f":joystick: { player.name }'s Submissions", color = COLORS.subs )
  embed.add_field(
    title_string,
    desc_string
  )
  embed.set_footer( f"Requested by: {ctx.author.username}" )

  # success: send message
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