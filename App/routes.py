from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, User, Ticket
import random
import string
from twilio.rest import Client

main = Blueprint('main', __name__)

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def send_sms(phone_number, code):
    account_sid = 'your_twilio_account_sid'
    auth_token = 'your_twilio_auth_token'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f'Your ticket code is: {code}',
        from_='your_twilio_phone_number',
        to=phone_number
    )

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/submit', methods=['POST'])
def submit():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone_number = request.form['phone_number']

    user = User(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number)
    db.session.add(user)
    db.session.commit()

    code = generate_code()
    ticket = Ticket(code=code, user_id=user.id)
    db.session.add(ticket)
    db.session.commit()

    send_sms(phone_number, code)

    flash('Ticket generated and code sent to phone number!', 'success')
    return redirect(url_for('main.index'))
