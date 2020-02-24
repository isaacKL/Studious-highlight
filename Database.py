import pyodbc
from pyodbc import Error
class Database:
        
    def __init__(self):
        #self.check(info['location'],info['name'])
        self.connectionString= (
            'DRIVER={MySQL ODBC 8.0 ANSI Driver};'
            'SERVER=studious.col7oouaxi6f.us-east-1.rds.amazonaws.com;'
            'UID=IC_DEV;'
            'PWD=db_instance;'
            'DATABASE=innodb;'
            'Port=3437;'
            'charset=utf8mb4;'
            
        )
        self.updateStatement="UPDATE Students SET FirstName=?,LastName=?,Token=? WHERE Email=?;" 
        self.insertStatement="INSERT INTO Students(FirstName,LastName,Email,Token,Oauth) VALUES (?,?,?,?,?)"
        self.selectStatement="SELECT Token,Oauth,Email FROM Students"
        
    #def create(self):

    def create_connection(self):
        try:
            self.connection=pyodbc.connect(self.connectionString)
            self.connection.setencoding(encoding='utf-8')
            self.cursor=self.connection.cursor()

        except Error as e:
            print("Error: ",e)            
        #if conn=None :
    def close(self):
        self.cursor.close()
        self.connection.close()

    def insertMemberData(self,data):

        self.cursor.execute(self.insertStatement,
            (data["First"],data["Last"],data["Email"],data["Token"],data["oAuth"]))
        self.connection.commit()
        
        #return result
        

    def selectMembers(self):
        with self.cursor as cursor:
            cursor.execute(self.selectStatement)
            return cursor.fetchall()

    def updateData(self,data):
        
        with self.cursor as cursor:
            cursor.execute(self.updateStatement,(data['firstName'],data['lastName'],data['token'],data['email']))
            cursor.commit()


if __name__ == "__main__":
    #db= Database({"name":"hi","location":"yrs"})
    db.create_connection(r"C:\\Users\icmuz\Documents\Studious.accdb")
    