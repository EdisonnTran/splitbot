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
    # SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

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

    def add_spending(self, id: str, title: str, cost: float, splitters: list[str]): # params: self, title: str, cost: int, splitters: list[str]
        spreadsheet = self.sheets.values()
        try:

            # bad practice, in the future will store the current line in a variable and increment it.
            line = 1
            while spreadsheet.get(spreadsheetId=id, range=f"Sheet1!{line}:{line}").execute().get("values") != None:
                line += 1

            spreadsheet.update(spreadsheetId=id, range=f"Sheet1!A{line}", valueInputOption="USER_ENTERED", body={"values": [[f'{title}']]}).execute()
            spreadsheet.update(spreadsheetId=id, range=f"Sheet1!B{line}", valueInputOption="USER_ENTERED", body={"values": [[f'{cost}']]}).execute()
            spreadsheet.update(spreadsheetId=id, range=f"Sheet1!C{line}", valueInputOption="USER_ENTERED", body={"values": [[f'{splitters}']]}).execute()
        
            # sheets.values().update(spreadsheetId=SPREADSHEET_ID, range="Sheet1!E5", valueInputOption="")

        except HttpError as error:
            print(error)

def main():
    create = SpreadsheetAPI()
    print("complete")
    create.add_spending(create.SPREADSHEET_ID, "Shopping", 23.94, ["Tara", "Jill"])

if __name__ == "__main__":
    main()
