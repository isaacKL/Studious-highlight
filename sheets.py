from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request



class Sheets:
    def __init__(self,name):
        self.name=name
        self.enums={"COLUMNS","PROJECT","INTERSECTING_LOCATION"}
        self.TEMPLATE_ID='1ORXhqhmBQ2urNkiw8LOHeX60yxtjL6QmmmazvZJouEM'
        self.POINT_SHEET='813406257'
        self.POINT_SHEET_METADATA={"Homework":11,"Exam":11,"Other":11}
        self.PERCENT_SHEET='2139402488'
        self.PERCENT_SHEET_METADATA={"Section1":"A16","Section2":"D16","Section3":"G16","Section4":"J16","Section5":"D23","Section6":"G23"}
        self.PERCENT_SHEET_SECTIONS="A7:B12"
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/drive.metadata.readonly',
                        'https://www.googleapis.com/auth/drive.file',
                        'https://www.googleapis.com/auth/gmail.readonly']
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
        #self.gmail=build('gmail','v1',credentials=self.creds)



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
                if file.get('name')==query:
                    self.sheetInfo['spreadsheetId']=file.get('id')
                    return True

            page_token = response.get('nextPageToken', None)
            if page_token is None:
                print('Creating File')

                return False




    def createSpreadsheet(self):
        body={
            "properties":{
                "title":'GS - '+ self.name
            }
        }
        self.sheetInfo=self.sheets.create(body=body).execute()

        #self.sheets.values().update(spreadsheetId=self.sheetInfo('spreadsheetId')).execute()
        #self.gradesheet=self.sheets.values().update(spreadsheetId='1q6g2ClWn5ndy4s9DSU_Tcg3nHG2caEMhSOu4R0yiHng',range='Running Points Based Class!A9:C24').execute()
        #self.gradesheet=self.sheets.create(body=template).execute()

    #done but find way to remove original sheet
    def updateFormat(self, courses):

        for course in courses:
            request=[]
            request={
                'destination_spreadsheet_id':self.sheetInfo['spreadsheetId']
            }
            #response=self.sheets.sheets().copyTo(spreadsheetId=self.TEMPLATE_ID,sheetId=self.PERCENT_SHEET if course['grading standard'] else self.POINT_SHEET,body=request).execute()
            response=self.sheets.sheets().copyTo(spreadsheetId=self.TEMPLATE_ID,sheetId= self.POINT_SHEET,body=request).execute()
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
            x=self.sheets.batchUpdate(spreadsheetId=self.sheetInfo['spreadsheetId'],body=body).execute()
            

    def spreadsheet(self):
        self.sheetInfo=self.sheets.get(spreadsheetId=self.sheetInfo['spreadsheetId']).execute()

    def updateValues(self,assignments,course,exam=False):
        #assignment{name, points,points received,class}
        _id=0
        _hidden=4 if not exam else 5
        print(course+": ","Exams" if exam else "Homework",len(assignments))
        #print(assignments)
        
        request=[]
        response_id=9
        _start="A" if not exam else "E"
        _end="C" if not exam else "G"
        for sheet in self.sheetInfo['sheets']:
            if  sheet['properties']['title']==course:
                _id=sheet['properties']['sheetId']
        
        response=self.sheets.values().get(spreadsheetId=self.sheetInfo['spreadsheetId'],range=course+"!Q"+str(_hidden),valueRenderOption="FORMULA").execute()
        if not (response.get('values'))==None:
            response_id=int(response.get('values')[0][0][2:])-2
            
        request.append({
            'insertRange': {
                "range": {
                    "sheetId": _id,
                    "startRowIndex": response_id,
                    "endRowIndex": response_id+len(assignments),
                    "startColumnIndex": 0,
                    "endColumnIndex": 3
                },
                "shiftDimension": "ROWS"
            }
        })
        body={'requests':request}
        self.sheets.batchUpdate(spreadsheetId=self.sheetInfo['spreadsheetId'],body=body).execute()
        
        request = {
            "valueInputOption": "USER_ENTERED",
            "data": [{
                "range": course+"!"+_start+str(response_id)+":"+_end+str(response_id+len(assignments)),
                "majorDimension": 'ROWS',
                "values": assignments
            }],
            "includeValuesInResponse": False,
        }
        response=self.sheets.values().batchUpdate(spreadsheetId=self.sheetInfo['spreadsheetId'],body=request).execute()

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
