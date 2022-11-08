from datetime import datetime
from model.mysql import conn_mysql

class Group():
    def __init__(self, group_key,group_name, group_master, created_date):
        self.key = group_key
        self.name = group_name
        self.master = group_master
        self.date = created_date
        
    @staticmethod
    def create(user_key, name):
        # mysql DB 연결
        conn = conn_mysql()
        date = datetime.today().strftime('%Y-%m-%d')
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM group_category WHERE group_name = '{name}';"
        cnt = cursor.execute(query)
        if cnt ==0:
            query2 = f"INSERT INTO group_category VALUES('None','{name}', '{user_key}','{date}');"
            print(query2)
            cnt2 = cursor.execute(query2)    # 쿼리 실행개수 (0:DB오류 / 1:정상)
            conn.commit()
            return True
        else:
            return False
    
    @staticmethod
    def search(name):
        conn = conn_mysql()
        date = datetime.today().strftime('%Y-%m-%d')
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM group_category WHERE group_name = '{name}';"
        cnt = cursor.execute(query)
        if cnt ==0:
            group = cursor.fetchall()
            return group
        else:
            return False
    