class Config:
    SECRET_KEY = 'your_secret_key'
    MONGO_URI = "mongodb://localhost:27017/ticketmaster"
    SESSION_COOKIE_SECURE = True
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    WTF_CSRF_SECRET_KEY = 'root'


