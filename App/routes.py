from flask import Blueprint, render_template, request, redirect, url_for, flash
from TicketMaster.App.models import db, users_collection
from TicketMaster.App.forms import UserForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

main = Blueprint('main', __name__)

ticket_counter = 1  # Initialize ticket counter

def generate_code():
    global ticket_counter
    ticket_code = f'{ticket_counter:03d}'
    ticket_counter += 1
    return f'{ticket_code}'

@main.route('/')
def index():
    form = UserForm()
    return render_template('index.html', form=form)

@main.route('/submit', methods=['POST'])
def submit():
    form = UserForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        phone_number = form.phone_number.data
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
            return render_template('success.html', email=email, code=code)
        except Exception as e:
            flash('An error occurred while sending the email.')
            print(str(e))
            return redirect(url_for('main.index'))

    return render_template('index.html', form=form)

@main.route('/print_receipt/<code>')
def print_receipt(code):
    # Assuming you have a receipt template named 'receipt.html'
    # Update this template to include the necessary information for the receipt
    return render_template('receipt.html', code=code)

