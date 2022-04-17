CREATE EXTENSION plpython3u;

------------------------------------------------------------------------------------------------------
-- 向 tb_arrivals 中插入 10000 0000 条随机数据记录
-- Вставьте 100 000 000 случайных записей данных в tb_arrivals
CREATE OR REPLACE FUNCTION fc_InsertArrivals()
	RETURNS TEXT
	AS $$
import random
import datetime


COL_NUM = 100000000


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
    try:
        num_port = plpy.execute("SELECT COUNT(*) FROM tb_ports")[0]['count']
        num_seacraft = plpy.execute("SELECT COUNT(*) FROM tb_seacrafts")[0]['count']
        # return str(num_port)
            
        for i in range(COL_NUM):
            portid = random.randint(1, num_port)
            seacraftid = random.randint(1, num_seacraft)
            purpose = get_random_text()
            arrival_leave_time = get_random_start_end_time()
            command = 'INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, LeaveTime) VALUES ('
            command = command + str(portid) + ', ' + str(seacraftid) + ', ' + purpose + ', ' + arrival_leave_time + ');'
            # return command
            plpy.execute(command)

    except plpy.SPIError as e:
        return "[ERROR] %s" % e.sqlstate

    else:
        return "[Info] Succful insert"
        
$$ LANGUAGE plpython3u;

----------------------------------------------------------

TRUNCATE TABLE tb_arrivals CASCADE;
SELECT fc_InsertArrivals();  -- 运行时间 13040 秒


SELECT COUNT(*) FROM tb_arrivals; -- 运行时间 26.195 秒
