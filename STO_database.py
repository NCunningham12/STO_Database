import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

db = mysql.connector.connect(
  user=os.getenv("USER"), 
  password=os.getenv("PASSWORD"),
  host=os.getenv("HOST"),
  database=os.getenv("DATABASE")
)
cursor = db.cursor()

query = ("SELECT first, last, username FROM users")

cursor.execute(query)

for x in cursor:
  print(x)

cursor.close()
db.close()