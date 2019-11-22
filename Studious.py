from  canvas import CanvasAPI
import Desktop
from datetime import datetime
import collections

now=datetime.now()
today=now.strftime('%y-%m-%d')
homework=[]
print(today)
test=[]
def main():
    #main stuff
    canvas=CanvasAPI('2006~hvjl4mDeAR2jYoxOYWkCbgp5Xpm7NSMCnNG9SRJ7hscjc6k3xzA6Aq4vW9TxtuRO','https://mst.instructure.com')
    courses=canvas.get_courses()
    for course in courses:
        assignments=canvas.get_assignments(course['id'],today)
         
                
if __name__=='__main__':
    main()