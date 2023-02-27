from utils import check_for_chaser_alias, dlog, handle_chaser_alias, score_list_to_int
from utils import score_to_int
from utils import get_longest_string_length

from global_variables import CHASER_ALIASES, NO_OF_SCORE_DATA_COLUMNS
import config as cfg

from classes import Submission, SubmissionType

class Player:
  """
  Storage structure for player data.
  """
  def __init__( self, raw, name ):
    self.raw   = raw
    self.name  = name
    self.key   = name.lower().strip()
    self._defined_in_session = False
    
    self.regular_submissions = []
    self.micro_submissions = []
      
  def update_calc_values( self ):
    self.balance     = self.total_points
    self.submissions = sorted( ( self.regular_submissions + self.micro_submissions ), key=lambda x: x.name )
    
  def initialise_player_data( self ) -> None:
    """
    Initialises player data, assuming it has not done so prior.
    """
    if self._defined_in_session:
      return
    
    self._defined_in_session = True
    data = self.raw
    data += [""] * ( NO_OF_SCORE_DATA_COLUMNS - len( data ) )

    self.total_points       = score_to_int( data[ 12 ] ) # Total Points (excl. Bonus Points)
    self.AVP                = score_to_int( data[ 13 ] ) # Additional Voting Power
    self.sub_points         = score_to_int( data[ 14 ] ) # Subscriber Points
    self.boost_points       = score_to_int( data[ 15 ] ) # Server Boost Points
    self.comp_points        = score_to_int( data[ 16 ] ) # Competition Points
    self.crown_points       = score_to_int( data[ 17 ] ) # Gold Crown Points
    self.bonus_points       = score_to_int( data[ 18 ] ) # Generic Bonus Points

    self.total_bonus_points = sum( (
      self.AVP,
      self.sub_points,
      self.boost_points,
      self.comp_points,
      self.crown_points,
      self.bonus_points,
    ) )

    self.will_earn_avp_with_sub = False
    self.update_calc_values()

    if check_for_chaser_alias( self.key ):
      handle_chaser_alias( self.key )
  
  def get_bonus_dict( self ) -> dict[ str: str ]:
    return {
      "Additional Voting Power": self.AVP,
      "Subscriber Points":       self.sub_points,
      "Server Boost Points":     self.boost_points,
      "Competition Points":      self.comp_points,
      "Gold Crown Points":     self.crown_points,
      "Bonus Points":            self.bonus_points,
    }
  
  def get_bonus_dict_items( self ):
    return self.get_bonus_dict().items()
  
  def calc_cost_of_submision( self ):
    no_of_subs = len( self.regular_submissions )
    
    if no_of_subs == 0:
      return 100
        
    if no_of_subs < 4:
      return no_of_subs * 100
    
    if no_of_subs == 4:
      self.will_earn_avp_with_sub = True
    
    return 500   
     

def parse_raw_data( raw_data: str ) -> dict[Player]:
  """
  Parses raw player data, returning a dict of Player objects
  """
  output       = {}
  subbed_games = []
  
  for row in raw_data:
    key, name = row[0].lower(), row[0]
  
    output[ key ] = Player( row, name )
    
    # add subbed games if there are any
    if len( row ) > 19:
      subs = parse_submissions( row[20:], name )
      output[ key ].regular_submissions = subs[0]
      output[ key ].micro_submissions   = subs[1]
      
      subbed_games += subs[0] + subs[1]

  cfg.GAME_LIST = sorted( subbed_games, key=lambda item: item.key )
  
  
  return output


def parse_submissions( raw_subs: list[str], player: str ) -> tuple[Submission, Submission]:
  """
  Returns two lists, regular and micro submissions.
  """
  regular_subs    = []
  micro_subs      = []

  for item in raw_subs:

    # Check for player alias
    if ( alias := CHASER_ALIASES.get( player ) ) != None:
      player = f"{alias.name} ({player})"

    sub = Submission( item, player )
    
    if sub.type == SubmissionType.MICRO:
      micro_subs.append( sub )
    else:
      regular_subs.append( sub )

  return regular_subs, micro_subs