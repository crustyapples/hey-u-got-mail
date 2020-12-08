from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a the spreadsheet.
HYGM_SPREADSHEET_ID = '1Au1m_9cP23aayyt0jgmTq0PIa3rjZCesh48FkddXo8E'
EMAIL_RANGE_NAME = 'Response!A2:W'

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=HYGM_SPREADSHEET_ID,
                                range=EMAIL_RANGE_NAME).execute()
    values = result.get('values', [])
    
    results_d = {}
    results_o = {}
    # creates dictonary of composition {date: [type of order]}
    for d in values:
        date = d[0].split()[0]
        results_d.setdefault(date,[])
        results_d[d[0].split()[0]].append(d[2])

        order_type = d[2]
        results_o.setdefault(order_type,[])
        results_o[d[2]].append(d[0])
    
    SINGLE_CARD = len(results_o['Send ONE card to somebody for $2'])
    MULTIPLE_CARD = len(results_o['Send MULTIPLE cards to several people at $2 per card'])
    DONATION = len(results_o['Make a donation for us to send the cards to our partner nursing homes'])

    print(f"SALES: \n Single Card: {SINGLE_CARD} \n Multiple Cards: {MULTIPLE_CARD} \n Donations: {DONATION} \n Current Total Card Orders: {SINGLE_CARD + MULTIPLE_CARD}")
    
    with open("orders.txt", "a+") as c:
        c.truncate(0)
        c.write(f"SALES: \n Single Card: {SINGLE_CARD} \n Multiple Cards: {MULTIPLE_CARD} \n Donations: {DONATION} \n Current Total Card Orders: {SINGLE_CARD + MULTIPLE_CARD}")

if __name__ == '__main__':
    main()