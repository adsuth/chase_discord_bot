from pprint import pprint

import hikari
import lightbulb

import config as cfg
from global_variables import (ADMIN_ROLE_IDS, BOT_ALLOWED_CHANNELS, ERROR_HANDLING_ENABLED, IN_DEBUG_MODE )
# My methods
from utils import ( dlog, error_embed )



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

