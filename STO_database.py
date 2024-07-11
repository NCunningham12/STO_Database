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
mycursor = db.cursor(buffered=True)

def input_trucks():
  input_auction = input("Auction Price?:\n")
  input_province = input("Province?:\n")
  input_book_cad = input("Canadian Book?:\n")

  input_data = (input_auction, input_province, input_book_cad)

  input_query = ("INSERT INTO inventory (auction_price, province, book_cad) VALUES (%s, %s, %s)")

  mycursor.execute(input_query, input_data)

  db.commit()

def calculate_bob():

  fetch_query = ("SELECT ROUND(auction_price, 2), province, ROUND(book_cad, 2) FROM inventory") 

  mycursor.execute(fetch_query)

  exchange = input("Current exchange rate:\n")

  for row in mycursor:
    
    auction_price = int(row[0])
    province = str(row[1])
    book_cad = int(row[2])
    book_usd = round(float(book_cad) * float(exchange), 2)

    if province.lower() == 'alb' or province.lower() == 'bc':
      auction_price += 1000
      auction_price *= 1.05
      canadian_price = round(auction_price, 2)

      us_price = round(float(canadian_price) * float(exchange), 2)
      us_price += 2300
      us_price *= 1.01
      total_us = round(us_price, 2)

      bob = round(float(book_usd) - float(total_us), 2)

      calculated_values = (book_usd, canadian_price, us_price, total_us, bob)

      input_query2 = ("UPDATE inventory SET book_usd = %s, canadian_price = %s, us_price = %s, total_us = %s, bob = %s")

      mycursor.execute(input_query2, calculated_values)

    elif province.lower() == 'ont':
      auction_price += 1000
      auction_price *= 1.13
      canadian_price = round(auction_price, 2)

      us_price = round(float(canadian_price) * float(exchange), 2)
      us_price += 3400
      us_price *= 1.01
      total_us = round(us_price, 2)

      bob = round(float(book_usd) - float(total_us), 2)

      calculated_values = (book_usd, canadian_price, us_price, total_us, bob)

      input_query2 = ("UPDATE inventory SET book_usd = %s, canadian_price = %s, us_price = %s, total_us = %s, bob = %s")

      mycursor.execute(input_query2, calculated_values)
    
    

  db.commit()

add_values = input("Would you like to add any values to the DB?\n")


if add_values.lower().startswith("y"):
  input_trucks()

fill_values = input("Would you like to fill out the DB values?\n")

if fill_values.lower().startswith("y"):
  calculate_bob()

mycursor.close()
db.close()