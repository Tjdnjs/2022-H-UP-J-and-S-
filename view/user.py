from flask import Flask, Blueprint, request, render_template, make_response, redirect, url_for, abort
from control.user import User
# from model import User
# from pybo import db
from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user, current_user, login_required

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
        return '<script>alert("존재하지 않는 아이디입니다");history.go(-1);</script>'
    elif pw != user.pw:
        return '<script>alert("잘못된 비밀번호입니다");history.go(-1);</script>'
    else:
        login_user(user)
        return redirect(url_for('main'))

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.user_page'))

###

@user.route('/register')
def register():
    return render_template('signin.html')


@user.route('/registerAction', methods=['POST'])
def registerAction():
    user_id = request.form.get('user_id')
    user_pw = request.form.get('user_pw')
    user_name = request.form.get('user_name')
    user_email = request.form.get('user_email')
    if User.get(user_id):
        return '<script>alert("이미 존재하는 ID 입니다");history.go(-1);</script>'
    else:
        result = User.create(user_name, user_id, user_pw,  user_email)
        return redirect(url_for('user.user_page'))
    if not result: 
        return '<script>alert("회원가입 오류입니다");history.go(-1);</script>'

# 회원탈퇴
@user.route('/delete')
def delete():
    if current_user.is_authenticated:
        return render_template('delete.html')
    else:
        return redirect(url_for('user.user_page'))
    

@user.route('/deleteAction', methods = ['GET','POST'])
def deleteAction():
    if current_user.is_authenticated:
        result = User.delete(current_user.id)
        logout_user()
        if result==1:  # 회원탈퇴 성공
            return redirect(url_for('user.register')) #  회원가입 페이지로
    return "<h1> 오류 </h1>"

@user.route('/mypage', methods = ['GET'])
@login_required
def mypage():
    current = User.get(current_user.id)
    return render_template('mypage.html', name=current.name, pw=current.pw,id=current.id,email=current.mail )