# ------*------ coding: utf-8 ------*------
# @Time    : 2022/4/27 14:37
# @Author  : 冰糖雪狸 (NekoSilverfox)
# @Project : IMDB 数据处理
# @File    : 反序列化数据.py.py
# @Software: PyCharm
# @Github  ：https://github.com/NekoSilverFox
# -----------------------------------------
import pickle
import datetime
import pandas as pd


def concat_df(bits_file_path_header: str,
              max_index: int,
              path_result_bits_save: str) -> pd.DataFrame:
    """
    从许多序列化文件中反序列化，并且拼接他们
    :param bits_file_path_header: 序列化文件的【文件头】
    :param max_index: 文件头的最大索引
    :param path_result_bits_save: 合并结果的反序列化保存位置
    :return: 反序列化后的 DataFrame
    """
    df_result = None

    for i in range(1, max_index + 1):
        print('-' * 50)
        print('[INFO] 开始读取第 ', i, '个文件')
        time_start = datetime.datetime.now()
        bits_file_path = bits_file_path_header + str(i) + '.bits'
        f = open(bits_file_path, 'rb')
        df_obj = pickle.load(file=f)
        f.close()
        time_end = datetime.datetime.now()
        print('[INFO] 读取第 ', i, '个文件结束，用时：', (time_end - time_start).seconds, ' 秒\n')

        if i == 1:
            df_result = df_obj
            continue

        print('[INFO] 开始拼接第 ', i, '个文件')
        time_start = datetime.datetime.now()
        df_result = pd.concat([df_result, df_obj])
        time_end = datetime.datetime.now()
        print('[INFO] 拼接第 ', i, '个文件结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    # 合并结束，使用序列化保存结果
    print('-' * 50)
    print('[INFO] 合并结束，使用序列化保存结果')
    time_start = datetime.datetime.now()
    f = open(path_result_bits_save, 'wb')
    pickle.dump(obj=df_result, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    return df_result


def merge_duplicates(df_source: pd.DataFrame) -> pd.DataFrame:
    """
    将最终的结果再次去重
    :param df_source: 合并男女演员是数组
    :return: 合并去重后的 DataFrame
    """
    df_source.sort_values(by='nconst', inplace=True)
    df_source.reset_index(drop=True, inplace=True)

    i_current = 0
    i_next = i_current + 1
    stop_index = df_source.shape[0]
    while i_next != stop_index:
        while df_source.loc[i_current]['nconst'] == df_source.loc[i_next]['nconst']:
            df_source.loc[i_current]['rols'] = pd.concat([df_source.loc[i_current]['rols'], df_source.loc[i_next]['rols']])
            df_source.drop(index=i_next, inplace=True)
            i_next += 1

            if i_next == stop_index:
                df_source.reset_index(drop=True, inplace=True)
                return df_source

        i_current = i_next
        i_next += 1

    df_source.reset_index(drop=True, inplace=True)
    return df_source







if __name__ == '__main__':
    ################################################################################################################
    # 合并所有男演员（actors）
    ################################################################################################################
    print('>>' * 50)
    bits_file_path_header = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                            '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                            'семестр/СУБД/资料/DataSet/result_dump_actors/dump_actors_'

    path_result_bits_save = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                            '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                            'семестр/СУБД/资料/DataSet/result_dump_actors/dump_actors_ALL.bits'

    df_all_actors = concat_df(bits_file_path_header=bits_file_path_header,
                              max_index=20,
                              path_result_bits_save=path_result_bits_save)
    print('[INFO] 合并并序列化输出成功！\n输出至：', path_result_bits_save)


    ################################################################################################################
    # 合并所有女演员（actors）
    ################################################################################################################
    print('>>' * 50)
    bits_file_path_header = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                            '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                            'семестр/СУБД/资料/DataSet/result_dump_actresses/dump_actresses_'

    path_result_bits_save = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                            '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                            'семестр/СУБД/资料/DataSet/result_dump_actresses/dump_actresses_ALL.bits'

    df_all_actresses = concat_df(bits_file_path_header=bits_file_path_header,
                                 max_index=13,
                                 path_result_bits_save=path_result_bits_save)
    print('[INFO] 合并并序列化输出成功！\n输出至：', path_result_bits_save)


    ################################################################################################################
    # 合并所有男演员（actors）和女演员（actors）
    ################################################################################################################
    print('>>' * 50)
    print('[INFO] 合并所有男演员（actors）和女演员（actors）')
    time_start = datetime.datetime.now()

    df_result_all = pd.concat([df_all_actors, df_all_actresses])

    time_end = datetime.datetime.now()
    print('[INFO] 合并所有男演员（actors）和女演员（actors）结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    ################################################################################################################
    df_all_actors = None
    df_all_actresses = None
    print('[INFO] 内存释放')
    ################################################################################################################


    ################################################################################################################
    # 合并后的最终结果再次去重并保存为 JSON 文件
    ################################################################################################################
    # TODO

    ################################################################################################################
    # 合并后的最终结果再序列化并保存为 JSON 文件
    ################################################################################################################
    path_result_bits_save = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                            '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                            'семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.bits'

    path_result_json_save = '/Users/fox/Library/CloudStorage/OneDrive-PetertheGreatSt' \
                            '.PetersburgPolytechnicalUniversity/СПБПУ/3 курс/6 ' \
                            'семестр/СУБД/资料/DataSet/result_ALL/dump_ALL.json'

    print('>>' * 50)
    print('[INFO] 合并结束，使用序列化保存[最终]结果')
    time_start = datetime.datetime.now()
    f = open(path_result_bits_save, 'wb')
    pickle.dump(obj=df_result_all, file=f)
    f.close()
    time_end = datetime.datetime.now()
    print('[INFO] 序列化保存结果结束，用时：', (time_end - time_start).seconds, ' 秒\n')

    print('>>' * 50)
    print('[INFO] 保存[最终]结果为 JSON')
    time_start = datetime.datetime.now()
    df_result_all.to_json(path_or_buf=path_result_json_save,
                          orient='records',
                          lines=True)
    time_end = datetime.datetime.now()
    print('[INFO] 保存[最终]结果为 JSON，用时：', (time_end - time_start).seconds, ' 秒\n')

    pass
