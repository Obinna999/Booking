import sqlite3 as sql 

dbCon = sql.connect("Restaurant.db")

"dbCouror is a variable"
dbCursor = dbCon.cursor()