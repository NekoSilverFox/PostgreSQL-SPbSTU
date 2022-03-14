-- 输出到达 `ST.PETERSBURG` 港口的船舶信息，并按照到达时间升序排序
-- Вывести информацию о судах, прибывающих в порт `ST.PETERSBURG`, отсортированную в порядке возрастания времени прибытия

WITH RegPort AS (
	SELECT idport AS IDRegPort, nameport AS NameRegPort FROM tb_ports
)
SELECT arrivaltime, nameseacraft, nametypeseacraft, displacement, NameRegPort, namecaptain
	FROM tb_ports
		INNER JOIN tb_arrivals
			ON tb_arrivals.PortID=tb_ports.IDPort
		INNER JOIN tb_seacrafts
			ON tb_seacrafts.idseacraft=tb_arrivals.seacraftid
		INNER JOIN tb_typeseacraft
			ON tb_typeseacraft.idtypeseacraft=tb_seacrafts.typeid
		INNER JOIN RegPort
			ON RegPort.IDRegPort=tb_seacrafts.RegPortID
		INNER JOIN tb_captains
			ON tb_captains.idcaptain=tb_seacrafts.captainid
	WHERE tb_ports.nameport='ST.PETERSBURG'
	ORDER BY ArrivalTime ASC
	
	
-- 注册地是中国且到达阿塞拜疆次数大于 2 的船只
-- Корабль, зарегистрированные в Китае и прибывающие в Азербайджан более 2 раз
SELECT IDSeacraft, NameSeacraft, COUNT(IDSeacraft) AS Times
	FROM tb_arrivals
		INNER JOIN tb_seacrafts 
			ON tb_seacrafts.IDSeacraft=tb_arrivals.SeacraftID
	WHERE tb_arrivals.PortID 			IN (SELECT IDPort FROM tb_ports WHERE Country='Azerbaijan')
		AND tb_arrivals.SeacraftID 	IN (SELECT IDSeacraft AS SeacraftIDWithCountry FROM tb_seacrafts 
																			WHERE RegPortID IN (SELECT IDPort FROM tb_ports WHERE Country='China'))
	GROUP BY IDSeacraft, NameSeacraft
	HAVING COUNT(SeacraftID) > 2
	ORDER BY IDSeacraft
																			

-- 名字第二个字母是 `e` 的船长，以及到达各个码头的次数。并只输出第 10 到 30 条记录
-- Капитаны со второй буквой своего имени `e` и количество раз, когда они прибывали к каждому пирсу. и выводить только записи с 10-й по 30-ю
WITH tb_NameCaptainWithE AS (
	SELECT * FROM tb_captains WHERE NameCaptain LIKE '_e%'
)
SELECT tb_NameCaptainWithE.NameCaptain, tb_ports.Country, tb_ports.NamePort, COUNT(tb_ports.IDPort)
	FROM tb_seacrafts
		INNER JOIN tb_arrivals
			ON tb_arrivals.SeacraftID=tb_seacrafts.IDSeacraft
		INNER JOIN tb_NameCaptainWithE
			ON tb_NameCaptainWithE.IDCaptain=tb_seacrafts.CaptainID
		INNER JOIN tb_ports
			ON tb_ports.IDPort=tb_arrivals.PortID
	GROUP BY tb_ports.Country, tb_ports.IDPort, tb_ports.NamePort, tb_NameCaptainWithE.NameCaptain
	ORDER BY tb_NameCaptainWithE.NameCaptain, tb_ports.Country, tb_ports.IDPort
	LIMIT 20 OFFSET 9



-- 将注册在巴库的排水量小于 30 0000 的 Container ship 的排水量全部增加 1000 吨
-- увеличить водоизмещение всех зарегистрированных в Баку контейнеровозов водоизмещением менее 30 000 тонн на 1 000 тонн
UPDATE tb_seacrafts
	SET Displacement = Displacement + 1000
	WHERE IDSeacraft IN (
												SELECT IDSeacraft
													FROM tb_seacrafts
													WHERE RegPortID=(SELECT IDPort FROM tb_ports WHERE NamePort='baku')
														AND TypeID=(SELECT IDTypeSeacraft FROM tb_typeseacraft WHERE NameTypeSeacraft='Container ship'))
														
SELECT * FROM tb_seacrafts WHERE IDSeacraft=2


-- 将所有 2020 年之后到达巴库的船只的离开时间推迟一个月
-- Отложить на один месяц отплытие всех корабли, прибывающих в Баку после 2020 года
UPDATE tb_arrivals
	SET LeaveTime = LeaveTime::TIMESTAMP + '1 month'
	WHERE IDArrival IN (
												SELECT IDArrival FROM tb_arrivals
													WHERE PortID=(SELECT IDPort FROM tb_ports WHERE NamePort='baku')
														AND ArrivalTime > '2020-01-01'::TIMESTAMP)
		
SELECT * FROM tb_arrivals WHERE IDArrival=15



-- 删除在巴库停留时间大于 7 个月的记录（只删除第一行）
-- Удалить записи, которые находились в Баку более 7 месяцев (только первая строка)
DELETE FROM tb_arrivals 
	WHERE IDArrival IN (
											SELECT IDArrival FROM tb_arrivals WHERE (LeaveTime::TIMESTAMP - ArrivalTime::TIMESTAMP) > '7 month' LIMIT 1)
	
SELECT * FROM tb_arrivals WHERE (LeaveTime::TIMESTAMP - ArrivalTime::TIMESTAMP) > '7 month'


-- [+] over()
--  每个港口收费与它们国家的平均值作对比
-- Сравнение тарифов каждого порта со средним значением тарифов по стране
SELECT IDPort, Country, NamePort, Price,
				AVG(Price) OVER (PARTITION BY Country)
	FROM tb_ports
	ORDER BY Country, NamePort
	
