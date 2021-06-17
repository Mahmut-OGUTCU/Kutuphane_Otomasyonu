import mysql.connector

mydb = mysql.connector.connect(
    host= "localhost",
    user = "root",
    password = "",
    database = "kutuphane_otomasyonu"
)

mycursor = mydb.cursor()


