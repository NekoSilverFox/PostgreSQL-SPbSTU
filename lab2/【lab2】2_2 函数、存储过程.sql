--------------------------------- Функция ---------------------------------
-- 评估船舶滞留码头时间的等级
-- Оценка уровня времени, в течение которого корабль простаивает в порте
CREATE OR REPLACE FUNCTION fc_PortTimeChecker(INTEGER) RETURNS TEXT 
	LANGUAGE plpgsql
	AS $$
	DECLARE 
		t_ArrivalTime TIMESTAMP := (SELECT ArrivalTime::TIMESTAMP FROM tb_arrivals WHERE IDArrival=$1);
		t_LeaveTime TIMESTAMP := (SELECT LeaveTime::TIMESTAMP FROM tb_arrivals WHERE IDArrival=$1);
		Days INTEGER;
		msg TEXT;
	BEGIN
		IF (t_LeaveTime IS NULL) THEN 
			RAISE EXCEPTION '[ERROR] LeaveTime can not be NULL';
		END IF;
		
		Days := extract(day from t_LeaveTime - t_ArrivalTime);
		CASE
			WHEN Days BETWEEN 0 AND 30 THEN
				msg := 'Short';
			WHEN Days BETWEEN 30 AND 100 THEN
				msg := 'Normal';
			WHEN Days BETWEEN 100 AND 150 THEN
				msg := 'Long';
			ELSE
				msg := 'Very long';
		END CASE;
		
		RETURN msg;
	END;
	$$;

SELECT fc_PortTimeChecker(1)
SELECT fc_PortTimeChecker(2)

-- 【LOOP】评估船舶滞留码头时间的等级
-- 【LOOP】Оценка уровня времени, в течение которого корабль простаивает в порте
CREATE OR REPLACE FUNCTION fc_AllPortTimeChecker() RETURNS TEXT 
	LANGUAGE plpgsql
	AS $$
	DECLARE 
 		t_ArrivalTime TIMESTAMP;
 		t_LeaveTime TIMESTAMP;
		StartNum INTEGER := (SELECT min(idarrival) FROM tb_arrivals);
		StopNum INTEGER := (SELECT max(idarrival) FROM tb_arrivals);
		Days INTEGER;
		msg TEXT;
	BEGIN
		FOR counter IN StartNum .. StopNum LOOP
				IF (t_LeaveTime IS NULL) THEN 
					RAISE NOTICE 'IDArrival: % con not handle', counter;
				END IF;		
						
				t_ArrivalTime := (SELECT ArrivalTime::TIMESTAMP FROM tb_arrivals WHERE IDArrival=counter);
				t_LeaveTime := (SELECT LeaveTime::TIMESTAMP FROM tb_arrivals WHERE IDArrival=counter);
				Days := extract(day from t_LeaveTime - t_ArrivalTime);
				CASE
					WHEN Days BETWEEN 0 AND 30 THEN
						msg := 'Short';
					WHEN Days BETWEEN 30 AND 100 THEN
						msg := 'Normal';
					WHEN Days BETWEEN 100 AND 150 THEN
						msg := 'Long';
					ELSE
						msg := 'Very long';
				END CASE;
		
			RAISE NOTICE 'IDArrival: %, Level: %', counter, msg;
		END LOOP;
	
		RETURN msg;
	END;
	$$;

SELECT fc_AllPortTimeChecker()


-- 获取船舶的自定义到达编号
-- Получение пользовательского номера прибытия корабля
CREATE OR REPLACE FUNCTION get_arrival_num(INTEGER) RETURNS VARCHAR
	AS
		'SELECT to_char(ArrivalTime, ''yyyy'') 
						|| to_char(ArrivalTime, ''mm'') 
						|| to_char(ArrivalTime, ''dd'')
						|| lpad(IDArrival::TEXT, 5, ''0'')::TEXT 
						|| lpad(PortID::TEXT, 3, ''0'')::TEXT 
		FROM tb_arrivals WHERE IDArrival=$1'
	LANGUAGE SQL
	RETURNS NULL ON NULL INPUT;
	
SELECT IDArrival, get_arrival_num(IDArrival) FROM tb_arrivals 


-- 根据指定港口的服务总时长
-- Общее количество часов работы в соответствии с назначенным портом
CREATE OR REPLACE FUNCTION fc_IncomePort(VARCHAR) RETURNS INTEGER
	AS
	'
			SELECT SUM(hours) AS hours FROM(
				SELECT EXTRACT(
					DAY FROM (
							SELECT SUM(LeaveTime::TIMESTAMP - ArrivalTime::TIMESTAMP)
							FROM tb_arrivals 
							WHERE PortID=(SELECT IDPort FROM tb_ports WHERE NamePort=$1)
						)
				) * 24 AS hours
				UNION ALL
				SELECT EXTRACT(
					HOUR FROM (
							SELECT SUM(LeaveTime::TIMESTAMP - ArrivalTime::TIMESTAMP)
							FROM tb_arrivals 
							WHERE PortID=(SELECT IDPort FROM tb_ports WHERE NamePort=$1)
						)
				) AS hours
		) AS hour_row
	'
	LANGUAGE SQL
	RETURNS NULL ON NULL INPUT;
	
DROP FUNCTION fc_IncomePort;
-- 
SELECT fc_IncomePort('baku');

WITH SumTimes AS (
		SELECT SUM(hours) AS hours FROM(
			SELECT EXTRACT(
				DAY FROM (
						SELECT SUM(LeaveTime::TIMESTAMP - ArrivalTime::TIMESTAMP)
						FROM tb_arrivals 
						WHERE PortID=(SELECT IDPort FROM tb_ports WHERE NamePort='baku')
					)
			) * 24 AS hours
			UNION ALL
			SELECT EXTRACT(
				HOUR FROM (
						SELECT SUM(LeaveTime::TIMESTAMP - ArrivalTime::TIMESTAMP)
						FROM tb_arrivals 
						WHERE PortID=(SELECT IDPort FROM tb_ports WHERE NamePort='baku')
					)
			) AS hours
	) AS hour_row
)
SELECT * from SumTimes

DROP EXTENSION plpython3u;
CREATE EXTENSION plpython3u;