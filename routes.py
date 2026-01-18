import os
import requests
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from models import Item
from db import SessionLocal
from nosql_db import log_activity

items_bp = Blueprint('items', __name__)

@items_bp.route('/items')
@login_required
def list_items():
    db = SessionLocal()
    user_items = db.query(Item).filter_by(user_id=current_user.id).all()
    db.close()
    return render_template('items/list.html', items=user_items)

@items_bp.route('/items/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        # 1. Save to SQL
        db = SessionLocal()
        new_item = Item(title=title, description=description, user_id=current_user.id)
        db.add(new_item)
        db.commit()
        db.close()
        
        # 2. Save to NoSQL (Datastore)
        log_activity(current_user.email, "CREATED_ITEM", title)
        
        # 3. Call Cloud Function for Translation
        try:
            # PASTE YOUR URL HERE
            cf_url = "https://translate-item-9398624084.europe-west2.run.app"
            response = requests.post(cf_url, json={'text': description}, timeout=10)
            if response.status_code == 200:
                translated = response.json().get('translated_text')
                flash(f'Item added! Spanish Translation: {translated}', 'success')
            else:
                flash('Item added (Translation service unavailable)', 'warning')
        except Exception as e:
            print(f"Translation Error: {e}")
            flash('Item added (Translation error)', 'warning')
            
        return redirect(url_for('items.list_items'))
        
    return render_template('items/add.html')

@items_bp.route('/items/delete/<int:item_id>')
@login_required
def delete_item(item_id):
    db = SessionLocal()
    item = db.query(Item).filter_by(id=item_id, user_id=current_user.id).first()
    if item:
        title = item.title
        db.delete(item)
        db.commit()
        log_activity(current_user.email, "DELETED_ITEM", title)
        flash('Item deleted.', 'info')
    db.close()
    return redirect(url_for('items.list_items'))