from flask import Blueprint, render_template, request, flash, jsonify,redirect,send_file,session
from flask_login import login_required, current_user
from .models import User
from . import dbsql
import json
from .models import PostForm,Posts,SearchForm,Messages
import os
import sqlite3
from datetime import datetime
views = Blueprint('views', __name__)



#Daha sonra tarihe göre eklenebilecek son haberler yeri yap!!!!!!!!!!
@views.route('/', methods=['GET', 'POST'])
def home():
    usermessage = Messages()
    posts = Posts.query.order_by(Posts.date_posted)
    posts_for_display = []
    for post in posts:
        if post.id <5:
            posts_for_display.append(post)
        else:
            break
    if request.method == 'POST':
        usermessage.name = request.form.get("name")
        usermessage.email = request.form.get("email")
        usermessage.subject = request.form.get("subject")
        usermessage.message = request.form.get("message")
        usermessage.sender_id = current_user.id
        dbsql.session.add(usermessage)
        dbsql.session.commit()
        flash("Mesaj başarıyla gönderildi")

    return render_template("home.html", user=current_user ,posts = posts_for_display)
