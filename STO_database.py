from flask import Flask, render_template, request, redirect, url_for, flash
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

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")




@app.route("/")
def Index():
  cursor = db.cursor()
  select_query = "SELECT * FROM inventory"
  cursor.execute(select_query)
  records = cursor.fetchall()
  cursor.close()

  return render_template("index.html", records=records)



@app.route('/insert', methods = ['POST'])
def insert():
  if request.method == "POST":
    flash("Vehicle Data Inserted Successfully")
    auction_price = request.form['auction_price']
    province = request.form['province']
    book_cad = request.form['book_cad']
    cursor = db.cursor()
    cursor.execute("INSERT INTO inventory (auction_price, province, book_cad) VALUES (%s, %s, %s)", (auction_price, province, book_cad))
    db.commit()

    return redirect(url_for('Index'))
  

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
  flash("Vehicle Record Has Been Successfully Deleted")
  cursor = db.cursor()
  cursor.execute("DELETE FROM inventory WHERE id=%s", (id_data,))
  db.commit()
  return redirect(url_for('Index'))


@app.route('/update/', methods=['POST'])
def update():
  if request.method == 'POST':
    id_data = request.form['id']
    auction_price = request.form['auction_price']
    province = request.form['province']
    book_cad = request.form['book_cad']
    cursor = db.cursor()
    cursor.execute("""UPDATE inventory SET auction_price=%s, province=%s, book_cad=%s WHERE id=%s""", (auction_price, province, book_cad, id_data))
    flash("Vehicle Data Updated Successfully")
    db.commit()
    return redirect(url_for('Index'))
  
# @app.route('/update/<id_data>', methods=['GET'])
# def update_modal(id_data):
#   flash('Success! Id: ' + str(id_data))
#   return redirect(url_for('Index'))

@app.route('/calculate/', methods=['POST'])
def calculate_bob():
  cursor = db.cursor()

  exchange = 0.73

  cursor.execute("SELECT id, auction_price, province, book_cad FROM inventory")
  trucks = cursor.fetchall()

  for row in trucks:
    
    id = int(row[0])
    auction_price = float(row[1])
    province = str(row[2])
    book_cad = float(row[3])
    book_usd = round(float(book_cad) * float(exchange), 2)

    if province.lower() == 'alb' or province.lower() == 'bc':
      auction_price += 1000
      auction_price *= 1.05
      canadian_price = round(auction_price, 2)

      us_price = round(float(canadian_price) * float(exchange), 2)
      updated_us_price = us_price + 2300
      updated_us_price *= 1.01
      total_us = round(updated_us_price, 2)

      bob = round(float(book_usd) - float(total_us), 2)

    elif province.lower() == 'ont':
      auction_price += 1000
      auction_price *= 1.13
      canadian_price = round(auction_price, 2)

      us_price = round(float(canadian_price) * float(exchange), 2)
      updated_us_price = us_price + 3400
      updated_us_price *= 1.01
      total_us = round(updated_us_price, 2)

      bob = round(float(book_usd) - float(total_us), 2)

    calculated_values = (book_usd, canadian_price, us_price, total_us, bob, id)

    input_query2 = ("UPDATE inventory SET book_usd = %s, canadian_price = %s, us_price = %s, total_us = %s, bob = %s WHERE id = %s")

    cursor.execute(input_query2, calculated_values)

  db.commit()

  return redirect(url_for('Index'))



if __name__ == "__main__":
  app.run(debug = True)


# def input_trucks():
#   input_auction = input("Auction Price?:\n")
#   input_province = input("Province?:\n")
#   input_book_cad = input("Canadian Book?:\n")

#   input_data = (input_auction, input_province, input_book_cad)

#   input_query = ("INSERT INTO inventory (auction_price, province, book_cad) VALUES (%s, %s, %s)")

#   mycursor.execute(input_query, input_data)

#   db.commit()

# def calculate_bob():
#   cursor = db.cursor()

#   exchange = input("Current exchange rate:\n")

#   cursor.execute("SELECT id, auction_price, province, book_cad FROM inventory")
#   trucks = cursor.fetchall()

#   for row in trucks:
    
#     id = int(row[0])
#     auction_price = float(row[1])
#     province = str(row[2])
#     book_cad = float(row[3])
#     book_usd = round(float(book_cad) * float(exchange), 2)

#     if province.lower() == 'alb' or province.lower() == 'bc':
#       auction_price += 1000
#       auction_price *= 1.05
#       canadian_price = round(auction_price, 2)

#       us_price = round(float(canadian_price) * float(exchange), 2)
#       updated_us_price = us_price + 2300
#       updated_us_price *= 1.01
#       total_us = round(updated_us_price, 2)

#       bob = round(float(book_usd) - float(total_us), 2)

#     elif province.lower() == 'ont':
#       auction_price += 1000
#       auction_price *= 1.13
#       canadian_price = round(auction_price, 2)

#       us_price = round(float(canadian_price) * float(exchange), 2)
#       updated_us_price = us_price + 3400
#       updated_us_price *= 1.01
#       total_us = round(updated_us_price, 2)

#       bob = round(float(book_usd) - float(total_us), 2)

#     calculated_values = (book_usd, canadian_price, us_price, total_us, bob, id)

#     print(calculated_values)

#     input_query2 = ("UPDATE inventory SET book_usd = %s, canadian_price = %s, us_price = %s, total_us = %s, bob = %s WHERE id = %s")

#     cursor.execute(input_query2, calculated_values)

#   db.commit()

# add_values = input("Would you like to add any values to the DB?\n")


# if add_values.lower().startswith("y"):
#   input_trucks()

# fill_values = input("Would you like to fill out the DB values?\n")

# if fill_values.lower().startswith("y"):
#   calculate_bob()


db.close()