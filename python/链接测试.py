import psycopg2


if __name__ == '__main__':
    # 如果数据库不存在，那么它将自动创建，最后将返回一个数据库对象
    conn = psycopg2.connect(database="db_port",
                            user="postgres",
                            password="postgres",
                            host="localhost",
                            port="5432")

    print("Opened database successfully")

    cur = conn.cursor()

    cur.execute("SELECT *  from tb_seacrafts")
    rows = cur.fetchall()
    for row in rows:
        print(row)

    conn.close()




