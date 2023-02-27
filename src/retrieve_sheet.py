from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
from functools import cache
from pprint    import pprint

from global_variables import SCOPES
from global_variables import CHASE_VGM_SCOREBOARD_ID
from global_variables import CHASE_VGM_SCOREBOARD_RANGE
from utils import dlog

# If modifying these scopes, delete the file token.json.



@cache
def retrieve_values():
    """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
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
          range         = CHASE_VGM_SCOREBOARD_RANGE
        ).execute()
        
        values = result.get( "values", [] )

        if not values:
            print("No data found.")
            return
    
        values = [ value for i, value in enumerate( values ) if i != 0 ]

        return values

        
    except HttpError as err:
        print(err)
