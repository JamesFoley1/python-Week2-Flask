from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
import re
app = Flask(__name__)
app.secret_key = "#!@$5-581#%6&.,[2381%$!#"
mysql = connectToMySQL('email')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    email = mysql.query_db("SELECT * FROM email")
    return render_template('index.html', email = email)

@app.route('/email', methods=['POST'])
def create():
    email_list = mysql.query_db("SELECT * FROM email")
    isValid = True

    for i in email_list:
        if request.form['email'] == i['email']:
            flash("Email already exists!")
            isValid = False

    if len(request.form['email']) <= 0:
        flash("Email cannot be blank!")
        isValid = False
    

    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        isValid = False

    elif isValid == True:
        session['email'] = request.form['email']
        flash('Success!')
        query = "INSERT INTO email (email, created_at, updated_at) VALUES (%(email)s, NOW(), NOW());"
        data = {
            'email': request.form['email'],
        }
        mysql.query_db(query, data)
        new_list = mysql.query_db("SELECT * FROM email")
        new_length = len(new_list)
        return render_template('index2.html', new_list = new_list, new_length = new_length)
        
    return redirect('/')

@app.route('/back', methods=['POST'])
def back():
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)