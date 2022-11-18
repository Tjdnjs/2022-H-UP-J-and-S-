from datetime import datetime
from model.mysql import conn_mysql

class Group():
    def __init__(self, group_key,group_name, group_master, created_date):
        self.key = group_key
        self.name = group_name
        self.master = group_master
        self.date = created_date
        
    @staticmethod
    def create(user_id, name):
        # mysql DB 연결
        conn = conn_mysql()
        date = datetime.today().strftime('%Y-%m-%d')
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM group_category WHERE group_name = '{name}';"
        cnt = cursor.execute(query)
        if cnt ==0:
            query2 = f"INSERT INTO group_category VALUES('None','{name}', '{user_id}','{date}');"
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
        if cnt !=0:
            group = cursor.fetchall()
            return group
        else:
            return False

    @staticmethod
    def getAll():
        print("get all group")
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM group_category;"
        cnt = cursor.execute(query)
        if cnt !=0:
            group = cursor.fetchall()
            return group
        else:
            return False
        
    @staticmethod
    def getCreator(group):
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM group_category WHERE group_name = '{group}';"
        cnt = cursor.execute(query)
        if cnt !=0:
            group = cursor.fetchall()
            return group[0][2]
        else:
            return False
        
    @staticmethod
    def register(group, user):
        # mysql DB 연결
        conn = conn_mysql()
        master = Group.getCreator(group)
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM temp_register WHERE group_name = '{group}' and user_name = '{user}';"
        cnt = cursor.execute(query)
        if cnt ==0:
            query2 = f"INSERT INTO temp_register VALUES('None', '{master}', '{user}','{group}');"
            print(query2)
            cnt2 = cursor.execute(query2)    # 쿼리 실행개수 (0:DB오류 / 1:정상)
            conn.commit()
            return True
        else:
            return False
        
    @staticmethod
    def registerList(master):
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM temp_register WHERE group_master = '{master}';"
        cnt = cursor.execute(query)
        if cnt !=0:
            group = cursor.fetchall()
            return group
        else:
            return False
        
    @staticmethod
    def allow_temp(group, user):
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query1 = f"DELETE FROM temp_register WHERE group_name = '{group}' and user_name = '{user}';"
        print(query1)
        cnt1 = cursor.execute(query1);
        if cnt1 !=0:
            query2 = f"INSERT INTO register VALUES('{group}','{user}');"
            print(query2)
            cnt2 = cursor.execute(query2)
            conn.commit()
            return True
        else:
            return False
    @staticmethod
    def delete_temp(group, user):
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query1 = f"DELETE FROM temp_register WHERE group_name = '{group}' and user_name = '{user}';"
        cnt1 = cursor.execute(query1)
        if cnt1 !=0:
            return True
        else:
            return False
        
    @staticmethod
    def find_register(user):
        conn = conn_mysql()
        cursor = conn.cursor()
        query = f"SELECT * FROM register WHERE user_name = '{user}';"
        cnt = cursor.execute(query)
        if cnt !=0:
            group = cursor.fetchall()
            print("registered : ", group)
            return group
        else:
            return False