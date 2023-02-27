import hikari
import miru

import sys

from utils import generic_embed
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

  async def callback( self, ctx: miru.ViewContext ) -> None:
    self.view.stop()



# # # # # # # # # # # # # # # # # # # # # # # #
#     Selections
# # # # # # # # # # # # # # # # # # # # # # # #
class WhoSubbedSelect( miru.TextSelect ):
  def __init__( self, options: list[ str ] ) -> None:
    super().__init__( options = options )
  
  @miru.text_select
  async def callback( self, select, ctx ) -> None:
    sub = cfg.GAME_LIST.get( select.values[0] )
    
    embed = generic_embed( ctx, "🕹️  Who Submitted?", COLORS.who_subbed )
    embed.add_field( f"{ sub.name }", f"Submitted by: { sub.submitter }" )
    
    await ctx.message.edit( embed = embed )