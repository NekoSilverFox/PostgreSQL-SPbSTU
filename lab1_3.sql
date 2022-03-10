-- 输出到达 `圣彼得堡` 港口的船舶信息，并按照到达时间升序排序
SELECT arrivaltime, nameseacraft, nametypeseacraft, displacement, NameRegPort, namecaptain
	FROM tb_ports
		INNER JOIN tb_arrivals
			ON tb_arrivals.PortID=tb_ports.IDPort
		INNER JOIN tb_seacrafts
			ON tb_seacrafts.idsercraft=tb_arrivals.seacraftid
		INNER JOIN tb_typeseacraft
			ON tb_typeseacraft.idtypeseacraft=tb_seacrafts.typeid
		INNER JOIN (SELECT idport AS IDRegPort, nameport AS NameRegPort FROM tb_ports) AS RegPort
			ON RegPort.IDRegPort=tb_seacrafts.registrationportid
		INNER JOIN tb_captains
			ON tb_captains.idcaptain=tb_seacrafts.captainid
	WHERE tb_ports.nameport='ST.PETERSBURG'
	ORDER BY ArrivalTime ASC
	
	
-- 注册地是中国且到达阿塞拜疆次数大于 2 的船只


-- 以字母 `J` 开头的船长，到达各个码头的次数


-- 将注册在巴库的船的排水量全部增加 1000 吨

-- 将所有 2020 年之后到达巴库的船只的离开时间推迟一个月

-- 删除所有 2000 年 2 月之前到达巴库运油船只的记录


