from pprint import pprint

import hikari
import lightbulb
from classes import EMBED_COLORS as COLORS

import config as cfg
from global_variables import (ADMIN_ROLE_IDS, BOT_ALLOWED_CHANNELS, CHANNELS, ERROR_HANDLING_ENABLED, IN_DEBUG_MODE, NON_BREAK_SPACE )
# My methods
from utils import ( dlog, error_embed, find_player_by_id, generic_embed, parse_request_message )



# # # # # # # # # # # # # # # # # # # # # # # #
#     Error Handling 
# # # # # # # # # # # # # # # # # # # # # # # #

if ERROR_HANDLING_ENABLED:
  @cfg.bot.listen( lightbulb.CommandErrorEvent )
  async def on_error( event: lightbulb.CommandErrorEvent ) -> None:

    title = "An Error Occurred..."
    desc  = "Something went wrong... "

    # Keeping this here because I always forget how to do this:
    # bot_channel = await bot.rest.fetch_channel( BOT_ALLOWED_CHANNELS[0] )
    # bot_channel_uri = f"https://discord.com/channels/{ BOT_ALLOWED_CHANNELS[0] }"

    dlog( event.exception )
    dlog( event.exc_info )

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

# # # # # # # # # # # # # # # # # # # # # # # #
#     Error Handling 
# # # # # # # # # # # # # # # # # # # # # # # #

@cfg.bot.listen( hikari.events.ReactionEvent )
async def on_reaction( event: hikari.events.ReactionEvent ) -> None:

  # break: reaction not in the correct channel
  # todo  - change this channel to appropriate chase channel
  if event.channel_id != CHANNELS[ "test_register" ]:
    return
  
  original_message = await cfg.bot.rest.fetch_message( event.channel_id, event.message_id )
  value = original_message.embeds[0].fields[0].value

  user_data   = parse_request_message( value )

  # break: if player is in database already
  if find_player_by_id( user_data[ "id" ] ) != None:
    dlog( "User with ID %d has already been added to the database" % ( user_data[ "id" ] ) )
    return

  # step: add player's id to the database
  cfg.DATABASE.get( user_data["key"] ).discord_id = user_data[ "id" ]

  # success: DM player to notify them of the request being successful
  user_snowflake = await cfg.bot.rest.fetch_user( user_data[ "id" ] )

  embed = generic_embed( None, "✅  Registration Confirmed!", COLORS.success )
  embed.add_field( "Your Discord ID has been linked to the Scoreboard", "Now when you enter a command, you won't need to pass your name. Simply leave the option blank and we'll get your data automatically! " )

  await user_snowflake.send(
    embed = embed
  )

  # delete the original message todo  - is this wanted?
  await original_message.delete()

