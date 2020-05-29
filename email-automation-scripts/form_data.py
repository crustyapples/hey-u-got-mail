from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import email_sender

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a the spreadsheet.
HYGM_SPREADSHEET_ID = '14_DZv16fwIgv5zp509Fm-NW_XDS0JM89sLAOXKBI36s'
EMAIL_RANGE_NAME = 'Form Responses 1!A2:P'

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
                'email-automation-scripts/credentials.json', SCOPES)
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
    # row[1] represents column(B) containing email addresses required
    emails = [r[1] for r in values]
    # calls function from email_senders to send template email to addresses captured in the form
    
    with open("email-automation-scripts/contacts.txt", "r") as c:
        sent_emails = c.read().split(',')
    
    print(sent_emails)
    print(emails)
    
    emailSend = list(filter(lambda x: True if x not in sent_emails else False, emails))
    print(emailSend)
    
    if len(emailSend) != 0:
        with open('email-automation-scripts/contacts.txt', "a+") as c:
            c.write(','+','.join(email_sender.send_emails(emailSend)))
    else:
        print("No more new emails to contact")
    
if __name__ == '__main__':
    main()