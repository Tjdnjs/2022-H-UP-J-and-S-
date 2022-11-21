from flask import flash
from model.mysql import conn_mysql

class Personal_plan():
    def __init__(self, plan_key,cat_key, content, date):
        self.key = plan_key
        self.cate = cat_key
        self.content = content
        self.date = date
    
    def get_b_date(date):
        mysql_db = conn_mysql()
        db_cursor = mysql_db.cursor()
        sql = "select * from personal_plan where date = '" + date + "'"
        db_cursor.execute(sql)
        print(sql)
        plan = db_cursor.fetchall()
        print(plan)
        if not plan:
            return None
        return plan
    
    @staticmethod
    def get_b_catkey(cat_key):
        mysql_db = conn_mysql()
        db_cursor = mysql_db.cursor()
        sql = "select * from personal_plan where cat_key = '" + str(cat_key) + "'"
        db_cursor.execute(sql)
        plan = db_cursor.fetchall()
        if not plan:
            return None
        return plan
    
    @staticmethod
    def get_b_key(pp_key):
        mysql_db = conn_mysql()
        db_cursor = mysql_db.cursor()
        sql = "select * from personal_plan where pp_key = '" + str(pp_key) + "'"
        db_cursor.execute(sql)
        print(sql)
        plan = db_cursor.fetchall()
        print(plan)
        if not plan:
            return None
        return plan
    
    #카테고리 생성
    @staticmethod
    def create(cate, content, date):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query2 = f"INSERT INTO personal_plan VALUES('None','{cate}', '{content}','{date}');"
        print(query2)
        cnt2 = cursor.execute(query2)    # 쿼리 실행개수 (0:DB오류 / 1:정상)
        conn.commit()

    @staticmethod
    def edit(plan_key, content):
        print("plan edit")
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"UPDATE personal_plan set content = '{content}' WHERE pp_key = '{plan_key}';"
        cnt = cursor.execute(query)
        conn.commit()
        
    @staticmethod
    def delete(plan_key):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM personal_plan WHERE pp_key = '{plan_key}';"
        cnt = cursor.execute(query)
        if cnt==1:
            query2 = f"DELETE FROM personal_plan WHERE pp_key = '{plan_key}';"
            cnt2 = cursor.execute(query2)    # 0:DB오류 / 1:정상
            conn.commit()
            return cnt2
        else:       # 오류
            return 0
        
    @staticmethod
    def plan_toggle(plan_key):
        print("plan toggle")
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM personal_plan WHERE pp_key = '{plan_key}' LIMIT 1;"
        cnt = cursor.execute(query)
        if cnt == 1:
            plan = cursor.fetchall();
            print("toggle : ", plan)
            if plan[0][-1] == 0:
                query = f"UPDATE personal_plan set checked = 1 WHERE pp_key = '{plan_key}';"
                cursor.execute(query)
            elif plan[0][-1] == 1:
                query = f"UPDATE personal_plan set checked = 0 WHERE pp_key = '{plan_key}';"
                cursor.execute(query)
            conn.commit()
        else: return 0