import os
import sqlite3
import hashlib
import pickle
import subprocess
from flask import Flask, request
import re

app = Flask(__name__)

# VULNERABILITATE 1: Hardcoded Secrets (Chei secrete lăsate în cod)
AWS_ACCESS_KEY = "AKIA1234567890EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # VULNERABILITATE 2: Weak Hashing (Utilizarea MD5 care este nesigur)
    # Parolele nu ar trebui stocate folosind MD5
    hashed_password = hashlib.md5(password.encode()).hexdigest()

    conn = get_db_connection()
    cursor = conn.cursor()

    # VULNERABILITATE 3: SQL Injection
    # Concatenarea directă a string-urilor permite atacatorilor să manipuleze interogarea
    query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + hashed_password + "'"
    cursor.execute(query)
    
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login successful"
    return "Login failed"

@app.route('/ping', methods=['GET'])
def ping_service():
    address = request.args.get('address')
    
    # Input validation: allow only IPs and hostnames (simple regex).
    if not address or not re.match(r'^[a-zA-Z0-9.\-]+$', address):
        return "Invalid address", 400
    
    # Secure command execution: no shell, pass argument list
    subprocess.call(['ping', '-c', '1', address])
    
    return "Ping executed"

@app.route('/import', methods=['POST'])
def import_data():
    data = request.data
    
    # VULNERABILITATE 5: Insecure Deserialization
    # 'pickle' nu trebuie folosit niciodată pe date din surse externe
    obj = pickle.loads(data)
    
    return "Data imported"

if __name__ == '__main__':
    
    # VULNERABILITATE 6: Debug Mode Enabled in Production
    app.run(debug=True)
