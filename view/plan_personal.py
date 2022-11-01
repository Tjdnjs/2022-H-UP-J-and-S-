from flask import Flask, Blueprint, request, render_template, redirect, url_for
from control.user import User
from control.plan_p import Cate
from control.plan_content import Personal_plan
from flask_login import current_user
from view.user import is_cate
import datetime

# user blueprint 생성
plan_p = Blueprint('plan', __name__)

@plan_p.route('/create', methods=['POST', 'GET'])
def plan_cate_c():
    cate = request.form.get('cate');
    print(cate)
    user = User.get(current_user.id).key
    if Cate.create(user, cate):
        return redirect(url_for('plan.plan'))
    else: return '<script>alert("이미 존재하는 카테고리명입니다.");history.go(-1);</script>'
    
@plan_p.route('/edit', methods = ['GET'])
def edit():
    cate = is_cate()
    return render_template('category_update.html', cate=cate)

@plan_p.route('/editaction/<int:cate_key>', methods=['POST', 'GET'])
def editaction(cate_key):
    edit = "edit"+str(cate_key)
    new_cate = request.form.get(edit)
    print(new_cate)
    if current_user.key == Cate.get_b_key(cate_key):
        Cate.edit(new_cate, cate_key)
        return redirect(url_for('plan.edit'))
    else:
        return '<script>alert("수정 권한이 없습니다");history.go(-1);</script>'

@plan_p.route('/deleteaction/<int:cate_key>', methods = ['GET','POST'])
def delete(cate_key):
    if current_user.key == Cate.get_b_key(cate_key):
        result = Cate.delete(cate_key)
        if result==1:
            return redirect(url_for('plan.edit'))
        else:return '<script>alert("카테고리 삭제에 실패했습니다");history.go(-1);</script>'
            
    else:
        return '<script>alert("삭제 권한이 없습니다");history.go(-1);</script>'

@plan_p.route('/<string:cate>')
def getcategory(cate):
    return render_template('plan.html', category=cate)

def getplan(cate):
    user = User.get(current_user.id).key
    key = Cate.get_b_cate(user,cate);
    plan = Personal_plan.get_b_key(key);
    if plan != None:
        plan_list = [[li[2], li[3]] for li in plan]
        print(plan_list)
    return plan_list

@plan_p.route('/<string:cate>/make-plan')
def create_plan(cate):
    date = request.args.get('date');
    content = request.args.get('p_content');
    user = User.get(current_user.id).key
    cate_key = Cate.get_b_cate(user, cate)
    print(date, content, cate_key)
    if content:
        Personal_plan.create(cate_key, content, date)
    else:
        return '<script>alert("계획 내용이 작성되지 않았습니다");history.go(-1);</script>'
        
    return render_template('plan.html', category=cate)

@plan_p.route('/<string:cate>/get-plan')
def get_plan(cate):
    plan = getplan(cate)
    date = request.args.get('date');
    date_plan = list(filter(lambda x: str(x[1]) == date, plan))
    return render_template('plan.html', category = cate, plan = date_plan)

@plan_p.route('/<string:cate>/get')
def get_category(cate):
    return render_template('plan.html', category=cate)

@plan_p.route('/')
def plan():
    return redirect(url_for('main'))