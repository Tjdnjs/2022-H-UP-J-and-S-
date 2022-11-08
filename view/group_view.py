from flask import Flask, Blueprint, request, render_template, redirect, url_for
from control.user import User
from control.group import Group
from flask_login import current_user, login_required
from view.user import is_cate
import datetime

# group blueprint 생성
group = Blueprint('group', __name__)

@login_required
@group.route('/', methods=['GET'])
def group_page():
    group = Group.getAll()
    return render_template('group.html', group=group)

@login_required
@group.route('/create', methods=['POST', 'GET'])
def group_create():
    group_name = request.form.get('g_name');
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
        return render_template('group.html', group=group)
    else:
        return '<script>alert("존재하지 않는 그룹명입니다.");history.go(-1);</script>'