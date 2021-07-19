import Studious
import Database
from googleapiclient.discovery import build

def check():
    #check google speadsheet add creditional and spreadsheet ID
    creds=''
    spreadsheet_id=""
    service = build('sheets', 'v4',developerKey=creds)
    sheets=service.spreadsheets()
    _range="A2:F110"
    drive=build('drive','v3',developerKey=creds)
    result = sheets.values().get(spreadsheetId=32,
                                range=_range).execute()
    values = result.get('values', [])

    if not values:
        print('No new queries')
    else:
        for row in values:
            packet={
                "First":values[0],
                "Last":values[1],
                "Email":values[2],
                "Token":values[3],
                
            }
            fileLocation=values[4]
            #download
            #
            packet["oAuth"]=read_file(_file)

    '''if so:
        db insert'''

def process():
    #
    #routine run through studious with db listing
    x=1
if __name__=="__main__":
    check()