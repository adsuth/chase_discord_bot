class PlayerScore:
  """
  Storage structure for player scores.
  """
  def __init__( self, raw, name, score ):
    self.raw   = raw
    self.name  = name
    self.score = score
  
  def __dict__( self ):
    return {
      "name": self.name,
      "score": self.score,
    }
  

def parse_raw_scores( raw_data ):
  output = {}
  for row in raw_data:
    key, name, score = row[0].lower(), row[0], row[12]
    
    output[ key ] = PlayerScore(
      row, 
      name,
      score,
    )
  
  return output