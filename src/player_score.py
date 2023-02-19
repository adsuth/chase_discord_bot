import utils

class PlayerScore:
  """
  Storage structure for player scores.
  """
  def __init__( self, raw, name ):
    # todo : this is not reflective of final structure
    self.raw   = raw
    self.name  = name
    self._defined_in_session = False
  
  def initialise_player_data( self ):
    if self._defined_in_session:
      return
    
    self._defined_in_session = True
    data = self.raw
    
    self.total_points = data[ 12 ]
    self.real_total   = sum( utils.score_list_to_int( data[ 12:19 ] ) )
    self.submissions  = data[ 20: ]
  
  def __dict__( self ):
    return {
      "Name": self.name,
      "Total Points": self.total_points,
    }
  
  def get_scores_dict( self ):
    return {
      "Total Points":               self.total_points,
      "Total Points (incl. Bonus)": self.real_total,
    }
  
  def get_submissions( self ):
    return self.submissions
  
  def get_scores_dict_items( self ):
    return self.get_scores_dict().items()

def parse_raw_scores( raw_data ):
  output = {}
  for row in raw_data:
    key, name = row[0].lower(), row[0]
    
    output[ key ] = PlayerScore(
      row, 
      name
    )
  
  return output