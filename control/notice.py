from model.mysql import conn_mysql

class Notice():
    def __init__(self, group, content):
        self.group = group
        self.content = content
        
    @staticmethod
    def create(group, content):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"INSERT INTO group_notice VALUES('None','{group}', '{content}', 'None');"
        print(query)
        if cursor.execute(query):    # 쿼리 실행개수 (0:DB오류 / 1:정상)
            conn.commit()
            return True
        else: return False
        
    # GET Group
    @staticmethod
    def getNotice(group):
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"select * from group_notice where group_key = '{group}'"
        print(query)
        cnt = cursor.execute(query)
        if cnt !=0:
            group = cursor.fetchall()
            return group
        else:
            return False
        
    @staticmethod
    def editNotice(noticeId, content):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"UPDATE group_notice set content = '{content}' WHERE noticeId = '{noticeId}';"
        cnt = cursor.execute(query)
        conn.commit()
        query = f"SELECT * FROM group_notice WHERE noticeId = '{noticeId}'";
        cursor.execute(query)
        notice = cursor.fetchone()
        return notice
        
    @staticmethod
    def delete(noticeId):
        # mysql DB 연결
        conn = conn_mysql()
        # 커서
        cursor = conn.cursor()
        query = f"SELECT * FROM group_notice WHERE noticeId = '{noticeId}';"
        cnt = cursor.execute(query)
        if cnt==1:
            query2 = f"DELETE FROM group_notice WHERE noticeId = '{noticeId}';"
            cnt2 = cursor.execute(query2)    # 0:DB오류 / 1:정상
            conn.commit()
            return cnt2
        else:       # 오류
            return 0