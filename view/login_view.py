from flask import Flask, request, render_template, Blueprint
from control.user import User
# from app import app
from flask_login import login_user, logout_user

login = Blueprint('login', __name__)

@login.route('/login', methods = ['get','post'])
def login():
    id = request.form.get('id')
    pw = request.form.get('pw')

    user = User.get(id)

    if not user:
        return '<script>alert("not found user");history.go(-1);</script>'
    elif pw != user.pw:
        return '<script>alert("passwork error");history.go(-1);</script>'
    else:
        return '<script>alert("logined");</script>'