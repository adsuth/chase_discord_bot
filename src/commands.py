import hikari
import lightbulb
import miru
from tabulate import tabulate

import config as cfg
import utils
from classes import EMBED_COLORS as COLORS
from classes import Alias, AliasType, SubmissionType
from global_variables import (CHANNELS, CHASER_ALIASES, DEBUG_LOGGING_INCLUDED,
                              NON_BREAK_SPACE, SERVER_ID, TOKEN)
# My methods
from player_data import Player
from utils import (bot_allow_action, convert_to_options, debug_embed, dlog,
                   error_embed, filter_sub_list, find_player,
                   format_submissions_as_strings, generic_embed,
                   get_can_afford_micro_string, get_can_afford_regular_string,
                   pad_string, pl, player_not_found)
from views.components import CloseButton, WhoSubbedSelect


# # # # # # # # # # # # # # # # # # # # # # # #
#     SpiritBomb  -  /spiritbomb
# # # # # # # # # # # # # # # # # # # # # # # #
@cfg.bot.command
@lightbulb.option( "player", "Player's Twitch username", default = "" )
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
  player = find_player( ctx, query )

  # break: player id not found
  if len( query ) == 0 and player_not_found( player ):
    embed = error_embed( f"Unable to find your ID" )
    embed.add_field( "You aren't registered yet...", "Use `/register` to request to have your ID tied to your Scoreboard entry.\nIf you have registered, please wait for Quetz to add you to the database." )
    return
    
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
@cfg.bot.command
@lightbulb.option( "player", "Player's Twitch username", default = "" )
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
  player = find_player( ctx, query )

  # break: player id not found
  if len( query ) == 0 and player_not_found( player ):
    embed = error_embed( f"Unable to find your ID" )
    embed.add_field( "You aren't registered yet...", "Use `/register` to request to have your ID tied to your Scoreboard entry.\nIf you have registered, please wait for Quetz to add you to the database." )
    return
  
  # break: player not found
  if player_not_found( player ):
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  cost_of_sub = player.calc_cost_of_submision()
  
  point_word_string = pl( "Point", player.balance )
  embed = hikari.Embed( title = f"💰 Total Point Balance", color = COLORS.balance )
  
  embed.add_field( f"{ player.name } has ` {player.balance} {point_word_string} ` to spend. ", f"They may spend up to `  {player.AVP} Points  ` per week" )
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
@cfg.bot.command
@lightbulb.option( "player", "Player's Twitch username", default = "" )
@lightbulb.command( "bonus", "Retrieves player's bonus point categories from the scoreboard as a table" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_score( ctx ):
  """ Retrieves a player's bonus points as a table
  """
  if not bot_allow_action( ctx ):
    raise lightbulb.CommandErrorEvent

  query = ctx.options.player.strip().lower()
  player = find_player( ctx, query )
  
  # break: player id not found
  if len( query ) == 0 and player_not_found( player ):
    embed = error_embed( f"Unable to find your ID" )
    embed.add_field( "You aren't registered yet...", "Use `/register` to request to have your ID tied to your Scoreboard entry.\nIf you have registered, please wait for Quetz to add you to the database." )
    return
  
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
@cfg.bot.command
@lightbulb.option( "player", "Player's Twitch username", default = "" )
@lightbulb.command( "subs", "Retrieves a list of the player's game submissions" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_submissions( ctx ):
  """ Retrieves a list of player submissions.
  """
  if not bot_allow_action( ctx ):
    raise lightbulb.CommandErrorEvent
  
  query = ctx.options.player.strip().lower()
  player = find_player( ctx, query )

  # break: player id not found
  if len( query ) == 0 and player_not_found( player ):
    embed = error_embed( f"Unable to find your ID" )
    embed.add_field( "You aren't registered yet...", "Use `/register` to request to have your ID tied to your Scoreboard entry.\nIf you have registered, please wait for Quetz to add you to the database." )
    return
  
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
  embed = hikari.Embed( title = f"🕹️  { player.name }'s Submissions", color = COLORS.subs )
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
@cfg.bot.command
@lightbulb.option( "game", "Name of the game to find" )
@lightbulb.command( "who_subbed", "Find out who subbed a certain game. " )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_who_subbed( ctx: lightbulb.SlashContext ):
  if not bot_allow_action( ctx ):
    raise lightbulb.CommandErrorEvent

  query = ctx.options.game.strip().lower()
  view  = miru.View( timeout = 30 )
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

    if sub.type == SubmissionType.LEGACY:
      embed.add_field( f"{ sub.name }", f"This was a legacy submission" )
    else:
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
  
  view.add_item( WhoSubbedSelect( options = convert_to_options( filtered_games ) ) )
  # view.add_item( CloseButton() )  
  
  message = await ctx.respond( embed, components = view, flags = hikari.MessageFlag.EPHEMERAL )
  
  await view.start( message )
  await view.wait()
  
  # success: 
  


# # # # # # # # # # # # # # # # # # # # # # # #
#     Register   - /register
# # # # # # # # # # # # # # # # # # # # # # # #
# @cfg.bot.command
# @lightbulb.option( "username", "The name you want to register as" )
# @lightbulb.command( "register", "Request to have Quetz assign your Discord Account to the Scoreboard" )
# @lightbulb.implements( lightbulb.SlashCommand )
# async def register_discord_to_scoreboard( ctx: lightbulb.SlashContext ):
#   if not bot_allow_action( ctx ):
#     raise lightbulb.CommandErrorEvent
  
#   query          = ctx.options.username.strip().lower()
#   player: Player = find_player( ctx, query )

#   # break: player id not found
#   if len( query ) == 0 and player_not_found( player ):
#     embed = error_embed( f"Unable to find your ID" )
#     embed.add_field( "You aren't registered yet...", "Use `/register` to request to have your ID tied to your Scoreboard entry.\nIf you have registered, please wait for Quetz to add you to the database." )
#     return
  
#   # break: player not found
#   if player_not_found( player ):
#     await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ), flags = hikari.MessageFlag.EPHEMERAL )
#     return

#   player.initialise_player_data()
#   player_already_registered = player.is_registered()

#   # break: name already registered
#   if player_already_registered:
#     registrar = await cfg.bot.rest.fetch_user( player.discord_id )
#     await ctx.respond( error_embed( f"{player.name} has already been registered to { registrar.name }... " ) )
#     return
  
#   registrar_details = [
#     [ "Name",   ctx.author.username ],
#     [ "ID",     ctx.author.id ],
#     [ "Player", player.name ]
#   ]

#   # step: create embed to send to the register channel
#   embed = generic_embed( ctx, f"📋  Register Request", COLORS.register )
#   embed.add_field(
#     "Registrar Details",
#     "%s\n```%s```" % ( "<@" + str( ctx.author.id ) + ">", tabulate( registrar_details, tablefmt = "plain" ) )
#   )

#   # embed.add_field( f"{ ctx.author.username } Wants to Register", f"<@{ ctx.author.id }> is looking to register as **{ player.name }**" )
#   # embed.add_field( "Their ID is ", f"`{ ctx.author.id }`" )

#   # step: send message to the register channel
#   await cfg.bot.rest.create_message (
#     embed = embed,
#     channel = CHANNELS.get( "register_channel" ) 
#   )

#   embed = generic_embed( ctx, "📋  Request Sent", COLORS.success )
#   embed.add_field( NON_BREAK_SPACE, f"You have successfully requested to register as **{player.name}**" )

#   await ctx.respond( embed = embed, flags = hikari.MessageFlag.EPHEMERAL )

#   # todo  - send poster an ephemeral message of request confirmation
#   # todo  - add new event for the register channel that will send confirmation DMs to users when quetz reacts to message