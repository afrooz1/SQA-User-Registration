
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'


client = MongoClient('mongodb://localhost:27017/')
db = client['registration_db']
users = db['users']


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    
    if not name or not email:
        flash('Name and email are required!', 'error')
        return redirect(url_for('index'))
    
    if not EMAIL_REGEX.match(email):
        flash('Invalid email format!', 'error')
        return redirect(url_for('index'))
    
    
    if users.find_one({'email': email}):
        flash('Email already exists!', 'error')
        return redirect(url_for('index'))
    
    
    users.insert_one({'name': name, 'email': email})
    flash('Registration successful!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)