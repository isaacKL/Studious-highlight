CREATE TABLE Students (
 Id int NOT NULL AUTO_INCREMENT,
 FirstName varchar(255) NOT NULL,
 LastName varchar(255),
 Email  varchar(255) NOT NULL,
 Token  varchar(500) NOT NULL,
 OAuth BLOB(8000) NOT NULL,
 Class int,
 Major varchar(150),
 PRIMARY KEY (Id)
)
