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


def normal_actor(file_path: str) -> pd.DataFrame:
    """
    将 IMDB 的演员数据标准化为 pd.DataFrame。每个演员及其各个作品独占一行（类似于交叉表）
    建议之前将数据通过 VS Code 处理
    :param file_path: 
    :return: pd.DataFrame
    """
    source_data = pd.read_csv(
        filepath_or_buffer=file_path,
        header=0,
        sep='\t'
    )
    source_data.columns = ['Name', 't1', 't2', 't3']
    source_data['t1'].fillna(value='', inplace=True)
    source_data['t2'].fillna(value='', inplace=True)
    source_data['t3'].fillna(value='', inplace=True)

    movie_list = source_data['t1'] + source_data['t2'] + source_data['t3']
    source_data = pd.concat([source_data['Name'], movie_list], axis=1)
    source_data.columns = ['Name', 'Title_mix']

    res_name_title = []
    name_list = []

    for col in source_data.values:
        if col[0] is not np.nan:
            title = None
            year = None
            series_name = None  # 系列名称： {}
            character_name = None  # 角色名称

            names = col[0]
            name_list = names.split(', ')

            title_mix = col[1]

        for this_name in name_list:
            res_name_title.append([this_name, col[1]])

    return pd.DataFrame(res_name_title, columns=['Name', 'Title'])


if __name__ == '__main__':
    # 女演员列表df
    df_actresses = normal_actor(
        file_path='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                  'курс/6 семестр/СУБД/资料/DataSet/data_actresses.list.txt'
    )

    # 男演员列表df
    df_actors = normal_actor(
        file_path='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity/СПБПУ/3 '
                  'курс/6 семестр/СУБД/资料/DataSet/data_actors.list.txt'
    )

    # 拼接两个df
    df_all_actors = pd.concat([df_actresses, df_actors], axis=0)
    df_all_actors.to_csv(
        path_or_buf='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity'
                    '/СПБПУ/3 курс/6 семестр/СУБД/资料/DataSet/df_all.csv')

    # # 演员信息表
    # df_name_info = pd.read_csv(
    #     filepath_or_buffer='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt'
    #                        '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 семестр/СУБД/资料/DataSet/name.basics.tsv',
    #     header=0,
    #     sep='\t'
    # )
    # df_name_info = df_name_info.iloc[:, :-1]
    # df_name_info.columns = ['nconst', 'Name', 'birthYear', 'deathYear', 'profession']
    #
    # df_all = pd.merge(left=df_name_info,
    #                   right=df_all_actors,
    #                   how='inner',
    #                   on='Name')
    #
    # df_all.to_csv(
    #     path_or_buf='/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt.PetersburgPolytechnicalUniversity'
    #                 '/СПБПУ/3 курс/6 семестр/СУБД/资料/DataSet/df_all.csv')

    pass
