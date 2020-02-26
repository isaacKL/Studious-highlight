import pyodbc
from pyodbc import Error
class Database:
        
    def __init__(self,info):
        #self.check(info['location'],info['name'])
        self.connectionString= (
            'DRIVER={MySQL ODBC 8.0 ANSI Driver};'
            'SERVER=studious.col7oouaxi6f.us-east-1.rds.amazonaws.com;'
            'UID=IC_DEV;'
            'PWD=db_instance;'
            'Port=3437'
            'charset=utf8mb4;'
        )
        self.updateStatement="UPDATE ? SET ?=? WHERE ? = ?" 
        self.insertStatement="INSERT INTO Students(FirstName,LastName,Email,Token,OAuth) VALUES (?,?,?,?,?)"
        
        
    #def create(self):

    def create_connection(self):
        try:
            self.connection=pyodbc.connect(self.connectionString)
            self.connection.setencoding(encoding='utf-8')
            self.cursor=self.connection.cursor()

        except Error as e:
            print("Error: ",e)            
        #if conn=None :
            
    def insertMemberData(self,data):
        result=self.cursor.execute(self.insertStatement,
            (data["First"],data["Last"],data["Email"],data["Token"],))
        print(result)
        #return result
        

    def updateData(self,value,field,where_value,where_field,table):
        
        with self.connection as con:
            con.execute(self.update_statement,(table,field,value,where_field,where_value))
        

if __name__ == "__main__":
    db= Database({"name":"hi","location":"yrs"})
    db.create_connection(r"C:\\Users\icmuz\Documents\Studious.accdb")
    