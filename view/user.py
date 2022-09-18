from flask import Flask, Blueprint, request, render_template, make_response, redirect, url_for, abort
from control.user import User
# from model import User
# from pybo import db
from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user, current_user

# user blueprint 생성
user = Blueprint('user', __name__)

# next 파라미터 유효성 검사 - open redirect 취약 방지하기 위함
def is_safe_url(target):
    print('secure on')
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@user.route('/')
def user_page():
    return render_template('login.html')

@user.route('/login', methods = ['get','post'])
def login():
    id = request.form.get('id')
    pw = request.form.get('pw')

    user = User.get(id)
    next = request.args.get('next')
    print(next)
    if not is_safe_url(next):
        return abort(400)

    if not user:
        return '<script>alert("not found user");history.go(-1);</script>'
    elif pw != user.pw:
        return '<script>alert("passwork error");history.go(-1);</script>'
    else:
        login_user(user)
        return redirect(url_for('user.user_page'))

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))