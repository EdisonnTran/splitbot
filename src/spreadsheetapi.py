import os
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

class SpreadsheetAPI:

    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"] 
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

    def __init__(self):
        self.credentials = None
        if os.path.exists("token.json"):
            self.credentials = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                self.credentials = flow.run_local_server(port=0)
            with open("token.json", 'w') as token:
                token.write(self.credentials.to_json())
        
        try:
            service = build("sheets", "v4", credentials = self.credentials)
            self.sheets = service.spreadsheets()
        
        except HttpError as error:
            print(error)

    def add_spending(self): # params: self, title: str, cost: int, splitters: list[str]

        try:
            result = self.sheets.values().get(spreadsheetId=self.SPREADSHEET_ID, range="Sheet1!A2:E4").execute().get("values")[0][0]
            self.sheets.values().update(spreadsheetId=self.SPREADSHEET_ID, range="Sheet1!E5", valueInputOption="USER_ENTERED", body={"values": [['']]}).execute()
            print(result)
        
            # sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!E5", valueInputOption="")

        except HttpError as error:
            print(error)

def main():
    create = SpreadsheetAPI()
    create.add_spending()

if __name__ == "__main__":
    main()
