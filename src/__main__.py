import hikari
import lightbulb
import miru

from classes import EMBED_COLORS as COLORS
import config as cfg
from global_variables import ADMIN_ROLES, SERVER_ID, TOKEN
from player_data import parse_raw_data
from retrieve_sheet import get_legacy_games, retrieve_values
from utils import bot_allow_action, error_embed, generic_embed

cfg.bot = lightbulb.BotApp (
  token                   = TOKEN,
  intents                 = hikari.Intents.ALL,
  default_enabled_guilds  = ( SERVER_ID ) 
)

# import our commands and events
import commands
import events

# # # # # # # # # # # # # # # # # # # # # # # #
#     ADMIN Refresh   - /refresh_data
# # # # # # # # # # # # # # # # # # # # # # # #
@cfg.bot.command
@lightbulb.add_checks( lightbulb.has_roles( ADMIN_ROLES[0] ) )
@lightbulb.command( "refresh_data", "ADMIN COMMAND: Refresh the player data for this session. " )
@lightbulb.implements( lightbulb.SlashCommand )
async def admin_refresh_data( ctx: lightbulb.SlashContext ):
  if not bot_allow_action( ctx ):
    raise lightbulb.MissingRequiredRole
  
  try:
    refresh_data()
    await ctx.respond( generic_embed( ctx, "✅  Success! Data has been refreshed. ", COLORS.success ) )

  except:
    await ctx.respond( error_embed( ctx, "❌  Failure. Data was not refreshed properly... ", COLORS.failure ) )
 

def refresh_data():
  cfg.GAME_LIST       = get_legacy_games()
  cfg.HANDLED_CHASERS = []
  cfg.DATABASE        = parse_raw_data( retrieve_values() )

def main():
  refresh_data()
  miru.install( cfg.bot )
  cfg.bot.run()


""" Entry Point
"""
if __name__ == "__main__":
  main()