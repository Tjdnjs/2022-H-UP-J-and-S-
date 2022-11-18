from flask import Flask, request, render_template, make_response, redirect, url_for, abort
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
import os
from control.user import User
from control.plan_p import Cate
from view import user, plan_personal, group_view
from view.user import is_cate, is_group

# https 만을 지원하는 기능읗 http에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static') # flask 객체 생성

# blueprint
app.register_blueprint(user.user, url_prefix='/user')
app.register_blueprint(plan_personal.plan_p, url_prefix='/plan')
app.register_blueprint(group_view.group, url_prefix='/group')

CORS(app) # 외부 API 사용하기 위함
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

@app.route('/')
def main():
    if current_user.is_authenticated:
        return render_template('index.html', cate=is_cate(), register=is_group())
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '8000', debug = True)