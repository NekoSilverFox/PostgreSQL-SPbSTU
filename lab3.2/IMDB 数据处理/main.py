# ------*------ coding: utf-8 ------*------
# @Time    : 2022/4/22 17:00
# @Author  : 冰糖雪狸 (NekoSilverfox)
# @Project : IMDB 数据处理
# @File    : main.py
# @Software: PyCharm
# @Github  ：https://github.com/NekoSilverFox
# -----------------------------------------
import pandas as pd
import numpy as np
import datetime
import pickle
import re


def normal_actor(file_path: str, dump_name_title: str, dump_df_res: str) -> pd.DataFrame:
    """
    将 IMDB 的演员数据标准化为 pd.DataFrame。每个演员及其各个作品独占一行（类似于交叉表）
    建议之前将数据通过 VS Code 处理
    :param file_path: 
    :return: pd.DataFrame
    """
    print('>>' * 50)
    print('[INFO] 开始读取文件', file_path)
    time_start = datetime.datetime.now()
    source_data = pd.read_csv(
        filepath_or_buffer=file_path,
        header=0,
        sep='\t'
    )

    # source_data = source_data.iloc[:10000, :]

    time_end = datetime.datetime.now()
    print('[INFO] 读取文件结束，用时：', (time_end - time_start).seconds, ' 秒')

    print('>>' * 50)
    print('[INFO] 开始数据预处理')
    time_start = datetime.datetime.now()
    source_data.columns = ['name', 't1', 't2', 't3']
    source_data['t1'].fillna(value='', inplace=True)
    source_data['t2'].fillna(value='', inplace=True)
    source_data['t3'].fillna(value='', inplace=True)

    movie_list = source_data['t1'] + source_data['t2'] + source_data['t3']
    source_data = pd.concat([source_data['name'], movie_list], axis=1)
    source_data.columns = ['name', 'title_mix']

    # source_data = source_data.iloc[:1000, :]

    time_end = datetime.datetime.now()
    print('[INFO] 数据预处理结束，用时：', (time_end - time_start).seconds, ' 秒')

    """
    使用正则表达式提取作品名、上映日期、系列名，并将他们作为新的 DataFrame
    所以取得的结果为带 MutIndex 的 DataFrame
    """
    print('>>' * 50)
    print('[INFO] 开始提取字符串中的信息')
    time_start = datetime.datetime.now()
    list_name_title = []
    i = 1
    for col in source_data.values:
        if col[0] is not np.nan:
            names = col[0]
            name_list = names.split(', ')

        for this_name in name_list:

            title_mix = col[1]

            """电影标题 字符串前一部分"""
            title = re.search(r'^[^\(\{\[]*', title_mix)
            if title is not None:
                title = str(title.group()[:-1])

            """上映年份 ()"""
            year = re.search(r'(?!=\({1})[\d]{4}(?!=\){1})', title_mix)
            if year is not None:
                year = int(year.group())

            """系列名称： {}"""
            series_name = re.search(r'\{(.*?)\}', title_mix)
            if series_name is not None:
                series_name = str(series_name.group()[1:-1])

            """角色名称"""
            character_name = re.search(r'\[(.*?)\]', title_mix)
            if character_name is not None:
                character_name = str(character_name.group()[1:-1])
            # name_title.append([this_name, title, series_name, year, character_name])
            # name_title.append([this_name, [title, series_name, year, character_name]])
            rols = pd.DataFrame([[title, series_name, year, character_name]],
                                columns=['title', 'series name', 'year', 'character name'])

            list_name_title.append([this_name, rols])  # this_name 是 str, rols 是DataFrame

            if i % 10000 == 0:
               use_sec = (datetime.datetime.now() - time_start).seconds
               print('[INFO] 已处理 ', i, ' 行 | ', (i / source_data.shape[0]) * 100, '% | 已用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')
            i += 1
    use_sec = (datetime.datetime.now() - time_start).seconds
    print('[INFO] 数据提取结束，用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')


    """将取得的结果 df_name_title 为带 MutIndex 的 DataFrame"""
    print('>>' * 50)
    print('[INFO] 将取得的结果 df_name_title 为带 MutIndex 的 DataFrame')
    time_start = datetime.datetime.now()
    df_name_title = pd.DataFrame(list_name_title, columns=['name', 'rols'])
    list_name_title = []
    df_name_title.sort_values(by='name', inplace=True)
    df_name_title.reset_index(drop=True, inplace=True)
    use_sec = (datetime.datetime.now() - time_start).seconds
    print('[INFO] DataFrame 转换结束，用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')



    print('>>' * 50)
    print('[INFO] 开始序列化（备份）df_name_title')
    time_start = datetime.datetime.now()
    f = open(dump_name_title, 'wb')
    pickle.dump(obj=df_name_title, file=f)
    f.close()
    use_sec = (datetime.datetime.now() - time_start).seconds
    print('[INFO] 序列化（备份）结束，用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')


    """合并重复的 name，使其唯一。rols 中增加同一演员的信息"""
    print('>>' * 50)
    print('[INFO] 开始合并重复的 name')
    time_start = datetime.datetime.now()
    name = None
    tmp_df_rols = []
    res_list_name_rols = []
    for i in range(df_name_title.shape[0]):

        """如果为同一人，即将作品合并的到一个 DataFrame 中"""
        if name == df_name_title.loc[i]['name']:
            tmp_df_rols = pd.concat([tmp_df_rols, df_name_title.loc[i]['rols']])

        else:
            """开始下一个人
                先将上一个人的信息写入到新的 list 中，再重置 name 和 tmp_df_rols 为当前行的内容
            """
            if name is not None:
                res_list_name_rols.append([name, tmp_df_rols])

                # if name == '$haniqua':
                #     print(tmp_df_rols)

            name = df_name_title.loc[i]['name']
            tmp_df_rols = df_name_title.loc[i]['rols']

        if i % 10000 == 0:
            use_sec = (datetime.datetime.now() - time_start).seconds
            print('[INFO] 已处理 ', i, ' 行 | ', (i / df_name_title.shape[0]) * 100, '% | 已用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')
    

    res_list_name_rols = pd.DataFrame(data=res_list_name_rols, columns=['name', 'rols'])

    print('>>' * 50)
    print('[INFO] 开始序列化（备份）res_list_name_rols')
    time_start = datetime.datetime.now()
    f = open(dump_df_res, 'wb')
    pickle.dump(obj=res_list_name_rols, file=f)
    f.close()
    use_sec = (datetime.datetime.now() - time_start).seconds
    print('[INFO] 序列化（备份）res_list_name_rols 结束，用时：', use_sec, ' 秒（', use_sec / 60, '）分钟')

    return res_list_name_rols


if __name__ == '__main__':
    print('>>' * 50)
    print('[INFO] 开始执行')

    # 女演员列表df
    print('[INFO]  main -> 开始处理 `data_actresses.list.txt`')
    df_actresses = normal_actor(
        file_path='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                  'курс/6 семестр/СУБД/资料/DataSet/data_actresses.list.txt', 
        dump_name_title='./dump_df_actresses_name_title.bits',
        dump_df_res='./dump_df_actresses.bits'
    )
    print('[INFO] 执行结束')

    # print('[INFO] `data_actresses.list.txt` 处理结束，开始写入文件 `result_actresses.csv`')
    # df_actresses.to_csv(path_or_buf='.\\result\\result_actresses.csv')
    # print('[INFO] `result_actresses.csv` 写入完成')


    # # 男演员列表df
    # print('[INFO] Start handle `data_actors.list.txt`')
    # df_actors = normal_actor(
    #     file_path='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
    #               'курс/6 семестр/СУБД/资料/DataSet/data_actors.list.txt'
    # )


    # print('[INFO] `data_actors.list.txt` 处理结束，开始写入文件 `result_actors.csv`')
    # df_actresses.to_csv(path_or_buf='.\\result\\result_actors.csv')
    # print('[INFO] `result_actors.csv` 写入完成')

    # # 拼接两个df
    # print('[INFO] Start to concat two DataFrame')
    # df_all_actors = pd.concat([df_actresses, df_actors], axis=0)

    # print('[INFO] Start write to CSV file `result_all_actors.csv`')
    # df_all_actors.to_csv(path_or_buf='.\\result\\result_all_actors.csv')
    # print('[INFO] `result_all_actors.csv` 写入完成')

    # # print('[INFO] Start write to JSON file')
    # # df_all_actors.to_json(
    # #     path_or_buf='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity'
    # #                 '/СПБПУ/3 курс/6 семестр/СУБД/资料/DataSet/df_all.json',
    # #     orient='table',
    # #     index=False)

    # # 演员信息表
    # print('[INFO] Start handle `name.basics.tsv`')
    # df_name_info = pd.read_csv(
    #     filepath_or_buffer='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt'
    #                        '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 семестр/СУБД/资料/DataSet/name.basics.tsv',
    #     header=0,
    #     sep='\t'
    # )
    # df_name_info = df_name_info.iloc[:, :-1]
    # df_name_info.columns = ['nconst', 'name', 'birthYear', 'deathYear', 'profession']

    # # 处理缺失值为 None，方便转换为 JSON
    # df_name_info.replace(to_replace=['\\N', np.nan], value=None, inplace=True)

    # print('[INFO] Start to merge DataFrame')
    # df_all = pd.merge(left=df_name_info,
    #                   right=df_all_actors,
    #                   how='inner',
    #                   on='name')

    # print('[INFO] Start write to JSON file')
    # df_all.to_json(
    #     path_or_buf='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity'
    #                 '/СПБПУ/3 курс/6 семестр/СУБД/资料/DataSet/df_final_all.json',
    #     orient='table',
    #     index=False)
    # print('[INFO] JSON 写入完成')


    pass
