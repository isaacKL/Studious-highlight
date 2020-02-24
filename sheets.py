from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import builtins
import  time

class Sheets:

    def __init__(self,name,token):
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
        self.creds=token 
        self.sheetInfo={}

        # Save the credentials for the next run
        #self.creds="AIzaSyCifncjO5VqPxgEkIEzWTmzjvRwCS-1Evc"
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.sheets=self.service.spreadsheets()
        self.drive=build('drive','v3',credentials=self.creds)
        #self.gmail=build('gmail','v1',credentials=self.creds) 

    def getFile(self,file_id=False):
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
                    if file_id:
                        return file.get('id')
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

    def total(self,cell,course):
        if cell ==  -1:
            print('No new stuff')
            return["=B9","=B9"]
        else:
            abc=["A","B","C","D","E","F","G","H","I","J","K","L"]
            letter1=abc[abc.index(cell[0])+1]
            letter2=abc[abc.index(cell[0])+2]
            rec_points="=sum("+letter1+"9:"+letter1+str(int(cell[1])-1)+")"
            total_points="=sum("+letter2+"9:"+letter2+str(int(cell[1])-1)+")"
            t=[[rec_points,total_points]]
            request = {
                "valueInputOption": "USER_ENTERED",
                "data": [{
                    "range": course+"!"+letter1+cell[1]+":"+letter2+cell[1],
                    "majorDimension": 'ROWS',
                    "values": t
                }],
                "includeValuesInResponse": True,
            }
            response=self.sheets.values().batchUpdate(spreadsheetId=self.sheetInfo['spreadsheetId'],body=request).execute()
            
            
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



    def updateValues(self,assignments,course,exam=False):
        #assignment{name, points,points received,class}
        _id=0
        _hidden=4 if not exam else 5
        print(course+": ","Exams" if exam else "Homework",len(assignments))
        #print(assignments)
        cell=-1
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
        cell=[response.get('values')[0][0][1],str(int(response.get('values')[0][0][2:]))]
        print(cell)
      
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
        
        self.total(cell,course)
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    def callback(self,request_id, response, exception):
        if exception:
            # Handle error
            print(exception)
        else:
            print("Permission Id: %s" % response.get('id'))

    def transferPermission(self,file_id,transfer_email):
                
        batch = self.drive.new_batch_http_request(callback=self.callback)
        user = {
            'type': 'user',
            'role': 'owner',
            'emailAddress': transfer_email
        }
        jose = {
            'type': 'user',
            'role': 'writer',
            'emailAddress': 'ic77f@umsystem.edu'
        }
        batch.add(self.drive.permissions().create(
                fileId=file_id,
                body=user,
                fields='id',
        ))
        batch.add(self.drive.permissions().create(
                fileId=file_id,
                body=jose,
                fields='id',
        ))        
        batch.execute()
    
if __name__ == '__main__':
    sheets=Sheets("Isaac Coppage")
    sheets.createSpreadsheet()
    #sheets.updateValues()
