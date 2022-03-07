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
	GrageID							INTEGER				NOT NULL		-- Категория 类别
);

-- Категория 港口类别
DROP TABLE IF EXISTS tb_PortGrage;
CREATE TABLE IF NOT EXISTS tb_PortGrage
(
	IDGrade							SERIAL,
	NameGrade						VARCHAR(255)	NOT NULL
);

-- Тип корабли
DROP TABLE IF EXISTS tb_TypeSeacraft;
CREATE TABLE IF NOT EXISTS tb_TypeSeacraft
(
	IDTypeSeacraft			SERIAL,
	TypeName						VARCHAR(255)	NOT NULL
);

-- Информации Капитана 船长信息
DROP TABLE IF EXISTS tb_Captain;
CREATE TABLE IF NOT EXISTS tb_Captain
(
	IDCaptain						SERIAL,
	NameCaptain					VARCHAR(255)	NOT NULL,
	Birthday						DATE					NOT NULL,
	Telephone						VARCHAR(18)		NOT NULL
);