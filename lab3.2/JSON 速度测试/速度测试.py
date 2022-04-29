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


def json_id_test():
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
    cur.execute("SELECT COUNT(*) FROM tb_json;")
    count_row = cur.fetchall()[0][0]
    print('行数：', count_row)

    # 用于统计的 DataFrame
    df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])

    # 执行查询并记录时间
    for i in range(1, 3000):
        print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')
        comm_sql = 'SELECT imdata FROM tb_json WHERE iddata=' + str(i) + ';'

        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        use_time_ms = (end_time - start_time).microseconds
        # print('用时：', (end_time - start_time).microseconds, 'ms')

        row = cur.fetchall()[0]
        len_row_json = len(str(row))  # JSON(B)长度

        df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
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
    # plt.show()


def jsonb_id_test():
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
    for i in range(1, 3000):
        print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')
        comm_sql = 'SELECT imdata FROM tb_jsonb WHERE iddata=' + str(i) + ';'

        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        use_time_ms = (end_time - start_time).microseconds
        # print('用时：', (end_time - start_time).microseconds, 'ms')

        row = cur.fetchall()[0]
        len_row_json = len(str(row))  # JSON(B)长度

        df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/jsonb/res_id.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['use_time_ms'].values)
    plt.title('Query by key `ID` in tb_jsonb')
    plt.xlabel('Length of JSONB')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/jsonb/res_id.png')
    # plt.show()


def json_where_name_test():
    print('>>' * 50)
    print('[INFO] 读取序列化数据')
    time_start = datetime.datetime.now()
    f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
             'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
    arr_name = pickle.load(file=f)
    f.close()
    arr_name = arr_name['name'].values
    time_end = datetime.datetime.now()
    print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    print('>>' * 50)
    print('[INFO] Start connect database')
    conn = pg.connect(database="db_imdb",
                      user="postgres",
                      password="postgres",
                      host="localhost",
                      port="5432")
    cur = conn.cursor()
    print('[INFO] Connect database successfully')

    i = 0
    count_row = len(arr_name)
    # 用于统计的 DataFrame
    df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
    # TODO 取消分割
    for name in arr_name[244:250]:
        i += 1
        print('[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | name = ', name)

        comm_sql = "SELECT imdata FROM tb_json WHERE imdata::json->> 'name' = '" + name + "';"
        start_time = datetime.datetime.now()
        try:
            cur.execute(comm_sql)
        except:
            print('[INFO] 第 ' + str(i) + ' 行取消 | name = ', name)
            continue
        end_time = datetime.datetime.now()
        use_time_ms = (end_time - start_time).microseconds
        # print('用时：', (end_time - start_time).microseconds, 'ms')

        row = cur.fetchall()[0]
        len_row_json = len(str(row))  # JSON(B)长度
        df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/json/res_name.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['use_time_ms'].values)
    plt.title('Query by key `name` in tb_json')
    plt.xlabel('Length of JSON')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/json/res_name.png')
    # plt.show()  # TODO 注释掉


def jsonb_where_name_test():
    print('>>' * 50)
    print('[INFO] 读取序列化数据')
    time_start = datetime.datetime.now()
    f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
             'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
    arr_name = pickle.load(file=f)
    f.close()
    arr_name = arr_name['name'].values
    time_end = datetime.datetime.now()
    print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    print('>>' * 50)
    print('[INFO] Start connect database')
    conn = pg.connect(database="db_imdb",
                      user="postgres",
                      password="postgres",
                      host="localhost",
                      port="5432")
    cur = conn.cursor()
    print('[INFO] Connect database successfully')

    i = 0
    count_row = len(arr_name)
    # 用于统计的 DataFrame
    df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
    # TODO 取消分割
    for name in arr_name[:3000]:
        i += 1
        print('[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | name = ', name)

        comm_sql = "SELECT imdata FROM tb_jsonb WHERE imdata::jsonb->> 'name' = '" + name + "';"
        start_time = datetime.datetime.now()
        try:
            cur.execute(comm_sql)
        except:
            print('[INFO] 第 ' + str(i) + ' 行取消 | name = ', name)
            continue
        end_time = datetime.datetime.now()
        use_time_ms = (end_time - start_time).microseconds
        # print('用时：', (end_time - start_time).microseconds, 'ms')

        row = cur.fetchall()[0]
        len_row_json = len(str(row))  # JSON(B)长度
        df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

        # print(rows)  # TODO 注释掉
        # print(len(str(rows)))  # TODO 注释掉

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/jsonb/res_name.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['use_time_ms'].values)
    plt.title('Query by key `name` in tb_jsonb')
    plt.xlabel('Length of JSONB')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/jsonb/res_name.png')
    # plt.show()  # TODO 注释掉


def json_where_nconst_test():
    print('>>' * 50)
    print('[INFO] 读取序列化数据')
    time_start = datetime.datetime.now()
    f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
             'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
    arr_nconst = pickle.load(file=f)
    f.close()
    arr_nconst = arr_nconst['nconst'].values
    time_end = datetime.datetime.now()
    print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    print('>>' * 50)
    print('[INFO] Start connect database')
    conn = pg.connect(database="db_imdb",
                      user="postgres",
                      password="postgres",
                      host="localhost",
                      port="5432")
    cur = conn.cursor()
    print('[INFO] Connect database successfully')

    i = 0
    count_row = len(arr_nconst)
    # 用于统计的 DataFrame
    df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
    # TODO 取消分割
    for nconst in arr_nconst[:10]:
        i += 1
        print('[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | nconst = ', nconst)

        comm_sql = "SELECT imdata FROM tb_json WHERE imdata::json->> 'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        try:
            cur.execute(comm_sql)
        except:
            print('[INFO] 第 ' + str(i) + ' 行取消 | nconst = ', nconst)
            continue
        end_time = datetime.datetime.now()
        use_time_ms = (end_time - start_time).microseconds
        print('\t用时：', (end_time - start_time).seconds, 's')

        row = cur.fetchall()[0]
        len_row_json = len(str(row))  # JSON(B)长度
        df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/json/res_nconst.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['use_time_ms'].values)
    plt.title('Query by key `nconst` in tb_json')
    plt.xlabel('Length of JSON')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/json/res_nconst.png')
    # plt.show()  # TODO 注释掉


def jsonb_where_nconst_test():
    print('>>' * 50)
    print('[INFO] 读取序列化数据')
    time_start = datetime.datetime.now()
    f = open('/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
             'курс/6 семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits', 'rb')
    arr_nconst = pickle.load(file=f)
    f.close()
    arr_nconst = arr_nconst['nconst'].values
    time_end = datetime.datetime.now()
    print('[INFO] 读取序列化数据结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    print('>>' * 50)
    print('[INFO] Start connect database')
    conn = pg.connect(database="db_imdb",
                      user="postgres",
                      password="postgres",
                      host="localhost",
                      port="5432")
    cur = conn.cursor()
    print('[INFO] Connect database successfully')

    i = 0
    count_row = len(arr_nconst)
    # 用于统计的 DataFrame
    df_counter = pd.DataFrame([[0, 0]], columns=['len_row', 'use_time_ms'])
    # TODO 取消分割
    for nconst in arr_nconst[:10]:
        i += 1
        print('[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | nconst = ', nconst)

        comm_sql = "SELECT imdata FROM tb_jsonb WHERE imdata::jsonb->> 'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        try:
            cur.execute(comm_sql)
        except:
            print('[INFO] 第 ' + str(i) + ' 行取消 | nconst = ', nconst)
            continue
        end_time = datetime.datetime.now()
        use_time_ms = (end_time - start_time).microseconds
        print('\t用时：', (end_time - start_time).seconds, 's')

        row = cur.fetchall()[0]
        len_row_json = len(str(row))  # JSON(B)长度
        df_tmp = pd.DataFrame([[len_row_json, use_time_ms]], columns=['len_row', 'use_time_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/jsonb/res_nconst.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['use_time_ms'].values)
    plt.title('Query by key `nconst` in tb_jsonb')
    plt.xlabel('Length of JSONB')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/jsonb/res_nconst.png')
    # plt.show()  # TODO 注释掉


if __name__ == '__main__':
    # json_id_test()

    # jsonb_id_test()

    # json_where_name_test()

    # jsonb_name_test()

    json_where_nconst_test()

    jsonb_where_nconst_test()



