from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt  
from mysqlconnection import connectToMySQL
import re
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "#!@$5-581#%6&.,[2381%$!#"
mysql = connectToMySQL('login_registration')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def initsession():
    session.clear()
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    session['pw_confirm'] = request.form['pw_confirm']


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success', methods=['POST'])
def register():
    isValid = True
    
    initsession()
    if "Reset" in request.form:
        if request.form['Reset'] == 'Reset':
            session.clear()    

    elif "Submit" in request.form: 
    
        query = "SELECT * FROM users WHERE email = %(email)s"
        data = {
            'email' : request.form['email']
        }
        existing = mysql.query_db(query, data)

        if len(existing):
            flash("Email address is already taken.", 'email')
            isValid = False

        if len(request.form['first_name']) <= 2 or len(request.form['first_name']) >= 25:
            flash('First name must be between 2-25 characters long.', 'first_name')
            isValid = False
        
        if len(request.form['last_name']) <= 2 or len(request.form['last_name']) >= 25:
            flash('Last name must be between 2-25 characters long.', 'last_name')
            flash('If your last name is longer than 25 characters, please abbreviate.', 'last_name')
            isValid = False

        if len(request.form['email']) <=0 or len(request.form['email']) >= 50:
            flash('Please enter an email address no longer than 50 characters long.', 'email')
            isValid = False
        elif not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid Email Address!", 'email')

        if len(request.form['password']) <=0 or len(request.form['pw_confirm']) <=0:
            flash('Please provide a password', 'password')
            isValid = False
        elif len(request.form['password']) >=255 or len(request.form['pw_confirm']) >=255:
            flash('Please provide a password', 'password')
            isValid = False

        if request.form['password'] != request.form['pw_confirm']:
            flash('Passwords do not match!', 'pw_confirm')
            isValid = False

        elif isValid == True:
            bc_password = bcrypt.generate_password_hash(request.form['password'])
            query = "INSERT INTO users (first_name, last_name, email, pw, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
            data = {
                'first_name' : request.form['first_name'],
                'last_name' : request.form['last_name'],
                'email' : request.form['email'],
                'password' : bc_password
            }
            mysql.query_db(query, data)
            return render_template('index2.html')

    return redirect('/')
    
    

@app.route('/login', methods=['POST'])
def login():
    session.clear()
    session['email2'] = request.form['email2']
    session['password2'] = request.form['password2']
    if "Login" in request.form:

        query = "SELECT * FROM users WHERE email = %(email)s"
        data = {
            'email' : request.form['email2'],
        }
        #  AND pw = %(password)s
        login_query = mysql.query_db(query, data)
        print(login_query)
        
        if login_query:
            if len(request.form['password2']) < 1 or len(request.form['password2']) > 255:
                flash('incorrect email/password!', 'login')
            if bcrypt.check_password_hash(login_query[0]['pw'], request.form['password2']):
                session['logged_in'] = True
                return render_template('index2.html')
            else:
                return redirect('/')
        if len(request.form['email2']) < 1:
            flash('Incorrect email/password!', 'login')
        elif not EMAIL_REGEX.match(request.form['email2']):
            flash('Invalid email/password!', 'login')
        else:
            flash('Incorrect email/password!', 'login')
        
        return redirect('/')

    else:
        return redirect('/')


@app.route('/back', methods=['POST'])
def back():
    session.clear()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)