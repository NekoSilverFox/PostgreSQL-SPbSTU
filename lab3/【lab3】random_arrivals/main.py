# ------*------ coding: utf-8 ------*------
# @Time    : 2022/3/13 19:57
# @Author  : 冰糖雪狸 (NekoSilverfox)
# @Project : pythonProject
# @File    : main.py
# @Software: PyCharm
# @Github  ：https://github.com/NekoSilverFox
# -----------------------------------------
import random
import datetime


def get_random_text():
    """
    生成一段随机 `text`
    :return: text -> string
    """
    text = ''
    num_word = random.randint(1, 20)
    for i in range(num_word):
        len_word = random.randint(1, 10)
        word = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba', len_word))
        text += (word + ' ')

    return "'" + text + "'"


def get_random_start_end_time():
    """
    获取一个随机开始时间 `start_time_str` 和随机结束时间 `end_time_str` 合并之后的字符串
    :return: string -> start time and end time
    """
    start = '1900-01-01 00:00:00'
    end = '2022-04-15 00:00:00'
    frmt = '%Y-%m-%d %H:%M:%S'
    num_hour = random.randint(12, 7 * 24)
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    time_datetime = random.random() * (etime - stime) + stime
    start_time_str = time_datetime.strftime(frmt)
    end_time_str = (time_datetime + datetime.timedelta(hours=num_hour)).strftime(frmt)

    return "'" + start_time_str + "', '" + end_time_str + "'"


if __name__ == '__main__':
    print(get_random_text())
    print(get_random_start_end_time())
