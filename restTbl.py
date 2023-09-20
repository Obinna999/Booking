from connect import * 

dbCursor.execute("CREATE TABLE guests ("
                 "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                 "name VARCHAR(255),"
                 "date DATE,"
                 "time TIME,"
                 "numGuest INT"
                 ")")






