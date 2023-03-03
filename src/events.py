import hikari
import lightbulb
from classes import EMBED_COLORS as COLORS

import config as cfg
from global_variables import (ADMIN_ROLES, CHANNELS, ERROR_HANDLING_ENABLED, IN_DEBUG_MODE, NON_BREAK_SPACE )
from utils import ( dlog, error_embed, find_player_by_id, generic_embed, parse_request_message )



# # # # # # # # # # # # # # # # # # # # # # # #
#     Error Handling 
# # # # # # # # # # # # # # # # # # # # # # # #
if ERROR_HANDLING_ENABLED:
  @cfg.bot.listen( lightbulb.CommandErrorEvent )
  async def on_error( event: lightbulb.CommandErrorEvent ) -> None:

    title = "An Error Occurred..."
    desc  = "Something went wrong... "

    # step: get the exception type
    match type( event.exception ):
        
      # break: For commands used outside the appropriate channel.
      case lightbulb.CommandInvocationError:
        bot_channel = CHANNELS.get( "bot_channel" )
        title = "You Cannot Use Commands Here"
        desc  = f"Go to <#{bot_channel}> to use commands. "

      # break: For ADMIN commands performed by non-admins
      case lightbulb.MissingRequiredRole:
        admin_roles = [ f"<@&{role}>" for role in ADMIN_ROLES ]
        title = "You Don't Have Permission to Use This Command"
        desc  = f"This command is exclusive to {admin_roles}>"


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
  """
  Upon using the /register command, a message is sent to the hidden "register" channel (that only Quetz should have access to) \n
  """

  # break: reaction not in the correct channel
  if event.channel_id != CHANNELS[ "register_channel" ]:
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

  await original_message.delete()

