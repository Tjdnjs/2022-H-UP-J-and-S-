from flask import flash
from flask_login import UserMixin
from model.mysql import conn_mysql

class Cate():
    def __init__(self, cat_key, user_key, cate):
        self.key = cat_key
        self.user = user_key
        self.name = cate

    @staticmethod
    def get_b_user(user_key):
        mysql_db = conn_mysql()
        db_cursor = mysql_db.cursor()
        sql = "select * from personal_category where user_key = '" + str(user_key) + "'"
        db_cursor.execute(sql)
        print(sql)
        cate = db_cursor.fetchall()
        print(cate)
        if not cate:
            return None
        # cate = Cate(cat_key = cate[0], user = cate[1], name = cate[2])
        return list(cate)
    
    #카테고리 생성
    @staticmethod
    def create(user_key, cate):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM personal_category WHERE cate = '{cate}' and user_key = '{user_key}';"
        cnt = cursor.execute(query)
        if cnt ==0:
            query2 = f"INSERT INTO personal_category VALUES('None','{user_key}', '{cate}');"
            print(query2)
            cnt2 = cursor.execute(query2)    # 쿼리 실행개수 (0:DB오류 / 1:정상)
            conn.commit()
            return True
        else:
            return False


    @staticmethod
    def edit(cate, user_key):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"UPDATE personal_category set cate = '{cate}' WHERE user_key = '{user_key}';"
        cnt = cursor.execute(query)
        conn.commit()
