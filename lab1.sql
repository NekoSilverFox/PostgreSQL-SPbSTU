-- IF EXISTS(SELECT * FROM pg_catalog.pg_database u WHERE u.datname='db_Port')
	
-- 创建数据库
DROP DATABASE IF EXISTS db_Port;
CREATE DATABASE db_Port
WITH
  OWNER = "fox"
  TABLESPACE = "pg_default"
;



--------------------------------- 创建表 ---------------------------------
-- Корабль
DROP TABLE IF EXISTS tb_Seacrafts;
CREATE TABLE IF NOT EXISTS tb_Seacrafts
(
	IDSercraft					SERIAL,
	NameSeacraft				VARCHAR(255)	NOT NULL,		-- Название
	Displacement				INTEGER 			NOT NULL,		-- Водоизменение 排水量
	RegistrationPortID	INTEGER				NOT NULL,		-- Порт приписки 船舶注册港
	TypeID							INTEGER				NOT NULL,		-- Тип
	CaptainID						INTEGER				NOT NULL		-- Капитан
);

-- Посещение
DROP TABLE IF EXISTS tb_Arrivals;
CREATE TABLE IF NOT EXISTS tb_Arrivals
(
	IDArrival						SERIAL,
	PortID							INTEGER			NOT NULL,		-- № причала 港口ID
	SeacraftID					INTEGER			NOT NULL,		
	Purpose							TEXT				NULL,		 		-- Цель посещения 目的
	ArrivalTime					TIMESTAMP		NOT NULL,		-- Дата прибытия 到达日
	DepartureTime				TIMESTAMP		NOT NULL 		-- Дата убытия 离开日期
);

-- Порт
DROP TABLE IF EXISTS tb_Ports;
CREATE TABLE IF NOT EXISTS tb_Ports
(
	IDPort							SERIAL,
	Country							VARCHAR(255)	NOT NULL,		-- Страна
	NamePort						VARCHAR(255)	NOT NULL,		-- Название
	Price								INTEGER				NOT NULL,		-- Цена 1-ого для пребывания
	LevelID							INTEGER				NOT NULL		-- Категория 类别
);

-- Категория 港口类别
DROP TABLE IF EXISTS tb_PortLevels;
CREATE TABLE IF NOT EXISTS tb_PortLevels
(
	IDLevel							SERIAL,
	NameLevel						VARCHAR(255)	NOT NULL
);

-- Тип корабли
DROP TABLE IF EXISTS tb_TypeSeacraft;
CREATE TABLE IF NOT EXISTS tb_TypeSeacraft
(
	IDTypeSeacraft			SERIAL,
	TypeName						VARCHAR(255)	NOT NULL
);

-- Информации Капитана 船长信息
DROP TABLE IF EXISTS tb_Captains;
CREATE TABLE IF NOT EXISTS tb_Captains
(
	IDCaptain						SERIAL,
	NameCaptain					VARCHAR(255)	NOT NULL,
	Birthday						DATE					NOT NULL,
	Telephone						VARCHAR(18)		NOT NULL
);

--------------------------------- 约束 ---------------------------------
ALTER TABLE tb_TypeSeacraft ADD CONSTRAINT PK_TypeSeacraft_IDTypeSeacraft PRIMARY KEY(IDTypeSeacraft);
ALTER TABLE tb_TypeSeacraft ADD CONSTRAINT UQ_TypeSeacraft_TypeName 			UNIQUE(TypeName);


ALTER TABLE tb_Captains ADD CONSTRAINT PK_Captain_IDCaptain PRIMARY KEY(IDCaptain);
ALTER TABLE tb_Captains ADD CONSTRAINT UQ_Captain_Telephone UNIQUE(Telephone);


ALTER TABLE tb_PortLevels ADD CONSTRAINT PK_PortGrage_IDLevel 		PRIMARY KEY(IDLevel);
ALTER TABLE tb_PortLevels ADD CONSTRAINT UQ_PortGrage_NameLevel	UNIQUE(NameLevel);


ALTER TABLE tb_Ports ADD CONSTRAINT PK_Ports_IDPort		PRIMARY KEY(IDPort);
ALTER TABLE tb_Ports ADD CONSTRAINT UQ_Ports_NamePort	UNIQUE(NamePort);
ALTER TABLE tb_Ports ADD CONSTRAINT CK_Ports_Price		CHECK(Price > 0);
ALTER TABLE tb_Ports ADD CONSTRAINT FK_Ports_LevelID	FOREIGN KEY(LevelID) REFERENCES tb_PortLevels(IDLevel);


ALTER TABLE tb_Seacrafts ADD CONSTRAINT PK_Seacrafts_IDSercraft 				PRIMARY KEY(IDSercraft);
ALTER TABLE tb_Seacrafts ADD CONSTRAINT FK_Seacrafts_RegistrationPortID FOREIGN KEY(RegistrationPortID) REFERENCES tb_Ports(IDPort);
ALTER TABLE tb_Seacrafts ADD CONSTRAINT FK_Seacrafts_TypeID 						FOREIGN KEY(TypeID)							REFERENCES tb_TypeSeacraft(IDTypeSeacraft);
ALTER TABLE tb_Seacrafts ADD CONSTRAINT FK_Seacrafts_CaptainID 					FOREIGN KEY(CaptainID) 					REFERENCES tb_Captains(IDCaptain);


ALTER TABLE tb_Arrivals ADD CONSTRAINT 	PK_Arrivals_IDArrival				PRIMARY KEY(IDArrival);
ALTER TABLE tb_Arrivals ADD CONSTRAINT 	FK_Arrivals_PortID					FOREIGN KEY(PortID)			REFERENCES tb_Ports(IDPort);
ALTER TABLE tb_Arrivals ADD CONSTRAINT 	FK_Arrivals_SeacraftID			FOREIGN KEY(SeacraftID)	REFERENCES tb_Seacrafts(IDSercraft);
ALTER TABLE tb_Arrivals ALTER 					ArrivalTime 								SET DEFAULT now();
ALTER TABLE tb_Arrivals ALTER 					DepartureTime								SET DEFAULT now();


--------------------------------- 插入数据 ---------------------------------
INSERT INTO tb_TypeSeacraft(TypeName) VALUES('Container ship');	-- Контейнеровоз 集装箱船
INSERT INTO tb_TypeSeacraft(TypeName) VALUES('Bulk carrier');		-- Балкер 散货船
INSERT INTO tb_TypeSeacraft(TypeName) VALUES('Oil tanker');			-- Нефтяной танкер 油船
INSERT INTO tb_TypeSeacraft(TypeName) VALUES('LNG carrier');		-- Газово́з 液化气体船

INSERT INTO tb_PortLevels(NameLevel) VALUES('Commercial port');		-- Торговый порт 商港
INSERT INTO tb_PortLevels(NameLevel) VALUES('ndustrial port');		-- Промышленный порт 工业港
INSERT INTO tb_PortLevels(NameLevel) VALUES('Fishing port');			-- Рыболовные порты 渔港

INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Mark', '1991-04-09', '+ 8198-1005');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Tom', '1985-06-17', '+ 4188-3461');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Jurry', '1996-05-26', '+1 212-443-4383');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Judy', '1989-01-21', '+44 1223-80 7237');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Nick', '1980-01-12', '+44 7108 073718');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Wilde', '2003-07-13', '+86 150-7814-9979');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Hopps', '1982-12-06', '+86 28-555-5423');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Fisher', '1991-08-26', '+81 52-467-3540');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Lau', '1982-05-12', '+2 1426-1149');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Lee', '1977-11-24', '+2 2425-9688');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Kelly', '2001-01-20', '+81 90-2392-7844');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Perry', '1983-11-24', '+81 80-9044-2019');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Fisher', '1990-09-22', '+81 70-2684-4336');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Yeow', '1994-12-03', '+81 70-1870-8264');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Kwok', '1989-06-05', '+1 312-978-2188');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Pak', '1994-12-10', '+44 116-822 0722');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Tam', '1978-10-24', '+81 11-997-1390');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Stewart', '1989-05-24', '+86 174-1724-0195');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Wu', '1990-10-09', '+1 212-968-8315');
INSERT INTO tb_Captains(NameCaptain, Birthday, Telephone) VALUES('Chavez', '1981-09-23', '+81 52-449-9028');


INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Russia', 'ST.PETERSBURG', 5000, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Russia', 'kaliningrad', 5000, 2);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Russia', 'irkutsk', 7000, 3);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Russia', 'vostochny', 9100, 3);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('China', 'GuangDong', 3000, 2);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('China', 'HongKong', 6000, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('China', 'TsingDao', 90000, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('China', 'ShangHai', 8000, 2);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Azerbaijan', 'baku', 10000, 3);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('USA', 'chicago', 9500, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('USA', 'houston', 8300, 2);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('USA', 'boston', 8030, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('USA', 'new york', 2900, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('USA', 'los angeles', 7800, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Germany', 'bremen', 8900, 2);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Germany', 'cologne', 5800, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Germany', 'frankfurt', 6500, 3);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Germany', 'hamburg', 4500, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Germany', 'orth', 9100, 2);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Italy', 'catania', 6800, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Italy', 'bologna', 8600, 3);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Italy', 'massa', 6300, 3);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Italy', 'asti', 7000, 1);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Italy', 'ancona', 1900, 2);
INSERT INTO tb_Ports(Country, NamePort, Price, LevelID) VALUES('Italy', 'bari', 8700, 1);

INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Henry''s LLC', 550020, 19, 3, 6);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Marjorie Inc.', 290252, 9, 1, 13);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Russell LLC', 216511, 25, 3, 2);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Bradley Logistic Inc.', 640207, 3, 1, 20);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Russell Brothers Technology LLC', 548642, 24, 2, 11);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Louis LLC', 450401, 4, 3, 1);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('King''s Food LLC', 494573, 1, 4, 19);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Julie Network Systems LLC', 126310, 3, 1, 3);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Olson Trading Inc.', 361159, 19, 2, 19);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Ellis Inc.', 803539, 4, 4, 17);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Martha Food LLC', 881351, 14, 3, 2);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Reyes Brothers Technology LLC', 257989, 19, 1, 11);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Sharon Network Systems LLC', 151294, 2, 1, 20);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Harris Trading LLC', 502181, 6, 2, 17);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Chris Software LLC', 763727, 14, 4, 3);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Spencer Communications LLC', 879937, 4, 3, 15);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Thompson Toy LLC', 576609, 8, 4, 16);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Ernest Software LLC', 874330, 19, 3, 12);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Ryan LLC', 226851, 10, 4, 19);
INSERT INTO tb_Seacrafts (NameSeacraft, Displacement, RegistrationPortID, TypeID, Captainid) VALUES ('Harris''s Food Inc.', 440595, 17, 1, 6);

INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (24, 9, NULL, '2020-05-18 03:49:02', '2020-06-02 23:11:29');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (22, 11, NULL, '2020-03-08 17:54:40', '2020-09-08 07:24:17');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (22, 4, NULL, '2020-04-21 15:28:52', '2020-06-28 03:18:59');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (6, 3, NULL, '2020-03-09 10:10:08', '2020-08-04 21:08:54');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (6, 20, NULL, '2020-06-04 02:50:25', '2020-08-30 15:31:27');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (25, 11, NULL, '2020-04-10 18:30:13', '2020-09-04 23:48:04');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (19, 15, NULL, '2020-04-16 12:21:01', '2020-07-24 10:35:22');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (19, 7, NULL, '2020-04-04 08:14:54', '2020-06-16 18:41:37');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (7, 6, NULL, '2020-04-19 08:04:06', '2020-08-26 07:09:29');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (25, 4, NULL, '2020-03-29 19:49:01', '2020-08-27 04:52:24');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (4, 20, NULL, '2020-04-17 02:56:27', '2020-08-05 11:17:51');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (17, 15, NULL, '2020-05-01 14:38:42', '2020-06-09 09:31:54');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (3, 10, NULL, '2020-01-12 14:32:17', '2020-07-04 23:01:19');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (10, 13, NULL, '2020-02-12 14:31:04', '2020-09-07 10:39:49');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (9, 1, NULL, '2020-02-26 16:47:19', '2020-06-02 00:33:13');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (23, 14, NULL, '2020-06-06 05:15:37', '2020-09-05 14:12:02');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (16, 3, NULL, '2020-03-27 01:15:57', '2020-08-29 10:10:59');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (21, 10, NULL, '2020-01-08 22:30:44', '2020-06-14 12:16:34');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (5, 13, NULL, '2020-03-18 08:53:23', '2020-07-01 06:06:08');
INSERT INTO tb_Arrivals (PortID, SeacraftID, Purpose, ArrivalTime, DepartureTime) VALUES (19, 16, NULL, '2020-02-13 12:47:16', '2020-06-28 14:06:45');