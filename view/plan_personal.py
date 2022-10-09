from flask import Flask, Blueprint, request, render_template, make_response, redirect, url_for, abort, jsonify, flash, get_flashed_messages
from control.user import User
from control.plan_p import Cate
from urllib.parse import urlparse, urljoin
from flask_login import login_user, logout_user, current_user, login_required
import bcrypt
from view.user import is_cate

# user blueprint 생성
plan_p = Blueprint('plan', __name__)

@plan_p.route('/create', methods=['POST', 'GET'])
def plan_cate_c():
    cate = request.form.get('cate');
    user = User.get(current_user.id).key
    print(cate)
    if Cate.create(user, cate):
        return redirect(url_for('plan.plan'))
    else: return '<script>alert("이미 존재하는 카테고리명입니다.");history.go(-1);</script>'
    
@plan_p.route('/edit')
def edit():
    cate = is_cate()
    return render_template('plan_update.html', cate=cate)

@plan_p.route('/')
def plan():
    return redirect(url_for('main'))