import os
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from db import SessionLocal
from models import User
from auth import auth_bp
from routes import items_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_key_123")

# Disable template caching (for development only)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initialize Security Tools
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# This tells Flask-Login how to find a user in your Cloud SQL DB
@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    user = db.query(User).get(int(user_id))
    db.close()
    return user

# Register the Authentication routes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(items_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)