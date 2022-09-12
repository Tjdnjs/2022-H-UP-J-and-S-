# flask_login에서 제공하는 사용자 클래스 객체
import pymysql

HOST = 'localhost'
connect = pymysql.connect(
    host = HOST,
    port = 3306,
    user = 'root',
    db = 'user_login',
    passwd = 'qkrtjdnjsdb1!',
    charset = 'utf8'
)

# db 연결이 끊겼을 때 재연결
def conn_mysql():
    if not connect.open:
        connect.ping(reconnect = True)
    return connect


    