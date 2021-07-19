
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import builtins
from os.path import join

class Token:
            
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                        'https://www.googleapis.com/auth/drive',
                        'https://www.googleapis.com/auth/drive.metadata.readonly',
                        'https://www.googleapis.com/auth/drive.file',
                        'https://www.googleapis.com/auth/gmail.readonly']
        self.creds=None
        

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
            with open(slef.resource_path('token.pickle'), 'rb') as token:
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
            with open('token.pickle', 'wb') as token:
                join("C\\Users\\%{User}\\downloads",token)
                pickle.dump(self.creds, token)

if __name__=="__main__":
    print("started")
    token=Token()
    token.get()