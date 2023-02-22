from utils import dlog, score_list_to_int
from utils import score_to_int
from utils import get_longest_string_length

from global_variables import NO_OF_SCORE_DATA_COLUMNS

from classes import SubmissionType

class Player:
  """
  Storage structure for player data.
  """
  def __init__( self, raw, name ):
    # todo : this is not reflective of final structure
    self.raw   = raw
    self.name  = name
    self._defined_in_session = False

  class Submission:
    """
    Mini-class, just to store the type of submission. 
    """
    def __init__( self, name : str, type : SubmissionType ):
      self.name = name
      self.type = type
  
  def initialise_player_data( self ) -> None:
    """
    Initialises player data, assuming it has not done so prior.
    """
    if self._defined_in_session:
      return
    
    self._defined_in_session = True
    data = self.raw
    data += [""] * ( NO_OF_SCORE_DATA_COLUMNS - len( data ) )

    dlog( data )
    
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
    self.balance         = self.total_points + self.total_bonus_points

    self.regular_submissions, self.micro_submissions = parse_submissions( data[ 20: ] ) # List of submissions 
  
  def __dict__( self ) -> dict[ str, any ]:
    return {
      "Name": self.name,
      "Total Points": self.total_points,
    }
  
  def get_submissions( self ) -> list[ Submission ]:
    return self.regular_submissions + self.micro_submissions
  
  def get_scores_dict_items( self ):
    return self.get_scores_dict().items()


def parse_raw_data( raw_data: str ) -> dict[Player]:
  """
  Parses raw player data, returning a dict of Player objects
  """
  output = {}
  for row in raw_data:
    key, name = row[0].lower(), row[0]
    output[ key ] = Player( row, name )
  return output


def parse_submissions( raw_subs: list[str] ) -> tuple[Player.Submission, Player.Submission]:
  """
  Returns two lists, regular and micro submissions.
  """
  regular_subs    = []
  micro_subs      = []

  for sub in raw_subs:
    if "(m)" in sub:
      sub = sub.replace( " (m)", "" )
      micro_subs.append( Player.Submission( sub, SubmissionType.MICRO ) )
      continue
      
    regular_subs.append( Player.Submission( sub, SubmissionType.REGULAR ) )

  return regular_subs, micro_subs