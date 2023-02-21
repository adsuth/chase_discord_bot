import miru
import hikari

import os, sys

SELECT_OPTIONS = {
  "debug_list": [ miru.SelectOption( label=i, value=i ) for i in range( 25 ) ],
  "submission_game_select": [
    miru.SelectOption(
      label = f"lbl_test_1",
      value = "test_1",
    ),
    miru.SelectOption(
      label = f"lbl_test_2",
      value = "test_2",
    ),
    miru.SelectOption(
      label = f"lbl_test_3",
      value = "test_3",
    ),
  ]
}

def get_select_options( key ):
  return SELECT_OPTIONS[ key ]

class SubmissionGameSelect( miru.View ):
  @miru.text_select( placeholder = "Select a Game", options = get_select_options( "debug_list" ) )
  async def select_option( self, select, ctx ):
    embed = hikari.Embed( title = f"Selected Game: " )
    embed.add_field( "\N{JOYSTICK}", f"{ select.values[0] }" )
    await ctx.edit_response( embed )

  @miru.button( emoji="\N{CROSS MARK}", style=hikari.ButtonStyle.SECONDARY )
  async def stop_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
    self.stop() # Stop listening for interactions
