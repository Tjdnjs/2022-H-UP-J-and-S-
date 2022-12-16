from flask import Blueprint, request, render_template, redirect, url_for
from control.user import User
from control.plan_p import Cate
from control.plan_content import Personal_plan
from flask_login import current_user
from view.user import is_cate, is_group

# plan blueprint 생성
plan_p = Blueprint('plan', __name__)

# 카테고리 생성
@plan_p.route('/create', methods=['POST', 'GET'])
def plan_cate_c():
    cate = request.form.get('cate');
    print(cate)
    user = User.get(current_user.id).key
    if Cate.create(user, cate):
        return redirect(url_for('plan.plan'))
    else: return '<script>alert("이미 존재하는 카테고리명입니다.");history.go(-1);</script>'

# 카테고리 수정
@plan_p.route('/edit', methods = ['GET'])
def edit():
    cate = is_cate()
    return render_template('category_update.html', cate=cate, register=is_group())

@plan_p.route('/editaction/<int:cate_key>', methods=['POST', 'GET'])
def editaction(cate_key):
    edit = "edit"+str(cate_key)
    new_cate = request.form.get(edit)
    print(new_cate)
    if current_user.key == Cate.getCreator(cate_key):
        Cate.edit(new_cate, cate_key)
        return redirect(url_for('plan.edit'))
    else:
        return '<script>alert("수정 권한이 없습니다");history.go(-1);</script>'

# 카테고리 삭제
@plan_p.route('/deleteaction/<int:cate_key>', methods = ['GET','POST'])
def delete(cate_key):
    if current_user.key == Cate.getCreator(cate_key):
        result = Cate.delete(cate_key)
        if result==1:
            return redirect(url_for('plan.edit'))
        else:return '<script>alert("카테고리 삭제에 실패했습니다");history.go(-1);</script>'
            
    else:
        return '<script>alert("삭제 권한이 없습니다");history.go(-1);</script>'

# 카테고리 내 조회
@plan_p.route('/<string:thiscate>')
def getcategory(thiscate):
    cate = is_cate()
    return render_template('plan.html', category=thiscate, cate=cate, register=is_group())

# 계획 생성
@plan_p.route('/<string:cate>/make-plan')
def create_plan(cate):
    date = request.args.get('date2');
    print("date", date);
    if not date: 
        return '<script>alert("날짜 선택을 다시 해주세요");history.go(-1);</script>'
    
    content = request.args.get('p_content');
    user = User.get(current_user.id).key
    cate_key = Cate.get_b_cate(user, cate)
    print(date, content, cate_key)
    if content:
        Personal_plan.create(cate_key, content, date)
    else:
        return '<script>alert("계획 내용이 작성되지 않았습니다");history.go(-1);</script>'
        
    return '<script>window.location=document.referrer</script>'

def getplan(cate):
    user = User.get(current_user.id).key
    key = Cate.get_b_cate(user,cate);
    plan = Personal_plan.get_b_catkey(key);
    if plan != None:
        plan_list = [[li[0], li[2], li[3], li[4]] for li in plan]
        print(plan_list)
    return plan_list

# 계획 조회
@plan_p.route('/<string:thiscate>/get-plan')
def get_plan(thiscate):
    cate = is_cate()
    plan = getplan(thiscate)
    date = request.args.get('date');
    date_plan = list(filter(lambda x: str(x[2]) == date and x[-1] == True, plan))
    date_plan_not = list(filter(lambda x: str(x[2]) == date and x[-1] == False, plan))
    return render_template('plan.html', category = thiscate, cate=cate, plan = date_plan, plan_left=date_plan_not, date=date, register=is_group())

# 계획 수정
@plan_p.route('/editplan/<int:pp_key>', methods=['POST', 'GET'])
def editplan(pp_key):
    edit = "editplan"+str(pp_key)
    new_plan = request.form.get(edit)
    plan = Personal_plan.get_b_key(pp_key)
    print(new_plan)
    # date = str(plan[0][3]); cate = Cate.get_b_key(plan[0][1])[0];
    if current_user.key == plan[1]:
        Personal_plan.edit(pp_key,new_plan)
        return '<script>window.location=document.referrer</script>'
    else:
        return '<script>alert("수정 권한이 없습니다");history.go(-1);</script>'

# 계획 삭제
@plan_p.route('/deleteplan/<int:pp_key>', methods = ['GET','POST'])
def deleteplan(pp_key):
    plan = Personal_plan.get_b_key(pp_key)
    # date = str(plan[0][3]); cate = Cate.get_b_key(plan[0][1])[0];
    if current_user.key == plan[1]:
        result = Personal_plan.delete(pp_key)
        if result==1:
            return '<script>window.location=document.referrer</script>'
        else:return '<script>alert("카테고리 삭제에 실패했습니다");history.go(-1);</script>'
            
    else:
        return '<script>alert("삭제 권한이 없습니다");history.go(-1);</script>'

@plan_p.route('/toggle/<int:pp_key>')
def toggleplan(pp_key):
    plan = Personal_plan.get_b_key(pp_key)
    Personal_plan.plan_toggle(pp_key)
    return '<script>window.location=document.referrer</script>'
    
@plan_p.route('/')
def plan():
    return redirect(url_for('main'))