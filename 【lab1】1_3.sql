-- 输出到达 `圣彼得堡` 港口的船舶信息，并按照到达时间升序排序
SELECT arrivaltime, nameseacraft, nametypeseacraft, displacement, NameRegPort, namecaptain
	FROM tb_ports
		INNER JOIN tb_arrivals
			ON tb_arrivals.PortID=tb_ports.IDPort
		INNER JOIN tb_seacrafts
			ON tb_seacrafts.idseacraft=tb_arrivals.seacraftid
		INNER JOIN tb_typeseacraft
			ON tb_typeseacraft.idtypeseacraft=tb_seacrafts.typeid
		INNER JOIN (SELECT idport AS IDRegPort, nameport AS NameRegPort FROM tb_ports) AS RegPort
			ON RegPort.IDRegPort=tb_seacrafts.RegPortID
		INNER JOIN tb_captains
			ON tb_captains.idcaptain=tb_seacrafts.captainid
	WHERE tb_ports.nameport='ST.PETERSBURG'
	ORDER BY ArrivalTime ASC
	
	
-- 注册地是中国且到达阿塞拜疆次数大于 2 的船只
SELECT IDSeacraft, NameSeacraft, COUNT(SeacraftID) AS Times
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
SELECT tb_NameCaptainWithE.NameCaptain, tb_ports.Country, tb_ports.NamePort, COUNT(tb_ports.IDPort)
	FROM tb_seacrafts
		INNER JOIN tb_arrivals
			ON tb_arrivals.SeacraftID=tb_seacrafts.IDSeacraft
		INNER JOIN (SELECT * FROM tb_captains WHERE NameCaptain LIKE '_e%') AS tb_NameCaptainWithE
			ON tb_NameCaptainWithE.IDCaptain=tb_seacrafts.CaptainID
		INNER JOIN tb_ports
			ON tb_ports.IDPort=tb_arrivals.PortID
	GROUP BY tb_ports.Country, tb_ports.IDPort, tb_ports.NamePort, tb_NameCaptainWithE.NameCaptain
	ORDER BY tb_NameCaptainWithE.NameCaptain, tb_ports.Country, tb_ports.IDPort
	LIMIT 20 OFFSET 9



-- 将注册在巴库的排水量小于 30 0000 的 Container ship 的排水量全部增加 1000 吨
UPDATE tb_seacrafts
	SET Displacement = Displacement + 1000
	WHERE IDSeacraft IN (
												SELECT IDSeacraft
													FROM tb_seacrafts
													WHERE 
														AND TypeID=(SELECT IDTypeSeacraft FROM tb_typeseacraft WHERE NameTypeSeacraft='Container ship'))
	
	
SELECT * FROM tb_seacrafts WHERE IDSeacraft=2


-- 将所有 2020 年之后到达巴库的船只的离开时间推迟一个月
UPDATE tb_arrivals
	SET LeaveTime = LeaveTime::TIMESTAMP + '1 month'
	WHERE IDArrival IN (
												SELECT IDArrival FROM tb_arrivals
													WHERE PortID=(SELECT IDPort FROM tb_ports WHERE NamePort='baku')
														AND ArrivalTime > '2020-01-01'::TIMESTAMP)
		
SELECT * FROM tb_arrivals WHERE IDArrival=15
		


-- 删除所有在巴库停留时间大于 7 个月的记录（只删除第一行）
DELETE FROM tb_arrivals 
	WHERE IDArrival IN (
											SELECT IDArrival FROM tb_arrivals WHERE (LeaveTime::TIMESTAMP - ArrivalTime::TIMESTAMP) > '7 month' LIMIT 1)
	
SELECT * FROM tb_arrivals WHERE (LeaveTime::TIMESTAMP - ArrivalTime::TIMESTAMP) > '7 month'

