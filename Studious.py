from  canvas import CanvasAPI
from sheets import Sheets
import Desktop
from datetime import datetime
import collections


class Studius:
        
    def __init__(self,access_token:str):
        #main stuff
        self.now=datetime.now()
        self.today=self.now.strftime('%y-%m-%d')
        self.canvas=CanvasAPI(access_token,'https://mst.instructure.com')
        self.sheets=Sheets(self.canvas.name)
        self.courses=self.canvas.get_courses()
        self.classes=[]
        self.sheets.getFile()
        for course in self.courses:
            self.classes.append({
                "name":course['name'],
                "grading standard":course['apply_assignment_group_weights']
            })
        
    #def check(self):

        #see if gs- [name] exist
        #see if gs contains each course

            
    def initiate(self):
        self.sheets.createSpreadsheet()
        self.sheets.updateFormat(self.classes)
        #send to sheets to make new spreadsheet

    def update(self,course=None):
        #request canvas report 
        #separate updates and corrections
        #send update to sheets
        #send correction to sheets
        assignments=self.canvas.get_assignments(self.courses[2]['id'],self.today)
        print(assignments)
        print()
        
                
if __name__=='__main__':
    me= Studius('2006~hvjl4mDeAR2jYoxOYWkCbgp5Xpm7NSMCnNG9SRJ7hscjc6k3xzA6Aq4vW9TxtuRO')
    #me.update()
    