from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import requests
from datetime import datetime  # Import datetime to capture the current date

app = Flask(__name__)
app.secret_key = '43cd702275063c951f843fd001f031c2'
app.config['SESSION_COOKIE_NAME'] = 'enter_data'


AUTH_SERVICE_URL = 'http://auth_service:5000/login'

# MySQL configuration
app.config['MYSQL_HOST'] = 'mysql_db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'my_db'


mydb = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if the user is already logged in
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for('temperature'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            response = requests.post(AUTH_SERVICE_URL, json={'username': username, 'password': password, 'app_name':'admin'})
            if response.status_code == 200:
                session['loggedin'] = True
                session['username'] = username  # Store username in session
                return redirect(url_for('temperature'))  
            else:
                msg = "Invalid login credentials"  # Display message on invalid login
        except requests.exceptions.RequestException as e:
            msg = f"Error communicating with the auth service: {e}"  # Display error message

    return render_template('login.html', msg=msg)


@app.route('/temperature', methods=['GET', 'POST'])
def temperature():
    
    if request.method == 'POST':
        temp = request.form['temperature']
        day = request.form['day']  # Get the day from the form
        cursor = mydb.connection.cursor()
        cursor.execute('INSERT INTO temperature_data (temperature, day) VALUES (%s, %s)', [temp, day])
        mydb.connection.commit()
        msg = 'Temperature data added successfully!'
        return render_template('temperature.html', msg=msg)
    return render_template('temperature.html')


@app.route('/logout', methods=['POST'])
def logout():
    try:
        # Clear session data
        session['loggedin'] = None
        session['username'] = None
        # session.pop('loggedin', None)
        # session.pop('username', None)
        return redirect(url_for('login'))
    except Exception as e:
        return f"Error during logout: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
