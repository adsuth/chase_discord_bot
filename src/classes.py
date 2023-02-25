# # # # # # # # # # # # # # # # # # # # # # # #
#     Data Classes
# # # # # # # # # # # # # # # # # # # # # # # #

class EMBED_COLORS:
  error       = 0xff4063
  red       = 0xff4063
  bonus       = 0xfdd888
  balance     = 0xfdd888
  subs        = 0x2eff43
  spiritbomb  = 0x62efff
  cyan      = 0x62efff



# # # # # # # # # # # # # # # # # # # # # # # #
#     Enums
# # # # # # # # # # # # # # # # # # # # # # # #
class SubmissionType:
  MICRO   = 0
  REGULAR = 1

class AliasType:
  PLAYER = 0
  CHASER = 1
  
  
  
# # # # # # # # # # # # # # # # # # # # # # # #
#     Functional Classes
# # # # # # # # # # # # # # # # # # # # # # # #
class Alias:
  """
  Class to store the type of player name.
  eg: The Collector == CHASER, Aakadarr == PLAYER
  This is primarily to distinguish them when allocating points later on.
  """
  def __init__( self, name: str, type: AliasType ):
    self.name = name
    self.key  = name.lower().strip()
    self.type = type 
  
  def __repr__( self ):
    return self.key

  def __str__( self ):
    return self.key
  
  def __hash__( self ):
    return hash( ( self.key ) )

  def __eq__( self, other ):
    return self.key == other
          

class duodict:
  def __init__( self, dict: dict = None ):
    self.data = dict if not dict == None else {}
    
    if not dict == None:
      self.data |= { value: key for key, value in self.data.items() }
    
  def __repr__( self ):
    return str( self.data )
    
  def __str__( self ):
    return str( self.key )
  
  def get( self, key, default = None ):
    """Get item via the `key`. \n
    Will return `default` if not found (defaults to `None`)
    """
    key = key.lower().strip()
    return self.data.get( key, default )
  
  def find( self, key, default = None ):
    """Returns the item *of* the key. \n
    Will return `default` if not found (defaults to `None`)
    """
    key    = key.lower().strip()
    my_key = self.data.get( key, default ).key
    return self.data.get( my_key )
    