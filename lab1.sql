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