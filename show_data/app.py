from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import requests
import pymongo

app = Flask(__name__)
app.config['SESSION_COOKIE_NAME'] = 'show_data'
app.secret_key = '7dfe6f0ed39d7be9f39d02495da2d0fc07f611cb81b7030d'

AUTH_SERVICE_URL = 'http://auth_service:5000/login'


# connect with the mongodb here
# MongoDB configuration
mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
mongo_db = mongo_client["my_db"]
mongo_collection = mongo_db["temperature_stats"]



@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    # Check if the user is already logged in
    if 'loggedin' in session and session['loggedin']:
        return redirect(url_for('show_data'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            response = requests.post(AUTH_SERVICE_URL, json={'username': username, 'password': password, 'app_name':'user'})
            if response.status_code == 200:
                session['loggedin'] = True
                session['username'] = username  # Store username in session
                return redirect(url_for('show_data'))  
            else:
                msg = "Invalid login credentials"  
        except requests.exceptions.RequestException as e:
            msg = f"Error communicating with the auth service: {e}"  # Display error message

    return render_template('login.html', msg=msg)


@app.route('/show_data', methods=['GET','POST'])
def show_data():
    try:
        # Get the latest record from MongoDB (sort by the insertion order)
        last_record = mongo_collection.find().sort([('$natural', -1)]).limit(1)
        last_record = last_record.next()
        if last_record:
            data = {
                "max_temperature": last_record["max_temperature"],
                "max_day": last_record["max_day"],
                "min_temperature": last_record["min_temperature"],
                "min_day": last_record["min_day"],
                "avg_temperature": last_record["avg_temperature"]
            }
        else:
            data = {
                "max_temperature": 'N/A',
                "max_day": 'N/A',
                "min_temperature": 'N/A',
                "min_day": 'N/A',
                "avg_temperature": 'N/A'
            }

        return render_template('show_data.html', data=data)

    except Exception as e:
        return f"Error retrieving data: {e}", 500



@app.route('/logout', methods=['POST'])
def logout():
    try:
        # Clear session data
        session['loggedin'] = None
        session['username'] = None
        return redirect(url_for('login'))
    except Exception as e:
        return f"Error during logout: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
