from flask_login import UserMixin
from model.mysql import conn_mysql

class User(UserMixin):

    # User 객체에 저장할 사용자 정보
    def __init__(self, user_name, user_id, user_pw, user_email):
        self.name = user_name
        self.id = user_id
        self.pw = user_pw
        self.mail = user_email
    
    def get_id(self):
        return str(self.id)

    @staticmethod
    def get(user_id):
        mysql_db = conn_mysql()
        db_cursor = mysql_db.cursor()
        sql = "select * from user_info where user_id = '" + str(user_id) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        user = User(user_name = user[0], user_id = user[1], user_pw = user[2], user_email=user[3])
        return user
    
    @staticmethod
    def get_e(user_email):
        mysql_db = conn_mysql()
        db_cursor = mysql_db.cursor()
        sql = "select * from user_info where user_email = '" + str(user_email) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        user = User(user_name = user[0], user_id = user[1], user_pw = user[2], user_email=user[3])
        return user
    
    # 회원가입
    @staticmethod
    def create(user_name : str, user_id : str, user_pw, user_email : str):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        # 이미 존재하는 아이디인지 조회
        query = f"SELECT * FROM user_info WHERE user_id = '{user_id}';"
        cnt = cursor.execute(query)
        if cnt == 0:    # 없는 아이디
            query2 = f"INSERT INTO user_info VALUES('{user_name}', '{user_id}', '{user_pw}', '{user_email}');"
            print(query2)
            cnt2 = cursor.execute(query2)    # 쿼리 실행개수 (0:DB오류 / 1:정상)
            conn.commit()
            return True
        else:
            return False


    # 회원탈퇴
    @staticmethod
    def delete(user_id : str):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        # 이미 존재하는 아이디인지 조회
        query = f"SELECT * FROM user_info WHERE user_id = '{user_id}';"
        cnt = cursor.execute(query)
        if cnt==1:    # 존재하는 아이디
            query2 = f"DELETE FROM user_info WHERE user_id = '{user_id}';"
            cnt2 = cursor.execute(query2)    # 0:DB오류 / 1:정상
            conn.commit()
            return cnt2
        else:       # 오류
            return 0
        
    # 회원 정보 수정
    @staticmethod
    def edit(user_id : str, user_pw : str):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"UPDATE user_info set user_pw = '{user_pw}' WHERE user_id = '{user_id}';"
        cnt = cursor.execute(query)
        conn.commit()

