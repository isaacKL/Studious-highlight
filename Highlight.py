from Studious import Studious
from Database import Database
from googleapiclient.discovery import build
import sched, time
from google.auth.credentials import Credentials as creds
import pickle
import dill
class Highlight:
    
   
    def check(self):
        #check google speadsheet
        db=Database()
        db.create_connection()
        creds='AIzaSyCifncjO5VqPxgEkIEzWTmzjvRwCS-1Evc'
        spreadsheet_id="1JS8rRdfI94wIi8h-N0-YCaAh2C0_RaSgn5zxvLPgrAk"
        service = build('sheets', 'v4',developerKey=creds)
        sheets=service.spreadsheets()
        _range="A2:E110"
        drive=build('drive','v3',developerKey=creds)
        result = sheets.values().get(spreadsheetId=spreadsheet_id,
                                    range=_range).execute()
        values = result.get('values', [])

        if not values:
            print('No new queries')
        else:
            for row in values:
                print(values)
                packet={
                    "firstName":row[2],
                    "lastName":row[3],
                    'email':row[1],
                    "token":row[4],
                }
                db.updateData(packet)
        db.close()

        '''if so:
            db insert'''

    def process(self):
        self.check()
        #routine run through studious with db listing
        #add db grab
        db=Database()
        db.create_connection()
        returnList=db.selectMembers()
        
        if len(returnList)>0:
            auth=open('token.pickle','rb')
            oauth=pickle.load(auth)
            updateTimes=[]
            for row in returnList:
                print(row)
                if row.Oauth!="":
                    
                    
                    '''print(row.Oauth[2:-1])
                    s=bytes(row.Oauth[2:-1],encoding="utf-8",errors="strict")
                    auth=pickle.loads(s)
                    
                    print(type(auth),": \n",auth)                    '''
                    student=Studious(row.Token,oauth,row.Email)
                    student.initiate()
                    updateTimes.append(student.update())
        db.close()

    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/drive.metadata.readonly',
                        'https://www.googleapis.com/auth/drive.file',
                        'https://www.googleapis.com/auth/gmail.readonly']
        self.process()
        self.scheduele=sched.scheduler(time.time,time.sleep)
        self.scheduele.enter(10,1,self.process)
        


if __name__=="__main__":
    hh=Highlight()
    