from flask import Flask, redirect, request, session, flash, render_template
from mysqlconnection import MySQLConnector
import re
from flask_bcrypt import Bcrypt


app = Flask(__name__)
mysql = MySQLConnector(app, "users")
bcrypt = Bcrypt(app)
app.secret_key = "SecretsSecretsAreNoFunSecretsSecretsHurtSomeone"
email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/reg', methods=["POST"])
def process_reg():
  err_flag = False
  # first name validation
  if not request.form['first_name'].isalpha():
    err_flag = True
    flash('Name can include letters only')    
  if len(request.form["first_name"]) < 2:
    err_flag = True
    flash("Name must be at least 2 characters")
    #  last name validation
  if not request.form['last_name'].isalpha():
    err_flag = True
    flash('Name can include letters only')    
  if len(request.form["last_name"]) < 2:
    err_flag = True
    flash("Name must be at least 2 characters")
    # email validation
  if len(request.form["email"]) < 2:
    err_flag = True
    flash('Your email must be at least 1 characters')
  if not email_regex.match(request.form['email']):
    err_flag = True
    flash('Not a valid email')
  # password validation
  if len(request.form["password"]) < 2:
    err_flag = True
    flash('Password must be longer than 2 characters')
  if request.form['password'] != request.form['confirm_pass']:
    err_flag = True
    flash('Passwords do not match')
    # redirect below
    
  if err_flag:
    return redirect('/')
  else:
    query = "INSERT into user (first_name, last_name, email, password, created_at, updated_at) values(:first_name, :last_name, :email, :password, NOW(), NOW())"
    
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    
    data = {
      "first_name": request.form["first_name"],
      "last_name": request.form["last_name"],
      "email": request.form["email"],
      "password": pw_hash
    }
    mysql.query_db(query, data)
    
    return redirect('/success') 

@app.route("/login", methods=["POST"])
def login():
  query = "SELECT * from user where email = :email"
  data = { "email": request.form["email"]}
  user = mysql.query_db(query, data)
  if user:
    if bcrypt.check_password_hash(user[0]['password'],request.form["password"]):
      return redirect('/success')
    else:
      flash('your password is invalid')
      return redirect('/')
  else:
    flash("Email doesn't exist")
    return redirect('/')

@app.route('/success')
def success_page():
  return render_template('success.html')  
  

app.run(debug=True)