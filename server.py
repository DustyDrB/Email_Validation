from flask import Flask, flash, render_template, request, redirect, session
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
mysql = MySQLConnector(app, 'email')
app.secret_key = "adorable_beagles"

mail_val = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

@app.route('/')
def index():
	query = "SELECT id, address FROM email"
	emails = mysql.query_db(query)
	return render_template('index.html', all_emails=emails)

@app.route('/success', methods=['POST', 'GET'])
def add_email():
	query = "SELECT * FROM email"
	address = mysql.query_db(query)
	if len(request.form['address']) < 1:
		flash['Email cannot be empty!']
		return redirect('/')
	elif not mail_val.match(request.form['address']):
		flash('Your email is not valid!')
		return redirect('/')
	else:
		query = "INSERT INTO email (address, date_created, date_updated) VALUES (:address, NOW(), NOW())"	
		data = {'address': request.form['address']}
		mysql.query_db(query, data)
		addresses = mysql.query_db("SELECT address FROM email")
   		return render_template('success.html', all_addresses=addresses)
if __name__ =="__main__":
	app.run(debug=True)