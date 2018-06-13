from flask import Flask, render_template, redirect, request, session, flash
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "#41Ui14913841384@$%04@#$05f1"
mysql = connectToMySQL('leads_clients')
print("all the users", mysql.query_db("SELECT * FROM clients;"))

@app.route('/')
def index():
    clients = mysql.query_db("SELECT * FROM clients")
    print("Fetched all friends", clients)
    length = len(clients)
    print(length)
    return render_template('index.html', clients = clients, length=length)

if __name__ == "__main__":
    app.run(debug=True)