import hikari
import lightbulb
import miru

from pprint           import pprint
from tabulate         import tabulate

# My methods
from player_data      import Player

from global_variables import ADMIN_ROLE_IDS, BOT_ALLOWED_CHANNELS, CHASER_ALIASES, TOKEN
from global_variables import SERVER_ID
from global_variables import NON_BREAK_SPACE
from global_variables import DEBUG_LOGGING_INCLUDED
from classes import EMBED_COLORS as COLORS, Alias, AliasType

import config as cfg
from views.components import CloseButton, WhoSubbedSelect

from views.who_subbed_select import convert_to_options, filter_sub_list

from retrieve_sheet   import retrieve_values
from player_data      import parse_raw_data

import utils
from   utils import bot_allow_action, debug_embed, error_embed, generic_embed, get_can_afford_micro_string, get_can_afford_regular_string, pad_string, pl
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

  if not bot_allow_action( ctx ):
    raise lightbulb.CommandErrorEvent
  
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

  if not bot_allow_action( ctx ):
    raise lightbulb.CommandErrorEvent
  
  query = ctx.options.player.strip().lower()
  player = find_player( query )
  
  # break: player not found
  if player_not_found( player ):
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  cost_of_sub = player.calc_cost_of_submision()
  
  point_word_string = pl( "Point", player.balance )
  embed = hikari.Embed( title = f"💰 Total Point Balance", color = COLORS.balance )
  
  embed.add_field( f"{ player.name } has ` {player.balance} {point_word_string} ` to spend. ", NON_BREAK_SPACE )
  embed.add_field( NON_BREAK_SPACE, NON_BREAK_SPACE )
  embed.add_field( f"Next Regular Submission will cost ` {cost_of_sub} Points `. ", get_can_afford_regular_string( player, cost_of_sub ) )
  embed.add_field( NON_BREAK_SPACE, NON_BREAK_SPACE )
  embed.add_field( f"Micro Submissions cost ` {100} Points ` *per track* (max of 4 tracks)", get_can_afford_micro_string( player ) )

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
  if not bot_allow_action( ctx ):
    raise lightbulb.CommandErrorEvent

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
  if not bot_allow_action( ctx ):
    raise lightbulb.CommandErrorEvent
  
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
  embed = hikari.Embed( title = f" { player.name }'s Submissions", color = COLORS.subs )
  embed.add_field(
    title_string,
    desc_string
  )
  embed.set_footer( f"Requested by: {ctx.author.username}" )

  # success: send message
  await ctx.respond( embed )



# # # # # # # # # # # # # # # # # # # # # # # #
#     Who Subbed   - /who_subbed
# # # # # # # # # # # # # # # # # # # # # # # #
@bot.command
@lightbulb.option( "game", "Name of the game to find" )
@lightbulb.command( "who_subbed", "Find out who subbed a certain game. " )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_who_subbed( ctx: lightbulb.SlashContext ):
  if not bot_allow_action( ctx ):
    raise lightbulb.CommandErrorEvent

  query = ctx.options.game.strip().lower()
  view  = miru.View( timeout = 60 )
  embed = generic_embed( ctx, f"🕹️  Who Submitted?", COLORS.who_subbed )
  
  filtered_games = filter_sub_list( query, cfg.GAME_LIST )
  too_many_matches = len( filtered_games ) > 25

  # break: no matches found
  if len( filtered_games ) == 0:
    await ctx.respond( error_embed( f"No games found with query \"{query}\"... " ) )
    return
   
  # break: direct match
  if len( filtered_games ) == 1:
    sub = filtered_games[ 0 ]

    embed.add_field( f"{ sub.name }", f"Submitted by: { sub.submitter }" )
    await ctx.respond( embed )
    
    return
  
  embed.add_field( "❓  Ambiguous Query...", f"Multiple possible results for \"{ query }\".\n{NON_BREAK_SPACE}" )

  # step: too many matches, warn that the game may not be present
  if too_many_matches:
    filtered_games = filtered_games[ :25 ] 
    embed.add_field( f"⚠️  Warning: Too many matches!", f"If the game isn't in the list, close this message and try again with a more precise query. " )

  
  # step: get user to specify game with dropdown
  embed.add_field( NON_BREAK_SPACE, "⬇️  Please clarify with the selection below. ⬇️" )
  options = convert_to_options( filtered_games )
  view.add_item( WhoSubbedSelect( options = options ) )
  view.add_item( CloseButton() )  
  
  message = await ctx.respond( embed, components=view )
  
  await view.start( message )
  await view.wait()
  
  # success: delete vestigial view
  await ctx.delete_last_response()
  
# # # # # # # # # # # # # # # # # # # # # # # #
#     ADMIN Refresh   - /refresh_data
# # # # # # # # # # # # # # # # # # # # # # # #
@bot.command
@lightbulb.add_checks( lightbulb.has_roles( ADMIN_ROLE_IDS ) ) # comment out this line for debugging
@lightbulb.command( "refresh_data", "ADMIN COMMAND: Refresh the player data for this session. " )
@lightbulb.implements( lightbulb.SlashCommand )
async def admin_refresh_data( ctx: lightbulb.SlashContext ):
  if not bot_allow_action( ctx ):
    raise lightbulb.CommandErrorEvent
  
  try:
    refresh_data()
    await ctx.respond( generic_embed( ctx, "✅  Success! Data has been refreshed. ", COLORS.success ) )

  except:
    await ctx.respond( error_embed( ctx, "❌  Failure. Data was not refreshed properly... ", COLORS.failure ) )
 


# # # # # # # # # # # # # # # # # # # # # # # #
#     Error Handling 
# # # # # # # # # # # # # # # # # # # # # # # #
@bot.listen( lightbulb.CommandErrorEvent )
async def on_error( event: lightbulb.CommandErrorEvent ) -> None:
  title = "An Error Occurred..."
  desc  = "Something went wrong... "

  # Keeping this here because I always forget how to do this:
  # bot_channel = await bot.rest.fetch_channel( BOT_ALLOWED_CHANNELS[0] )
  # bot_channel_uri = f"https://discord.com/channels/{ BOT_ALLOWED_CHANNELS[0] }"

  dlog( event.exception )

  # step: get the exception type
  match type( event.exception ):
    
    # break: For commands used outside the appropriate channel.
    case lightbulb.CommandInvocationError:
      title = "You Cannot Use Commands Here"
      desc  = f"Go to <#{ BOT_ALLOWED_CHANNELS[0] }> to use commands. "

    # break: For ADMIN commands performed by non-admins
    case lightbulb.MissingRequiredRole:
      title = "You Don't Have Permission to Use This Command"
      desc  = f"This command is exclusive to <@&{ADMIN_ROLE_IDS[0]}>"
    
    

  # step: create the embed
  embed = error_embed( "❌  " + title, desc )
  embed.set_footer( "Only you can see this. " )

  # success: Send ephemeral message to invoker
  await event.context.respond (
    hikari.ResponseType.MESSAGE_CREATE,  
    embed,
    flags=hikari.MessageFlag.EPHEMERAL, # ephemeral == only the respondee can see it
    role_mentions=True
  )


 

def refresh_data():
  cfg.GAME_LIST       = []
  cfg.HANDLED_CHASERS = []
  cfg.DATABASE  = parse_raw_data( retrieve_values() )

def main():
  refresh_data()
  miru.install( bot )
  bot.run()

  
def test():
  """ Debug method, dont use this in production.
  """
  from classes import duodict
  
  test_dict  = duodict( { Alias( "The Collector", AliasType.CHASER ): Alias( "Aakadarr", AliasType.PLAYER ) } )
  
  pprint( test_dict )
  pprint( test_dict.get( "Aakadarr" ) )
  pprint( test_dict.get( "the cOLLector" ) )

if __name__ == "__main__":
  main()
  # test()