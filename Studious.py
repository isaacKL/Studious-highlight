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
        
        for course in self.courses:
            self.classes.append({
                "name":course['name'],
                "grading standard":course['apply_assignment_group_weights']
            })
        
    #def check(self):

        #see if gs- [name] exist
        #see if gs contains each course

            
    def initiate(self):
        if not self.sheets.getFile():
            self.sheets.createSpreadsheet()
            self.sheets.updateFormat(self.classes)
        
        #send to sheets to make new spreadsheet

    def update(self):
        #request canvas report 
        #separate updates and corrections
        #send update to sheets
        #send correction to sheets
        for course in self.courses:
            assignments=self.canvas.get_assignments(courses['id'],self.today)
            break
            if assignments != None:
                self.sheets.updateValues(assignments)
        
        
                
if __name__=='__main__':
    me= Studius('2006~hvjl4mDeAR2jYoxOYWkCbgp5Xpm7NSMCnNG9SRJ7hscjc6k3xzA6Aq4vW9TxtuRO')
    me.initiate()
    me.update()
    