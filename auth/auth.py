from flask import Flask, request, jsonify, session, redirect, url_for
import time
# import mysql.connector
from mysql.connector import Error
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'mysql_db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'my_db'

mydb = MySQL(app)

@app.route('/login', methods=['GET','POST'])
def login():
    
    data = request.get_json()  # Get JSON data from request
    username = data.get('username')
    password = data.get('password')
    app_name = data.get('app_name')

    print("user_name : ",username)
    print("password : ",password)
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    cursor = mydb.connection.cursor(MySQLdb.cursors.DictCursor)
    if app_name=="admin":
        cursor.execute('SELECT * FROM admins WHERE username = %s AND password = %s', (username, password))
    elif app_name=="user":
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
    else:
        return jsonify({"error": "Invalid app identifier"}), 400
    
    account = cursor.fetchone()
    print("#"*50)
    if account:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
