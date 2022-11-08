from flask import Flask, Blueprint, request, render_template, redirect, url_for
from control.user import User
from control.group import Group
from flask_login import current_user
from view.user import is_cate
import datetime

# group blueprint 생성
group = Blueprint('group', __name__)

@group.route('/create', methods=['POST', 'GET'])
def group_create():
    group_name = request.form.get('g_name');
    user = User.get(current_user.id).key
    if Group.create(user, group_name):
        return 
    else: '<script>alert("이미 존재하는 그룹명입니다.");history.go(-1);</script>'
    
@group.route('/search', methods=['GET', 'POST'])
def group_search():
    group_name = request.form.get('g_name');
    group = Group.search(group_name)
    if group:
        return group
    else:
        return 