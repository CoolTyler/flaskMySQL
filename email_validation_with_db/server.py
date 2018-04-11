from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
mysql = MySQLConnector(app,'tylerdb')
app.secret_key = "SecretsSecretsAreNoFunSecretsSecretsHurtSomeone"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def create():
  query = "INSERT INTO users (email, created_at, updated_at) VALUES (:email, NOW(), NOW())"
  data = {
    'email': request.form['email']
  }
  mysql.query_db(query, data)

def display():
  query = "SELECT * FROM users"
  emails = mysql.query_db(query)
  return render_template('success.html', emails=emails)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/process', methods=["POST"])
def validate():
  email_val = True
  if len(request.form["email"]) < 1:
    flash("E-mail field cannot be empty!", "wrong")
    email_val = False
  elif not EMAIL_REGEX.match(request.form["email"]):
    flash("Not a vaild e-mail, smart guy", "wrong")
    email_val = False
  if email_val == True:
    flash("Good job.", "success")
    create()
    return display()
  return redirect('/')

app.run(debug=True)