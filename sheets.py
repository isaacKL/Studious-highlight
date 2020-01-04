from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class Sheets:
    def __init__(self,name):
        self.name=name
        self.TEMPLATE_ID='1ORXhqhmBQ2urNkiw8LOHeX60yxtjL6QmmmazvZJouEM'
        self.POINT_SHEET='813406257'
        self.PERCENT_SHEET='2139402488'
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file','https://www.google']
        self.creds=None
        self.sheetInfo={}

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow =  InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scopes=self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheets=self.service.spreadsheets()
        self.drive=build('drive','v3',credentials=self.creds)


        

    def getFile(self):
        page_token = None
        query='GS - '+ self.name
        tempId=None
        while True:
            response = self.drive.files().list(q="name='"+query+"'",
                                                spaces='drive',
                                                fields='nextPageToken, files(id, name)',
                                                pageToken=page_token).execute()
            for file in response.get('files', []):
                # Process change
                print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
                self.sheetInfo['spreadsheetId']=file.get('id')
                break
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                return False
                print('Creating File')
                break
        

    def createSpreadsheet(self):
        body={
            "properties":{
                "title":'GS - '+ self.name
            }
        }
        print(self.sheets.get(spreadsheetId=self.TEMPLATE_ID).execute())
        self.sheetInfo=self.sheets.create(body=body).execute()
        
        #self.sheets.values().update(spreadsheetId=self.sheetInfo('spreadsheetId')).execute()
        #self.gradesheet=self.sheets.values().update(spreadsheetId='1q6g2ClWn5ndy4s9DSU_Tcg3nHG2caEMhSOu4R0yiHng',range='Running Points Based Class!A9:C24').execute()
        #self.gradesheet=self.sheets.create(body=template).execute()
        
    #done but find way to remove original sheet
    def updateFormat(self, courses=None):
        
        for course in courses:
            request=[]
            request={
                'destination_spreadsheet_id':self.sheetInfo['spreadsheetId']
            }
            response=self.sheets.sheets().copyTo(spreadsheetId=self.TEMPLATE_ID,sheetId=self.PERCENT_SHEET if course['grading standard'] else self.POINT_SHEET,body=request).execute()
            sheetId=response['sheetId']
            request=[]
            request.append({
                'updateSheetProperties':{
                    'properties':{
                        'sheetId':sheetId,
                        'title':course['name']
                    },
                    'fields':'title'
                }
            })
            body={'requests':request}
            x=self.sheets.update(spreadsheetId=self.sheetInfo['spreadsheetId'],body=body).execute()
            print(x)
    
    def updateValues(self,assignments):
        #assignment{name, points,points received,class}
        request=[]
        request.append({
            'findReplace':{
                'find':'Homework Total',

            }
        })
        body={
            'requests':request
        }
        response=self.sheets.values().batchUpdate(spreadsheetId=self.sheetInfo.get('spreadsheetId'),body=body).execute()
        print(response)

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    def cell(self,cell,value=None):
        if value ==  None:
            print('No value')
        else:
            return self.sheets
        # Call the Sheets API
        '''sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s' % (row[0], row[4]))'''

if __name__ == '__main__':
    sheets=Sheets()
    sheets.createSpreadsheet("Isaac Coppage")
    #sheets.updateValues()
