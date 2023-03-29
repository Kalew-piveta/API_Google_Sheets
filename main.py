from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '13-zWme2y1HKaT9h_gSJlxbSKHslFFVTOTRzVaVQGQuw'
SAMPLE_RANGE_NAME = 'Página1!A1:B13'


def main():
    creds = None
    
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'cliente_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        # Ler informações do Google Sheets
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        print(values)
        # Adicionar/Editar valores no Google Sheets
        values_add = [
            ['Janeiro/22', 'R$ 70.000,00'],
            ['Fevereiro/22', 'R$ 80.000,00']
        ]
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range='Página1!A14', 
                                    valueInputOption='USER_ENTERED', 
                                    body={"values":values_add}).execute()

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()