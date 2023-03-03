from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
from functools import cache
from classes import Submission, SubmissionType

from global_variables import PATH_TO_LEGACY_GAME_LIST, SCOPES
from global_variables import CHASE_VGM_SCOREBOARD_ID
from global_variables import CHASE_VGM_SCOREBOARD_RANGE
from utils import dlog

import config as cfg


@cache
def retrieve_values():
  """
  Gets the values from CHASE VGM sheet
  """
  creds = None
  # The file token.json stores the user"s access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists( "token.json" ):
    creds = Credentials.from_authorized_user_file( "token.json", SCOPES )
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh( Request() )
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES)
      creds = flow.run_local_server(port=0)
      
    # Save the credentials for the next run
    with open( "token.json", "w" ) as token:
      token.write( creds.to_json() )

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(
      spreadsheetId = CHASE_VGM_SCOREBOARD_ID,
      range     = CHASE_VGM_SCOREBOARD_RANGE
    ).execute()
    
    values = result.get( "values", [] )

    if not values:
      print("No data found.")
      return
  
    values = [ value for i, value in enumerate( values ) if i != 0 ]

    return values

    
  except HttpError as err:
    print(err)

@cache
def get_legacy_games():
  dlog( f"Retrieving Legacy games from {PATH_TO_LEGACY_GAME_LIST}" )
  legacy_games = []

  with open( PATH_TO_LEGACY_GAME_LIST ) as file:
    for line in file:
      game = Submission( line.strip(), None )
      game.type = SubmissionType.LEGACY
      legacy_games.append( game )
  
  return legacy_games