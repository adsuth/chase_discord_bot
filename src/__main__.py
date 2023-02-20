import hikari
import lightbulb
import miru

from pprint           import pprint
from tabulate         import tabulate

# My methods
from player_score     import PlayerScore
from global_variables import TOKEN
from global_variables import SERVER_ID
from global_variables import SCORES
from global_variables import COLORS

from retrieve_sheet   import retrieve_values
from player_score     import parse_raw_scores

import utils
from utils import error_embed

bot = lightbulb.BotApp (
  token=TOKEN,
  intents=hikari.Intents.ALL,
  default_enabled_guilds=( SERVER_ID ) 
)

# START

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
  @miru.text_select( placeholder="Select a Game", options=get_select_options( "debug_list" ) )
  async def select_option( self, select, ctx ):
    await ctx.edit_response( f"Selected > {select.values[0]}" )

  @miru.button( emoji="\N{CROSS MARK}", style=hikari.ButtonStyle.DANGER )
  async def stop_button(self, button: miru.Button, ctx: miru.ViewContext) -> None:
    self.stop() # Stop listening for interactions

@bot.command
@lightbulb.option( "player", "Player's Twitch username" )
@lightbulb.command( "score", "Retrieves a player's score from the scoreboard" )
@lightbulb.implements( lightbulb.SlashCommand )
async def get_player_score( ctx ):
  query = ctx.options.player.strip().lower()
  player = SCORES.get( query )
  
  # break: player not found
  if player == None:
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  player.initialise_player_data()
  
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
  player = SCORES.get( query )
  
  # break: player not found
  if player == None:
    await ctx.respond( error_embed( f"Unable to find player: \"{query}\"" ) )
    return
  
  player.initialise_player_data()
  
  data = utils.bullet_list_strings( player.get_submissions() )
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
  view = SubmissionGameSelect( timeout = 5 )  # Create a new view
  message = await ctx.respond( "Find Submitter of Game", components=view )
  
  await view.start(message)  # Start listening for interactions
  await view.wait() # Optionally, wait until the view times out or gets stopped
  await ctx.delete_last_response()


def main():
  global SCORES
  SCORES = parse_raw_scores( retrieve_values() )
  miru.install( bot ) # Load miru and attach it to the bot instance.
  bot.run()
  
def test():
  print( utils.show_strings_on_new_line( "test1" ) )
  print( utils.show_strings_on_new_line( [ "a", "b", "c" ] ) )
  print( utils.show_strings_on_new_line( [  ] ) )

if __name__ == "__main__":
  main()