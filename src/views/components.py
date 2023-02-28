import hikari
import miru

import sys

from utils import dlog, error_embed, generic_embed, get_from_list
sys.path.append( "../" )

from global_variables import NON_BREAK_SPACE
from classes          import EMBED_COLORS as COLORS
import config as cfg

# # # # # # # # # # # # # # # # # # # # # # # #
#     Buttons
# # # # # # # # # # # # # # # # # # # # # # # #
class CloseButton( miru.Button ):
  def __init__( self ) -> None:
    super().__init__( style = hikari.ButtonStyle.DANGER, label = "Close" )



# # # # # # # # # # # # # # # # # # # # # # # #
#     Selections
# # # # # # # # # # # # # # # # # # # # # # # #
class WhoSubbedSelect( miru.TextSelect ):
  def __init__( self, options: list[ str ] ) -> None:
    super().__init__( placeholder = "Select a Game", options = options )
  
  async def callback( self, ctx: miru.ViewContext ) -> None:
    index = get_from_list( self.values[0], [ item.key for item in cfg.GAME_LIST ] )
    sub   = cfg.GAME_LIST[ index ]  
    
    embed = generic_embed( ctx, "🕹️  Who Submitted?", COLORS.who_subbed )
    embed.add_field( f"{ sub.name }", f"Submitted by: { sub.submitter }" )
    
    # await cfg.bot.rest.create_message( embed = embed, channel = ctx.channel_id )
    await ctx.edit_response( embed = embed )
    
    self.view.stop()
    self.view.clear_items()