import os

from convert import generate_text

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError 

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1qQkew3843KCitycmp2--PiU0B-YFWe_wq7UK5gttgM4"

def main():
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        for row in range(2, 10):
            malay_word_response = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!A{row}:A{row}").execute()
            malay_word_values = malay_word_response.get("values")
            if not malay_word_values:
                break

            malay_word = malay_word_values[0][0]

            current_text_response = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!E{row}:E{row}").execute()
            current_text_values = current_text_response.get("values")
            current_text = current_text_values[0][0] if current_text_values else None

            if str(malay_word)[0] == "*" or current_text is not None:
                continue

            print(f"Malay word at a:{row} is {malay_word}")
            text = generate_text(malay_word)
            print(f"Text at a:{row} is {text}")
            
            sheets.values().update(spreadsheetId=SPREADSHEET_ID, range=f"Sheet1!E{row}:E{row}", valueInputOption="USER_ENTERED", body={"values": [[f"{text}"]]}).execute()

    except HttpError as error:
        print(error)

if __name__ == "__main__":
    main()