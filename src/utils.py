from time import time

import hikari
import lightbulb

from   classes import EMBED_COLORS as COLORS
from   global_variables import DEBUG_LOGGING_INCLUDED
from   classes import SubmissionType
import config as cfg

def func_timer( func ):
  """
  Decorator that returns the time taken for a function to complete
  """
  def wrapper():
    start_time = time()
    output = func()
    end_time   = time()
    
    print( f"Total time to run {func.__name__} >> {end_time - start_time}" )
    return output
  return wrapper

def get_all_props( instance: object ) -> list[ str ]:
  """
  Returns a list of all keys / props in given user-defined Class instance. \n
  This will ignore dunder methods (eg, Python's inbuilt methods)
  """
  return [ prop for prop in dir( instance ) if not prop.startswith( "__" ) ]

def get_props( instance: object ) -> list[ str ]:
  """
  Returns a list of all keys / props in given user-defined Class instance. \n
  This will ignore any Class Methods!!
  This will ignore dunder methods (eg, Python's inbuilt methods)
  """
  return [ prop for prop in dir( instance ) if not prop.startswith( "__" ) and not callable( getattr( instance, prop ) ) ]

def strip_excess_bonus_point_data( item ):
  """Removes extra brackets from the item. eg "10 (1)" -> "10"

  Args:
      item (str): candidate

  Returns:
      str: item without the ()
  """
  startingIndex = item.find( "(" )
  
  if ( startingIndex == -1 ):
    return item
  
  startingIndex -= 1 # get to the space
  
  return item[ :startingIndex ]
    
  
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
  mapped_arr = map( lambda item: f"* {item}", arr )
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

def find_player( query: str ):
  """ Finds player in the DATABASE dict. \n
  When found, initialises player's data (if not done prior) \n
  If player is unfound, will return None
  """
  player = cfg.DATABASE.get( query )

  # break: player not found
  if player == None:
    return None
  
  player.initialise_player_data()
  
  print( player.name )
  if player.name == "VorpalStorm":
    dlog( *list( map( lambda prop: ( prop, player.__getattribute__( prop ) ), get_props( player ) ) ) )

  return player

def format_submissions_as_strings( subs ) -> str:
  output = []
  for sub in subs:
    output.append( sub.title.replace( "(m)", "(micro)" ) if sub.type == SubmissionType.MICRO else sub.title )

  return output