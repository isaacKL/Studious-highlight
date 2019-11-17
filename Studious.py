from  canvas import CanvasAPI
import Desktop
from datetime import datetime



today= datetime.strftime('%y-%m-%d')
homework=[]
test=[]
def main():
    #main stuff
    canvas=CanvasAPI('2006~hvjl4mDeAR2jYoxOYWkCbgp5Xpm7NSMCnNG9SRJ7hscjc6k3xzA6Aq4vW9TxtuRO','https://mst.instructure.com')
    courses=canvas.get_courses()
    
    for course in courses:
        assignments=canvas.get_assignments(course['id'],today)
        for assignment in assignments:
            due_date=datetime.strptime(assignment['due_at']-10,"%Y-%m-%d")
            if due_date>today and due_date<(today+7):
                homework.append(assignment)

if __name__=='__main__':
    main()