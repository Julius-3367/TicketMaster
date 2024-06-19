from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from pymongo import MongoClient
from TicketMaster.App.routes import main
from TicketMaster.App.config import Config

app = Flask(__name__)
app.config.from_object(Config)

csrf = CSRFProtect(app)
Session(app)

client = MongoClient(app.config["MONGO_URI"])
db = client.ticketmaster
users_collection = db.users

app.register_blueprint(main)

