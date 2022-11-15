from flask import Flask, Blueprint, request, render_template, redirect, url_for
from control.user import User
from control.group import Group
from view.user import is_cate
from flask_login import current_user, login_required
from view.user import is_cate
import datetime

# group blueprint 생성
group = Blueprint('group', __name__)

@login_required
@group.route('/', methods=['GET'])
def group_page():
    group = Group.getAll()
    cate = is_cate()
    return render_template('group.html', group=group, cate=cate)

@login_required
@group.route('/create', methods=['POST', 'GET'])
def group_create():
    group_name = request.form.get('g_name');
    if not group_name:
        return '<script>alert("그룹명을 입력해주세요");history.go(-1);</script>'
    user = current_user.id
    if Group.create(user, group_name):
        return redirect(url_for('group.group_page'))
    else: '<script>alert("이미 존재하는 그룹명입니다.");history.go(-1);</script>'

@login_required
@group.route('/search', methods=['GET', 'POST'])
def group_search():
    group_name = request.args.get('g_name');
    print(group_name)
    group = Group.search(group_name)
    print(group)
    if group:
        return render_template('group.html', group=group, cate=is_cate())
    else:
        return '<script>alert("존재하지 않는 그룹명입니다.");history.go(-1);</script>'
    
@login_required
@group.route('/register/<string:group_key>', methods=['GET', 'POST'])
def group_registesr(group_key):
    user = current_user.id
    if Group.getCreator(group_key) == user:
        return '<script>alert("당신은 그룹 생성자입니다.");history.go(-1);</script>'
    if Group.register(group_key, user):
        return redirect(url_for('group.group_page'))
    else:
        return '<script>alert("그룹 가입에 실패하셨습니다.");history.go(-1);</script>'
    
@login_required
@group.route('/manage')
def group_manage():
    user = current_user.id
    group = Group.registerList(user)
    return render_template('group_check.html', grouplist=group, cate=is_cate())
