from flask import Flask, Blueprint, request, render_template, make_response, redirect, url_for, abort, jsonify, flash, get_flashed_messages
from control.user import User
from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash

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

# 로그인 동작
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
    elif not check_password_hash(user.pw, pw):
        return '<script>alert("잘못된 비밀번호입니다");history.go(-1);</script>'
    # elif pw != user.pw:
    #     return '<script>alert("잘못된 비밀번호입니다");history.go(-1);</script>'
    else:
        login_user(user)
        return redirect(url_for('main'))

# 로그아웃 동작
@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('user.user_page'))


# 회원가입 탬플릿 연결
@user.route('/register')
def register():
    # return render_template('sign2.html')
    return render_template('signin.html')

@user.route('/checkDup/<string:user_id>', methods=['POST'])
def check_dup(user_id):
    print('Checking')
    # user_id = request.form.get('user_id')
    exists = bool(User.get(user_id))
    return jsonify({'result': 'success', 'exists': exists})
    
@user.route('/checke/<string:email>', methods=['POST'])
def checke(email):
    print('Checking')
    # user_id = request.form.get('user_id')
    exists = bool(User.get_e(email))
    return jsonify({'result': 'success', 'exists': exists}) 

# 회원가입 동작
@user.route('/registerAction', methods=['POST'])
def registerAction():
    user_id = request.form.get('user_id')
    user_pw = request.form.get('user_pw')
    user_name = request.form.get('user_name')
    user_email = request.form.get('user_email')
    # 암호화
    pw_hash = generate_password_hash(user_pw, 10)
    result = User.create(user_name, user_id, pw_hash,  user_email)
    return redirect(url_for('user.user_page'))
    if not result: 
        # DB 오류 발생
        return '<script>alert("회원가입 오류입니다");history.go(-1);</script>'

# 회원탈퇴
@user.route('/delete')
def delete():
    if current_user.is_authenticated:
        return render_template('delete.html')
    else:
        return redirect(url_for('user.user_page'))
    
# 회원 탈퇴 동작
@user.route('/deleteAction', methods = ['GET','POST'])
def deleteAction():
    if current_user.is_authenticated:
        result = User.delete(current_user.id)
        logout_user()
        if result==1:  # 회원탈퇴 성공
            return redirect(url_for('user.register')) #  회원가입 페이지로
    return '<script>alert("회원탈퇴 오류입니다");history.go(-1);</script>'

# 개인 정보 조회
@user.route('/mypage', methods = ['GET'])
@login_required
def mypage():
    current = User.get(current_user.id)
    user = {"name": current.name, "pw": current.pw, "id":current.id, "email": current.mail}
    return render_template('mypage.html', user = user )

@user.route('/edit', methods = ['POST'])
@login_required
def edit():
    user_pw = request.form.get('user_pw')
    current = User.get(current_user.id)
    pw_hash = generate_password_hash(user_pw, 10)
    current.edit(current_user.id, pw_hash)
    return redirect(url_for('user.mypage'))
    