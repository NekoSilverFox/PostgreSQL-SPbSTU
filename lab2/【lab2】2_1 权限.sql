----------------------------- представлений -----------------------------
-- 各个船舶具体信息的列表
-- Список индивидуальной информации о конкретном корабле
CREATE OR REPLACE VIEW VW_Seacrafts
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
		
SELECT * FROM VW_Seacrafts;


-- 港口详细信息列表
-- Вывод списка подробной информации о порте
CREATE OR REPLACE VIEW VW_Ports
AS
SELECT IDPort, Country, NamePort, NameLevel, Price, COUNT(IDPort) AS NumArrivals
	FROM tb_arrivals
		INNER JOIN tb_ports ON tb_ports.idport=tb_arrivals.portid
		INNER JOIN tb_portlevels ON tb_ports.levelid=tb_portlevels.idlevel
	GROUP BY IDPort, Country, NamePort, NameLevel, Price 
	ORDER BY IDPort ASC;

SELECT * FROM VW_Ports;


----------------------------- управления доступом -----------------------------
-- CREATE USER fox;
CREATE ROLE test;
ALTER ROLE test PASSWORD '123';
ALTER ROLE test LOGIN;


GRANT SELECT, INSERT, UPDATE ON tb_portlevels TO test;
GRANT SELECT, UPDATE ON tb_typeseacraft TO test;
GRANT SELECT ON tb_ports TO test;
GRANT SELECT ON VW_Ports TO test;

CREATE ROLE update_vw_test;
GRANT UPDATE (NameSeacraft) ON vw_seacrafts TO update_vw_test;
GRANT update_vw_test TO test;


-- For user `test`
SELECT * FROM tb_portlevels;
INSERT INTO tb_portlevels(IDLevel, NameLevel) VALUES(4, 'test');
UPDATE tb_portlevels SET NameLevel='tesssst' WHERE IDLevel=4;
DELETE FROM tb_portlevels WHERE IDLevel=4;

SELECT * FROM tb_typeseacraft;
INSERT INTO tb_typeseacraft(IDtypeseacraft, Nametypeseacraft) VALUES(5, 'test');
UPDATE tb_typeseacraft SET Nametypeseacraft='tesssst' WHERE IDtypeseacraft=5;
DELETE FROM tb_typeseacraft WHERE IDtypeseacraft=5;

SELECT NameSeacraft FROM vw_seacrafts;
UPDATE vw_seacrafts SET NameSeacraft='titannic' WHERE idseacraft=1;
UPDATE tb_seacrafts SET NameSeacraft='titannic' WHERE idseacraft=1;
--
REVOKE ALL ON DATABASE db_port from test;
DROP ROLE test;


REVOKE ALL ON DATABASE db_port from update_vw_test;
DROP ROLE update_vw_test;



