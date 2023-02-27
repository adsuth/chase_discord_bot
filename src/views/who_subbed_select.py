import miru
import hikari

import sys
from classes import Submission

from utils import dlog
sys.path.append( "../" )

from global_variables import MAX_NO_OF_SELECT_OPTIONS, NON_BREAK_SPACE
import config as cfg


def filter_sub_list( query: str, arr: list[ Submission ], limit: int = None ) -> list[str]:
  """ Filter a list of strings by the given query (case insensitive). \n
  You can also limit the number of results (this defaults to the length of the given list)
  """
  output = []
  query = query.lower().strip()
  
  if limit == None:
    limit = len( arr )
  
  for item in arr:
    formatted_item = item.name.lower().strip()
    
    if query in formatted_item:
      output.append( item )

    if len( output ) == limit:
      break

  return output


def convert_to_options( filtered_list: list[ Submission ] ) -> list[ miru.SelectOption ]:
  return [ miru.SelectOption( label = item.name, value = item.name.lower().strip() ) for item in filtered_list ]