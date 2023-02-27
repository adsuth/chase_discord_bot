import re
from time import time

import hikari
import lightbulb

from   classes import EMBED_COLORS as COLORS, Alias, AliasType
from   global_variables import CHASER_ALIASES, DEBUG_LOGGING_INCLUDED
from   classes import SubmissionType
import config as cfg

def func_timer( func ):
  """
  Decorator that returns the time taken for a function to complete
  """
  def wrapper():
    start_time = time()
    output     = func()
    end_time   = time()
    
    print( f"Total time to run {func.__name__} >> {end_time - start_time}" )
    return output
  return wrapper

def get_all_props( instance ):
  """
  Returns a list of all keys / props in given user-defined Class instance. \n
  This will ignore dunder methods (eg, Python's inbuilt methods)
  """
  return [ prop for prop in dir( instance ) if not prop.startswith( "__" ) ]

def get_props( instance ):
  """
  Returns a list of all keys / props in given user-defined Class instance. \n
  This will ignore any Class Methods!!
  This will ignore dunder methods (eg, Python's inbuilt methods)
  """
  return [ prop for prop in dir( instance ) if not prop.startswith( "__" ) and not callable( getattr( instance, prop ) ) ]

def strip_excess_bonus_point_data( item ):
  """Removes extra brackets from the item. eg "10 (1)" -> "10" (and also ! for the sub column)

  Args:
      item (str): candidate

  Returns:
      str: item without the ()
  """
  return re.sub("[^0-9]", "", item )
    
  
def score_to_int( item ):
  """Returns given item as an INTEGER. This should be used to prevent empty cells from raw csv data breaking sums. 

  Args:
      item (str): The candidate to be converted

  Returns:
      int: the converted int. 0 if item was an empty string 
  """
  if item == "":
    item = "0"     
  
  item = strip_excess_bonus_point_data( item ) # some cols appear as "10 (1)" for example
  
  return int( item )

def score_list_to_int( arr ):
  """Converts all indices of given list to ints

  Args:
      arr (list): list to be converted

  Returns:
      list: converted list
  """
  if type( arr ) != list:
    return -1
  
  mapped_arr = map(
    score_to_int,
    arr
  )
  
  return list( mapped_arr ) 

def string_on_new_line( inp ):
  return inp + "\n"

def show_strings_on_new_line( arr ):
  should_return = (
    type( arr ) != list or 
    len( arr )  <= 1
  )
  
  if should_return:
    return arr
  
  mapped_arr = map(
    string_on_new_line,
    arr[:-1]
  )
  
  return "".join( list( mapped_arr ) ) + arr[-1]

def bullet_list_strings( arr ):
  mapped_arr = map( lambda item: f"‣ {item}", arr )
  return "\n".join( list( mapped_arr ) )




def error_embed( msg ):
  return hikari.Embed(
    title = msg,
    color = COLORS.error,
  )

def debug_embed( msg ):
  return hikari.Embed(
    title = msg,
  )

def dlog( *args ):
  """ Debug Logging. Prints only if DEBUG_LOGGING_INCLUDED has been set to True"""
  if DEBUG_LOGGING_INCLUDED:
    print( "\033[93m", *args, f"\033[0m" )

def get_chaser_alias_key( query: str ) -> bool:
  alias = CHASER_ALIASES.get( query )
  
  if alias == None:
    return None
  
  if alias.type == AliasType.PLAYER:
    return CHASER_ALIASES.get( query ).key

  return alias.key

def find_player( query: str ):
  """ Finds player in the DATABASE dict. \n
  When found, initialises player's data (if not done prior) \n
  If player is unfound, will return None
  """
  chaser_alias_key = get_chaser_alias_key( query )
  
  if chaser_alias_key != None:
    query = chaser_alias_key
  
  player = cfg.DATABASE.get( query )
  
  # find chaser alias
  if player == None:
    alias  = CHASER_ALIASES.get( query )
    player = cfg.DATABASE.get( alias.key ) if alias != None else None

  # break: player not found
  if player == None:
    return None
  
  player.initialise_player_data()
  
  return player

def pad_string( string: str, length: int, pad_start: bool = False, padding_char: str = " " ):
  """
  ( "abc", 5, "x" ) \n
  Returns           \n
  "abcxx"
  """
  string_length = len( string )
  amount        = length - string_length

  # break: string isnt valid for padding, return input string by default
  if amount < 1:
    return string
  
  if pad_start:
    string = padding_char * amount + string
  else:
    string = string + padding_char * amount
  
  return string

def format_submissions_as_strings( subs ) -> str:
  """
  Strings generated *use padding*.\n
  They should be displayed with a `monospace font` 
  """
  output           = []
  max_sub_length   = get_longest_string_length( list( map( lambda sub: sub.name.replace( " (m)", "" ), subs ) ) )

  for sub in subs:
    string = pad_string( sub.name, max_sub_length )
    
    if sub.type == SubmissionType.MICRO:
      string += " Ⓜ️"
    
    output.append( string )

  return output

def player_not_found( player: object ) -> bool:
  """
  Semantic way of checking if player is None
  """
  return player == None

def get_longest_string_length( arr: list[ str ] ) -> int:
  """
  Returns the SIZE of the longest string in a given list
  """
  dlog( arr )
  return len( max( arr, key=len ) )

def pl( word: str, amount: int, plural_suffix: str = "s" ) -> str:
  """
  Pluralises a word if neeeded
  """
  return word if amount == 1 else word + plural_suffix

def pluralise( word: str, amount: int, plural_suffix: str = "s" ) -> str:
  """
  Pluralises a word if neeeded
  """
  return pl( word, amount, plural_suffix )

def cast_to_class( input, class_type = None ):
  """
  Cast given input to a different, passed type. \n
  Prevent issues with casting on a NoneType object.
  """
  if class_type == None:
    class_type = lambda input: input

  return class_type( input )

def check_for_chaser_alias( alias_key: str ):
  """
  Checks if the given key needs to be hanlded as a CHASER
  """
  if CHASER_ALIASES.get( alias_key ) == None:
    return False
  
  if CHASER_ALIASES.find( alias_key ).key in cfg.HANDLED_CHASERS:
    return False
  
  if CHASER_ALIASES.get(  alias_key ).key in cfg.HANDLED_CHASERS:
    return False
  
  return True

def handle_chaser_alias( alias_key: str ) -> None:  
  """
  "Merges" PLAYER and CHASER names into one and handles knock-ons
  """
  # we won't know what key is which yet
  keys = [ CHASER_ALIASES.find( alias_key ), CHASER_ALIASES.get( alias_key ) ]

  # determine what each key is
  player_alias = keys[0] if keys[0].type == AliasType.PLAYER else keys[1]
  chaser_alias = keys[1] if keys[1].type == AliasType.CHASER else keys[0]
  
  # get the data
  player_data = cfg.DATABASE.get( player_alias.key )
  chaser_data = cfg.DATABASE.get( chaser_alias.key )
  
  # prevent redoing this process
  cfg.HANDLED_CHASERS.append( player_alias.key )
  cfg.HANDLED_CHASERS.append( chaser_alias.key )
    
  # init player data if we haven't already
  player_data.initialise_player_data()
  chaser_data.initialise_player_data()

  # add PLAYER points to CHASER  
  chaser_data.total_points += player_data.total_points
  
  # add PLAYER subs to CHASER
  chaser_data.regular_submissions += player_data.regular_submissions
  chaser_data.micro_submissions   += player_data.micro_submissions
  
  # TODO: - We'll need to reassign the Submitters of each submission later
  
  # recalc stuff like the balance and subs
  chaser_data.update_calc_values()
  
  cfg.DATABASE.pop( player_alias.key )
  cfg.DATABASE.update( { chaser_alias.key: chaser_data } )
  
  
def get_can_afford_regular_string( player: object, cost: int ) -> str:
  """
  Checks to see if the `player`'s balance is within the brackets for regular subs. 
  """
  if player.balance >= cost:
    return f"✅ {player.name} can afford another regular submission! "

  return f"❌ {player.name} cannot afford another regular submission. "
  
  
def get_can_afford_micro_string( player: object ) -> str:
  """
  Checks to see if the `player`'s balance is within the brackets for micro subs. 
  """
  if player.balance < 100:
    return f"❌ {player.name} cannot afford a micro submission. "
  
  if player.balance < 200:
    return f"🆗 {player.name} can afford a micro submission with **1 track**. "

  if player.balance < 300:
    return f"🆗 {player.name} can afford a micro submission with **2 tracks**. "

  if player.balance < 400:
    return f"🆗 {player.name} can afford a micro submission with **3 tracks**. "
  
  return f"✅ {player.name} can afford a **full** micro submission! "


def generic_embed( ctx, title: str, color: COLORS ) -> hikari.Embed:
  embed = hikari.Embed( title = title, color = color )
  embed.set_footer( f"Requested by: { ctx.author.username }" )
  return embed
