from flask import Flask, Blueprint, request, render_template, redirect, url_for
from control.notice import Notice
from control.user import User
from control.group import Group
from view.user import is_cate
from flask_login import current_user, login_required
from view.user import is_cate, is_group
import datetime

# group blueprint 생성
group = Blueprint('group', __name__)

@login_required
@group.route('/', methods=['GET'])
def group_page():
    group = Group.getAll()
    cate = is_cate()
    return render_template('group.html', group=group, cate=cate, register=is_group())


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
        return render_template('group.html', group=group, cate=is_cate(), register=is_group())
    else:
        return '<script>alert("존재하지 않는 그룹명입니다.");history.go(-1);</script>'
    
@login_required
@group.route('/register/<string:group_key>', methods=['GET', 'POST'])
def group_registesr(group_key):
    user = current_user.id
    if Group.search_key(group_key).master == user:
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
    return render_template('group_check.html', grouplist=group, cate=is_cate(), register=is_group())

@login_required
@group.route('/allow/<string:group>/<string:user>')
def group_allow(group, user):
    register = Group.allow_temp(group, user)
    if register:
        return '<script>window.location=document.referrer</script>'
    else:
        return f"<script>${user}님의 ${group} 가입 승인에 실패하셨습니다.</script>"
    
@login_required
@group.route('/reject/<string:group>/<string:user>')
def group_reject(group, user):
    drop = Group.delete_temp(group, user)
    if drop:
        return '<script>window.location=document.referrer</script>'
    else:
        return f"<script>${user}님의 ${group} 가입 거절에 실패하셨습니다.</script>"
    
@login_required
@group.route('/<string:group>', methods=['GET'])
def group_detail(group):
    group = Group.getGroup(group)
    notice = Notice.getNotice(group[0])
    cate = is_cate()
    return render_template('group_plan.html', group=group, cate=cate, notice=notice, register=is_group())

@login_required
@group.route('/notice/<int:group>', methods=['POST'])
def notice():
    edit = "edit"+str(group)
    content = request.form.get(edit)
    notice = Notice.create(group, content);
    if notice:
        return '<script>window.location=document.referrer</script>'
    else:
        return f"<script>공지 생성에 실패하셨습니다.</script>"
    
@login_required
@group.route('/notice/<int:notice>', methods=['UPDATE'])
def noticeUpdate():
    edit = "edit"+str(notice)
    content = request.form.get(edit)
    notice = Notice.editNotice(notice, content);
    if notice:
        return '<script>window.location=document.referrer</script>'
    else:
        return f"<script>공지 수정에 실패하셨습니다.</script>"
    
@login_required
@group.route('/notice/<int:notice>', methods=['DELETE'])
def noticeDel():
    notice = Notice.delete(notice);
    if notice:
        return '<script>window.location=document.referrer</script>'
    else:
        return f"<script>공지 삭제에 실패하셨습니다.</script>"