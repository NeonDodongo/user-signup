from flask import Flask, redirect, request, render_template

import cgi
import os
import jinja2

app = Flask(__name__)

app.config['DEBUG'] = True

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index', methods=['POST'])
def log_in():

    user_name = request.form['user-name']
    pw = request.form['password']
    confirm_pw = request.form['confirm']
    email = request.form['email']

    user_name_err = ''
    pw_err = ''
    confirm_err = ''
    email_err = ''

    if len(user_name) < 3 or len(user_name) > 20:
        user_name_err = "Invalid username, must be between 3 and 20 characters."
    if len(pw) < 3 or len(pw) > 20:
        pw_err = "Invalid password must be between 3 and 20 characters"
    if confirm_pw != pw:
        confirm_err = "Passwords do not match."
    if len(email) < 3 and len(email) > 20:
        email_err = "Invalid length, must be between 3 and 20 characters."
    else:
        at_count = 0
        p_count = 0
        space_count = 0
        
        for char in email:
            if char == "@":
                at_count += 1
            elif char == ".":
                p_count += 1
            elif char == ' ':
                space_count += 1
                email_err = "Email cannot contain spaces."
                break
            if at_count > 1 or p_count > 1 or at_count == 0 or p_count == 0:
                email_err = "Invalid characters."
                break

        

    if user_name_err or pw_err or confirm_err or email_err:
        return render_template('index.html', user_name=user_name, email=email, user_name_err=user_name_err, 
                                pw_err=pw_err, confirm_err=confirm_err, email_err=email_err)
    else:
        return render_template('welcome.html', user_name=user_name, email=email)


app.run()

