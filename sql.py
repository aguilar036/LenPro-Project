from linecache import cache

import pymysql

def get_conn():
    return pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='',
        db='test',
    )

def create_tables():
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("CREATE TABLE IF NOT EXISTS agenda(id INT AUTO_INCREMENT PRIMARY KEY, name TEXT, lastname TEXT);")
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()