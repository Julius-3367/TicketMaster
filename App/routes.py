from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, users_collection
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

main = Blueprint('main', __name__)

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone_number = request.form['phone_number']
    code = generate_code()

    user = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "code": code
    }
    users_collection.insert_one(user)

    sender_email = "korirjulius001@gmail.com"
    app_password = "eymr jlbq gesm skms"
    receiver_email = email

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Your Ticket Code"
    message.attach(MIMEText(f"Your ticket code is: {code}", "plain"))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.close()
        return render_template('success.html', email=email)
    except Exception as e:
        flash('An error occurred while sending the email.')
        print(str(e))
        return redirect(url_for('main.index'))

