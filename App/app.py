from flask import Flask
from pymongo import MongoClient
from App.routes import main

app = Flask(__name__)
app.config.from_object('App.config.Config')

client = MongoClient("mongodb://localhost:27017/")
db = client.ticketmaster
users_collection = db.users

app.register_blueprint(main)

