# ------*------ coding: utf-8 ------*------
# @Time    : 2022/4/28 14:22
# @Author  : 冰糖雪狸 (NekoSilverfox)
# @Project : JSON 速度测试
# @File    : 速度测试.py
# @Software: PyCharm
# @Github  ：https://github.com/NekoSilverFox
# -----------------------------------------
import psycopg2 as pg
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import pickle


if __name__ == '__main__':
    # 如果数据库不存在，那么它将自动创建，最后将返回一个数据库对象
    print('>>' * 50)
    print('[INFO] Start connect database')
    conn = pg.connect(database="db_imdb",
                      user="postgres",
                      password="postgres",
                      host="localhost",
                      port="5432")
    cur = conn.cursor()
    print('[INFO] Connect database successfully')

    # 获取行数
    cur.execute("SELECT COUNT(*) FROM tb_jsonb;")
    count_row = cur.fetchall()[0][0]
    print('行数：', count_row)

    # 用于统计的 DataFrame
    df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])

    # 执行查询并记录时间
    for i in range(1, 100):
        print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row, 4)) + '%')
        comm_sql = 'SELECT imdata FROM tb_json WHERE iddata=' + str(i) + ';'

        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        use_time_ms = (end_time - start_time).microseconds
        # print('用时：', (end_time - start_time).microseconds, 'ms')

        rows = cur.fetchall()
        len_row_json = len(str(rows))  # JSON(B)长度

        df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/json/res_id.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['use_time_ms'].values)
    plt.title('Query by key `ID` in tb_json')
    plt.xlabel('Length of JSON')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/json/res_id.png')
    plt.show()

    # print(rows)
    # print(len_row)

    # for row in rows:
    #     print(row)

    conn.close()
