from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from models import User
from db import SessionLocal

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = SessionLocal()
        user_exists = db.query(User).filter_by(email=email).first()
        
        if user_exists:
            flash('Email already exists.', 'danger')
            db.close()
            return redirect(url_for('auth.register'))
        
        hashed_pw = generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password_hash=hashed_pw)
        
        db.add(new_user)
        db.commit()
        db.close()
        
        flash('Account created! Please login.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = SessionLocal()
        user = db.query(User).filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            db.close()
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check email and password.', 'danger')
            db.close()
            return redirect(url_for('auth.login'))
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))