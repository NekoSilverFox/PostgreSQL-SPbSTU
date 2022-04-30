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


def get_id_len_json_df():
    """
    获取数据库中每个 ID 对应 JSON data 的长度
    :return:
    """
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
    df_counter = pd.DataFrame([[0, 0]], columns=['id', 'len_json'])

    # 执行查询并记录时间
    for i in range(1, count_row):
        print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')

        comm_sql = 'SELECT imdata FROM tb_json WHERE iddata=' + str(i) + ';'
        cur.execute(comm_sql)
        len_row_json = len(str(cur.fetchall()[0]))  # JSON(B)长度

        df_tmp = pd.DataFrame([[i, len_row_json]], columns=['id', 'len_json'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_json', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/df_id_json_len.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')


def json_by_id_only_full_row_test():
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


def jsonb_by_id_only_full_row_test():
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


def json_by_id_every_col_test():
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
    df_counter = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]],
                              columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])

    # 执行查询并记录时间
    for i in range(1, count_row):
        print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')

        # 整个 data 行所有字段
        comm_sql = 'SELECT imdata FROM tb_json WHERE iddata=' + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        full_use_time_ms = (end_time - start_time).microseconds
        row = cur.fetchall()[0]
        len_row_json = len(str(row))  # JSON(B)长度

        # 整个 data 行的字段 nconst
        comm_sql = "SELECT imdata->>'nconst' FROM tb_json WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        nconst_use_time_ms = (end_time - start_time).microseconds

        # 整个 data 行的字段 name
        comm_sql = "SELECT imdata->>'name' FROM tb_json WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        name_use_time_ms = (end_time - start_time).microseconds

        # 整个 data 行的字段 birthYear
        comm_sql = "SELECT imdata->>'birthYear' FROM tb_json WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        birthYear_use_time_ms = (end_time - start_time).microseconds

        # 整个 data 行的字段 profession
        comm_sql = "SELECT imdata->>'profession' FROM tb_json WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        profession_use_time_ms = (end_time - start_time).microseconds

        # 整个 data 行的字段 rols
        comm_sql = "SELECT imdata->>'rols' FROM tb_json WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        rols_use_time_ms = (end_time - start_time).microseconds

        df_tmp = pd.DataFrame([[len_row_json, full_use_time_ms, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, profession_use_time_ms, rols_use_time_ms]],
                              columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/json/res_id_ix_every_col.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['full_ms'].values,
                label='full row')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['nconst_ms'].values,
                label='nconst')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['name_ms'].values,
                label='name')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['birthYear_ms'].values,
                label='birthYear')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['profession_ms'].values,
                label='profession')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['rols_ms'].values,
                label='rols')
    plt.legend()
    plt.title('Query by key `ID` in tb_json')
    plt.xlabel('Length of JSON')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/json/res_id_ix_every_col.png')
    # plt.show()


def jsonb_by_id_every_col_test():
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
    df_counter = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]],
                              columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])

    # 执行查询并记录时间
    for i in range(1, count_row):
        print('[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')

        # 整个 data 行所有字段
        comm_sql = 'SELECT imdata FROM tb_jsonb WHERE iddata=' + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        full_use_time_ms = (end_time - start_time).microseconds
        row = cur.fetchall()[0]
        len_row_jsonb = len(str(row))  # JSON(B)长度

        # 整个 data 行的字段 nconst
        comm_sql = "SELECT imdata->>'nconst' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        nconst_use_time_ms = (end_time - start_time).microseconds

        # 整个 data 行的字段 name
        comm_sql = "SELECT imdata->>'name' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        name_use_time_ms = (end_time - start_time).microseconds

        # 整个 data 行的字段 birthYear
        comm_sql = "SELECT imdata->>'birthYear' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        birthYear_use_time_ms = (end_time - start_time).microseconds

        # 整个 data 行的字段 profession
        comm_sql = "SELECT imdata->>'profession' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        profession_use_time_ms = (end_time - start_time).microseconds

        # 整个 data 行的字段 rols
        comm_sql = "SELECT imdata->>'rols' FROM tb_jsonb WHERE iddata=" + str(i) + ';'
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        rols_use_time_ms = (end_time - start_time).microseconds

        df_tmp = pd.DataFrame([[len_row_jsonb, full_use_time_ms, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, profession_use_time_ms, rols_use_time_ms]],
                              columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/jsonb/res_id_ix_every_col.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['full_ms'].values,
                label='full row')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['nconst_ms'].values,
                label='nconst')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['name_ms'].values,
                label='name')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['birthYear_ms'].values,
                label='birthYear')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['profession_ms'].values,
                label='profession')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['rols_ms'].values,
                label='rols')
    plt.legend()
    plt.title('Query by key `ID` in tb_jsonb')
    plt.xlabel('Length of JSONB')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/jsonb/res_id_ix_every_col.png')
    # plt.show()


def jsonb_uodate_by_id_every_col_test():
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
    df_counter = pd.DataFrame([[0, 0, 0, 0, 0]],
                              columns=['len_row', 'nconst_ms', 'name_ms', 'birthYear_ms', 'rols_ms'])

    # 执行查询并记录时间
    for i in range(1, 100):
        print('\n[INFO] 正在测试第 ' + str(i) + '行 | ' + str(round(i / count_row * 100, 4)) + '%')

        try:
            # 整个 data 行所有字段
            comm_sql = 'SELECT imdata FROM tb_jsonb WHERE iddata=' + str(i) + ';'
            cur.execute(comm_sql)
            len_row_jsonb = len(str(cur.fetchall()[0]))  # JSON(B)长度

            cur.execute('BEGIN;')

            print('\tBEGIN;')

            # 整个 data 行的字段 nconst
            comm_sql = "UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{nconst}', '\"tt0000009\"'::jsonb) WHERE iddata=" + str(i) + ';'
            # comm_sql = "UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, \'{nconst}\', \'\"tt0000009\"\'::jsonb) WHERE iddata=" + str(i) + ';'
            # print(comm_sql)
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            nconst_use_time_ms = (end_time - start_time).microseconds
            print('\tnconst 测试结束, 用时：', nconst_use_time_ms, ' ms')

            # 整个 data 行的字段 name
            comm_sql = "UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '\"tt_name\"'::jsonb) WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            name_use_time_ms = (end_time - start_time).microseconds
            print('\tname 测试结束, 用时：', name_use_time_ms, ' ms')

            # 整个 data 行的字段 birthYear
            comm_sql = "UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{birthYear}', '\"2222\"'::jsonb) WHERE iddata=" + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            birthYear_use_time_ms = (end_time - start_time).microseconds
            print('\tbirthYear 测试结束, 用时：', birthYear_use_time_ms, ' ms')

            # 整个 data 行的字段 rols
            comm_sql = 'UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, \'{rols}\', \'[{"year": 2000, "title": "t_title", "series name": "t_series", "character name": "t_character_name"}]\'::jsonb) WHERE iddata=' + str(i) + ';'
            start_time = datetime.datetime.now()
            cur.execute(comm_sql)
            end_time = datetime.datetime.now()
            rols_use_time_ms = (end_time - start_time).microseconds
            print('\trols 测试结束, 用时：', rols_use_time_ms, ' ms')

        except:
            cur.execute('ROLLBACK;')
            continue

        cur.execute('ROLLBACK;')
        df_tmp = pd.DataFrame([[len_row_jsonb, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, rols_use_time_ms]],
                              columns=['len_row', 'nconst_ms', 'name_ms', 'birthYear_ms', 'rols_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/jsonb/res_update_id_ix_every_col.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['nconst_ms'].values,
                label='nconst')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['name_ms'].values,
                label='name')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['birthYear_ms'].values,
                label='birthYear')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['rols_ms'].values,
                label='rols')
    plt.legend()
    plt.title('Test UPDATE, query by key `ID` in tb_jsonb')
    plt.xlabel('Length of JSONB')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/jsonb/res_update_id_ix_every_col.png')
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


def json_by_where_nconst_only_full_row_test():
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
    for nconst in arr_nconst[:1000]:
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


def jsonb_by_where_nconst_only_full_row_test():
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
    for nconst in arr_nconst[:3000]:
        i += 1
        print('\n[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | nconst = ', nconst)

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


def json_by_where_nconst_every_col_test():
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
    df_counter = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]],
                              columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms',
                                       'rols_ms'])
    # TODO 取消分割
    # for nconst in arr_nconst[:2000]:
    for nconst in arr_nconst[:10]:
        i += 1
        print('\n[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / count_row * 100, 4)) + '% | nconst = ', nconst)

        # 整个 data 行所有字段
        comm_sql = "SELECT imdata FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        try:
            cur.execute(comm_sql)
        except:
            print('[INFO] 第 ' + str(i) + ' 行取消 | nconst = ', nconst)
            continue
        end_time = datetime.datetime.now()
        full_use_time_ms = (end_time - start_time).microseconds
        row = cur.fetchall()[0]
        len_row_json = len(str(row))  # JSON(B)长度
        print('\tfull row 用时：', (end_time - start_time).seconds, 's')

        # 整个 data 行的字段 nconst
        comm_sql = "SELECT imdata->>'nconst' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        nconst_use_time_ms = (end_time - start_time).microseconds
        print('\tnconst 用时：', (end_time - start_time).seconds, 's')



        # 整个 data 行的字段 name
        comm_sql = "SELECT imdata->>'name' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        name_use_time_ms = (end_time - start_time).microseconds
        print('\tname 用时：', (end_time - start_time).seconds, 's')

        # 整个 data 行的字段 birthYear
        comm_sql = "SELECT imdata->>'birthYear' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        birthYear_use_time_ms = (end_time - start_time).microseconds
        print('\tbirthYear 用时：', (end_time - start_time).seconds, 's')

        # 整个 data 行的字段 profession
        comm_sql = "SELECT imdata->>'profession' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        profession_use_time_ms = (end_time - start_time).microseconds
        print('\tprofession 用时：', (end_time - start_time).seconds, 's')

        # 整个 data 行的字段 rols
        comm_sql = "SELECT imdata->>'rols' FROM tb_json WHERE imdata::json->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        rols_use_time_ms = (end_time - start_time).microseconds
        print('\trols 用时：', (end_time - start_time).seconds, 's')


        df_tmp = pd.DataFrame([[len_row_json, full_use_time_ms, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, profession_use_time_ms, rols_use_time_ms]],
                              columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/json/res_by_nconst_all_col.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['full_ms'].values,
                label='full row')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['nconst_ms'].values,
                label='nconst')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['name_ms'].values,
                label='name')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['birthYear_ms'].values,
                label='birthYear')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['profession_ms'].values,
                label='profession')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['rols_ms'].values,
                label='rols')
    plt.legend()
    plt.title('Query by key `nconst` in tb_json')
    plt.xlabel('Length of JSON')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/json/res_by_nconst_all_col.png')
    # plt.show()


def jsonb_by_where_nconst_every_col_test():
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
    df_counter = pd.DataFrame([[0, 0, 0, 0, 0, 0, 0]],
                              columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms',
                                       'rols_ms'])
    # TODO 取消分割
    # for nconst in arr_nconst[:1000]:
    for nconst in arr_nconst[:2500]:
        i += 1
        print('[INFO] 正在测试第 ' + str(i) + ' 行 | ' + str(round(i / 2500 * 100, 4)) + '% | nconst = ', nconst)

        # 整个 data 行所有字段
        comm_sql = "SELECT imdata FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        try:
            cur.execute(comm_sql)
        except:
            print('[INFO] 第 ' + str(i) + ' 行取消 | nconst = ', nconst)
            continue
        end_time = datetime.datetime.now()
        full_use_time_ms = (end_time - start_time).microseconds
        row = cur.fetchall()[0]
        len_row_jsonb = len(str(row))  # JSON(B)长度
        print('\tfull row 用时：', (end_time - start_time).seconds, 's')

        # 整个 data 行的字段 nconst
        comm_sql = "SELECT imdata->>'nconst' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        nconst_use_time_ms = (end_time - start_time).microseconds
        print('\tnconst 用时：', (end_time - start_time).seconds, 's')


        # 整个 data 行的字段 name
        comm_sql = "SELECT imdata->>'name' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        name_use_time_ms = (end_time - start_time).microseconds
        print('\tname 用时：', (end_time - start_time).seconds, 's')

        # 整个 data 行的字段 birthYear
        comm_sql = "SELECT imdata->>'birthYear' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        birthYear_use_time_ms = (end_time - start_time).microseconds
        print('\tbirthYear 用时：', (end_time - start_time).seconds, 's')

        # 整个 data 行的字段 profession
        comm_sql = "SELECT imdata->>'profession' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        profession_use_time_ms = (end_time - start_time).microseconds
        print('\tprofession 用时：', (end_time - start_time).seconds, 's')

        # 整个 data 行的字段 rols
        comm_sql = "SELECT imdata->>'rols' FROM tb_jsonb WHERE imdata::jsonb->>'nconst' = '" + nconst + "';"
        start_time = datetime.datetime.now()
        cur.execute(comm_sql)
        end_time = datetime.datetime.now()
        rols_use_time_ms = (end_time - start_time).microseconds
        print('\trols 用时：', (end_time - start_time).seconds, 's')


        df_tmp = pd.DataFrame([[len_row_jsonb, full_use_time_ms, nconst_use_time_ms, name_use_time_ms, birthYear_use_time_ms, profession_use_time_ms, rols_use_time_ms]],
                              columns=['len_row', 'full_ms', 'nconst_ms', 'name_ms', 'birthYear_ms', 'profession_ms', 'rols_ms'])
        df_counter = pd.concat([df_counter, df_tmp])

    conn.close()

    df_counter = df_counter.iloc[1:, :]
    df_counter.sort_values(by='len_row', inplace=True)

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open('./result/jsonb/res_by_nconst_all_col.bits', 'wb')
    pickle.dump(obj=df_counter, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # print(df_counter)

    """绘制结果"""
    plt.figure(figsize=(20, 10), dpi=100)
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['full_ms'].values,
                label='full row')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['nconst_ms'].values,
                label='nconst')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['name_ms'].values,
                label='name')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['birthYear_ms'].values,
                label='birthYear')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['profession_ms'].values,
                label='profession')
    plt.scatter(x=df_counter['len_row'].values,
                y=df_counter['rols_ms'].values,
                label='rols')
    plt.legend()
    plt.title('Query by key `nconst` in tb_jsonb')
    plt.xlabel('Length of JSONB')
    plt.ylabel('Query time (milliseconds)')
    plt.savefig('./result/jsonb/res_by_nconst_all_col.png')
    # plt.show()


if __name__ == '__main__':
    # get_id_len_json_df()

    # json_by_id_every_col_test()

    # jsonb_by_id_every_col_test()

    # json_id_test()

    # jsonb_id_test()

    # json_where_name_test()

    # jsonb_name_test()

    # jsonb_where_nconst_test()

    # json_where_nconst_test()

    # jsonb_by_where_nconst_every_col_test()

    # json_by_where_nconst_every_col_test()

    jsonb_uodate_by_id_every_col_test()





