from time import time

import hikari
import lightbulb

from global_variables import COLORS

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