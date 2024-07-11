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
mycursor = db.cursor()

input_id = int(input("id?\n")) - 1

query1 = ("SELECT ROUND(auction_price, 2), province, ROUND(book, 2) FROM inventory") 

mycursor.execute(query1)
input_columns = mycursor.fetchall()[input_id]

auction_price = (input_columns[0])
province = (input_columns[1])
book = (input_columns[2])

# mycursor.close()
db.close()