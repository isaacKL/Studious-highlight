
from __future__ import print_function
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pyodbc
from pyodbc import Error
from os.path import join
    
class Token:
            
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/drive.metadata.readonly',
                        'https://www.googleapis.com/auth/drive.file',
                        'https://www.googleapis.com/auth/gmail.readonly']
        self.creds=None
        self.connectionString= (
            'DRIVER={MySQL ODBC 8.0 ANSI Driver};'
            'SERVER=studious.col7oouaxi6f.us-east-1.rds.amazonaws.com;'
            'UID=IC_DEV;'
            'PWD=db_instance;'
            'DATABASE=innodb;'
            'Port=3437;'
            'charset=utf8mb4;'
            
        )
        self.insertStatement="INSERT INTO Students (Email,Oauth) VALUES (?,?);"
        self.sess={}
        
        
    def create_connection(self):
        self.connection=pyodbc.connect(self.connectionString)
        self.connection.setencoding( encoding='utf-8')
        self.cursor=self.connection.cursor()

        #if conn=None :
    def close(self):
        self.connection.close()
        
    def insertMemberData(self,email,token):

        self.cursor.execute(self.insertStatement,(email,token))
        self.connection.commit()
        
    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def get(self):
        if os.path.exists(self.resource_path('token.pickle')):
            with open(self.resource_path('token.pickle'), 'rb') as token:
               
                self.creds = pickle.load(token)
            # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow =  InstalledAppFlow.from_client_secrets_file(
                    self.resource_path('credentials.json'), scopes=self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle','wb') as token:
                pickle.dump(self.creds,token)
              
        
        self.user=build('gmail','v1',credentials=self.creds)
        x=self.user.users()
        x=x.getProfile(userId='me').execute()
        email=x['emailAddress'].replace('umsystem','mst')
        with open(self.resource_path('token.pickle'),'rb') as token:
            d=token.read()
            print(str(d))
            self.insertMemberData(email,str(d))

        #self.insertMemberData(token)

if __name__=="__main__":
    print("started")
    token=Token()
    token.create_connection()
    token.get()
    token.close()