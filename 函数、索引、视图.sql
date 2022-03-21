--------------------------------- 函数 ---------------------------------
-- 获取自定义到达编号
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


--------------------------------- 索引 ---------------------------------
CREATE INDEX IX_Arrival ON tb_arrivals(IDArrival)
DROP INDEX IX_Arrival


--------------------------------- 视图 ---------------------------------
CREATE VIEW VW_Seacrafts
AS
	SELECT idseacraft, nameseacraft, nametypeseacraft, displacement, NamePort, namecaptain
		FROM tb_seacrafts
			INNER JOIN tb_typeseacraft
				ON tb_typeseacraft.idtypeseacraft=tb_seacrafts.typeid
			INNER JOIN tb_ports
				ON tb_ports.IDPort=tb_seacrafts.RegPortID
			INNER JOIN tb_captains
				ON tb_captains.idcaptain=tb_seacrafts.captainid
		ORDER BY idseacraft ASC;
		
SELECT * FROM VW_Seacrafts
