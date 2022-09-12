from flask_login import UserMixin
from model.mysql import conn_mysql

class User(UserMixin):

    # User 객체에 저장할 사용자 정보
    def __init__(self, user_id, user_pw):
        self.id = user_id
        self.pw = user_pw
    
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
        user = User(user_id = user[0], user_pw = user[1])
        return user