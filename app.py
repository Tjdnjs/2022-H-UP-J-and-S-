from flask import Flask, request, render_template, make_response, redirect, url_for, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from urllib.parse import urlparse, urljoin
import os
from control.user import User
# from view import login_view

# https 만을 지원하는 기능읗 http에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static') # flask 객체 생성
CORS(app)
app.secret_key = os.urandom(24) # 보안을 위해 서버가 생성될 때마다 시크릿키 새로 발급

login_manager = LoginManager() # 로그인 객체 생성
login_manager.init_app(app) # app에 login_manager 연결
login_manager.session_protection = 'strong' # session 보안성 강화

# User class 를 통해 사용자 정보를 가져옴
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# login_required 데코레이터로 로그인 후 접근 가능한 페이지 보호
@login_manager.unauthorized_handler
def unauthorized():
    return '<script>alert("not found user");history.go(-1);</script>'

# next 파라미터 유효성 검사 - open redirect 취약 방지하기 위함
def is_safe_url(target):
    print('secure on')
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/login', methods = ['get','post'])
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
        return redirect(url_for('main'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '8080', debug = True)