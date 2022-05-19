DROP DATABASE db_IMDB;

CREATE DATABASE db_IMDB
WITH
  OWNER = "fox"
  TABLESPACE = "pg_default"
;

--------------------------------------------------------------------------------
DROP TABLE tb_json;
CREATE TABLE tb_json (
	iddata						SERIAL,
	imdata 						JSON
);
CREATE INDEX IX_json_iddata ON tb_json(iddata);

COPY tb_json(imdata) FROM program 'sed -e ''s/\\/\\\\/g'' /Users/fox/Desktop/dump_ALL.json'; -- 49s
SELECT * FROM tb_json LIMIT 10;
SELECT COUNT(*) FROM tb_json;

SELECT imdata FROM tb_json WHERE imdata::json->>'name' = 'Richard Burton';
SELECT imdata->>'name' FROM tb_json WHERE imdata::json->>'name' = 'Richard Burton';
SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_json WHERE iddata=51989;  -- 170 Byte

BEGIN;
UPDATE tb_json SET imdata=jsonb_set(imdata::jsonb, '{name}', '"tttttttt"'::jsonb) WHERE iddata=1;

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{rols}', '[{"year": 2000, "title": "t_title", "series name": "t_series", "character name": "t_character_name"}]'::jsonb) WHERE iddata=1;

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{nconst}', '"tt0000009"'::jsonb) WHERE iddata=1;

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{birthYear}', '"2222"'::jsonb) WHERE iddata=1;

SELECT * FROM tb_jsonb WHERE iddata=1;
ROLLBACK;

--------------------------------------------------------------------------------
DROP TABLE tb_jsonb;
CREATE TABLE tb_jsonb (
	iddata						SERIAL,
	imdata 						JSONB
);
CREATE INDEX IX_jsonb_iddata ON tb_jsonb(iddata);

COPY tb_jsonb(imdata) FROM program 'sed -e ''s/\\/\\\\/g'' /Users/fox/Desktop/dump_ALL.json';  -- 79.32s
SELECT * FROM tb_jsonb;
SELECT COUNT(*) FROM tb_jsonb;

SELECT imdata FROM tb_jsonb WHERE imdata::jsonb->> 'name' = 'Richard Burton';
SELECT imdata FROM tb_jsonb WHERE imdata::jsonb->> 'nconst' = 'nm0000009';
SELECT imdata FROM tb_jsonb WHERE imdata::jsonb->'nconst' = '"nm0000009"';
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::jsonb->'nickname' = '"gs"';



BEGIN;
UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '"tttttttt"'::jsonb) WHERE iddata=1;

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{rols}', '[{"year": 2000, "title": "t_title", "series name": "t_series", "character name": "t_character_name"}]'::jsonb) WHERE iddata=1;

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{nconst}', '"tt0000009"'::jsonb) WHERE iddata=1;

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{birthYear}', '"2222"'::jsonb) WHERE iddata=1;

SELECT * FROM tb_jsonb WHERE iddata=1;
ROLLBACK;


select relname, relfilenode, reltoastrelid from pg_class where relname='tb_jsonb';
select count(*) from pg_toast.pg_toast_162078;
-------------------------------------------------------------------------------------------------------
BEGIN;
SELECT * FROM tb_jsonb WHERE iddata=51989;
SELECT pg_table_size('tb_jsonb');  -- 1108811776 Byte
SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1057 MB
SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=51989;  -- 202 Byte
SELECT SUM(size) FROM pg_ls_waldir(); -- 1056964608 Byte
SELECT pg_size_pretty(SUM(size)) FROM pg_ls_waldir(); -- 1008 MB

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '"Bf AAAAAAAAAAAAAAAAAAAAAAAAA"'::jsonb) WHERE iddata=51989;

SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=51989;  -- 230 Byte
SELECT pg_table_size('tb_jsonb');  -- 1108811776 Byte
SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1057 MB

ROLLBACK;
-------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------
BEGIN;
ALTER TABLE tb_jsonb ALTER imdata SET STORAGE EXTERNAL;
SELECT * FROM tb_jsonb WHERE iddata=51989;
SELECT pg_table_size('tb_jsonb');  -- 1108811776 Byte
SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1057 MB
SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=51989;  -- 202 Byte
SELECT SUM(size) FROM pg_ls_waldir(); -- 1056964608 Byte
SELECT pg_size_pretty(SUM(size)) FROM pg_ls_waldir(); -- 1008 MB

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '"Bf AAAAAAAAAAAAAAAAAAAAAAAAA"'::jsonb) WHERE iddata=51989;

SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=51989;  -- 230 Byte
SELECT pg_table_size('tb_jsonb');  -- 1108811776 Byte
SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1057 MB
SELECT SUM(size) FROM pg_ls_waldir(); -- 1056964608 Byte
SELECT pg_size_pretty(SUM(size)) FROM pg_ls_waldir(); -- 1008 MB
ROLLBACK;
-------------------------------------------------------------------------------------------------------


BEGIN;
SELECT pg_table_size('tb_jsonb');  -- 1108811776 Byte
SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1057 MB
SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=3789;  -- 4034997 Byte
SELECT SUM(size) FROM pg_ls_waldir(); -- 1056964608 Byte
SELECT pg_size_pretty(SUM(size)) FROM pg_ls_waldir(); -- 1008 MB

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '"David AAAAAAAAAAAAAAAAAAAAAAAAA"'::jsonb) WHERE iddata=3789;

SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=3789;  -- 4035007 [+10] Byte
SELECT pg_table_size('tb_jsonb');  -- 1112997888 Byte [+4186112 Byte]
SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1061 MB
SELECT SUM(size) FROM pg_ls_waldir(); -- 1056964608 Byte
SELECT pg_size_pretty(SUM(size)) FROM pg_ls_waldir(); -- 1008 MB
ROLLBACK;

-------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------

BEGIN;
ALTER TABLE tb_jsonb ALTER imdata SET STORAGE EXTERNAL;

SELECT pg_table_size('tb_jsonb');  -- 1117184000 Byte
SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1065 MB
SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=3789;  -- 4034997 Byte
SELECT SUM(size) FROM pg_ls_waldir(); -- 1056964608 Byte
SELECT pg_size_pretty(SUM(size)) FROM pg_ls_waldir(); -- 1008 MB

UPDATE tb_jsonb SET imdata=jsonb_set(imdata::jsonb, '{name}', '"David AAAAAAAAAAAAAAAAAAAAAAAAA"'::jsonb) WHERE iddata=3789;

SELECT iddata, pg_column_size(imdata) , imdata, imdata->>'{name}' FROM tb_jsonb WHERE iddata=3789;  -- 15845197 [+] Byte
SELECT pg_table_size('tb_jsonb');  -- 1133617152 [+16433152] Byte
SELECT pg_size_pretty(pg_table_size('tb_jsonb'));  -- 1081 MB [+ MB]
SELECT SUM(size) FROM pg_ls_waldir(); -- 1056964608 Byte
SELECT pg_size_pretty(SUM(size)) FROM pg_ls_waldir(); -- 1008 MB
ROLLBACK;

-------------------------------------------------------------------------------------------------------

SELECT * FROM tb_jsonb WHERE tb_jsonb.imdata::jsonb->> 'name' = 'Aditya';

--------------------------------------------------------------------------------
SELECT * 
	FROM tb_name_basics p
	WHERE any(string_to_array(p.knownfortitles, ','))='tt0050419'
	LIMIT 10 


SELECT nconst, primaryName, birthYear FROM tb_name_basics 
	WHERE to_json(nconst)::json->>'nconst' = 'nm9993261';

SELECT to_jsonb(nconst) FROM tb_name_basics Limit 10;

SELECT row_to_json(row(nconst, primaryName, birthYear)) FROM tb_name_basics Limit 10;

-- 构建 JSON 对象
SELECT jsonb_build_object('nconst', nconst,
												 'primaryName', primaryName,
												 'birthYear', birthYear,
												 'deathYear', deathYear) FROM tb_name_basics Limit 10;



SELECT json_build_object('nconst', nconst,
												 'primaryName', primaryName,
												 'birthYear', birthYear,
												 'deathYear', deathYear) as tb_json
	FROM tb_name_basics
	WHERE tb_json::json->> 'nconst' = 'nm9993261';
												 
												 
												 
select * from json_each('{"nconst":"nm9993261"}')

--------------------------------------------------------------------------------
	
	
	
	
	
--------------------------------------------------------------------------------
-- 简单标量/基本值
-- 基本值可以是数字、带引号的字符串、true、false或者null
SELECT '5'::json;

-- 有零个或者更多元素的数组（元素不需要为同一类型）
SELECT '[1, 2, "foo", null]'::json;

-- 包含键值对的对象
-- 注意对象键（key）必须总是带引号的字符串
SELECT '{"bar": "baz", "balance": 7.77, "active": false}'::json;

-- 数组和对象可以被任意嵌套
SELECT '{"foo": [true, "bar"], "tags": {"a": 1, "b": null}}'::json;

-- "->" 通过键获得 JSON 对象域 结果为json对象
select '{"nickname": "goodspeed", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::json->'nickname' as nickname;
"goodspeed"

-- "->>" 通过键获得 JSON 对象域 结果为text 
select '{"nickname": "goodspeed", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::json->>'nickname' as nickname;
goodspeed

-- 当一个 JSON 值被输入并且接着不做任何附加处理就输出时， json会输出和输入完全相同的文本，而jsonb 则不会保留语义上没有意义的细节
SELECT '{"bar": "baz", "balance": 7.77, "active":false}'::json;
{"bar": "baz", "balance": 7.77, "active":false}

-- jsonb 不会保留语义上的细节，key 的顺序也和原始数据不一致
SELECT '{"bar": "baz", "balance": 7.77, "active":false}'::jsonb;
{"bar": "baz", "active": false, "balance": 7.77}

-- nickname 为 gs 的用户 这里使用 ->> 查出的数据为text，所以匹配项也应该是text
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::json->>'nickname' = 'gs';
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::jsonb->>'nickname' = 'gs';

-- 使用 -> 查询，会抛出错误，这里无论匹配项是text类型的 'gs'  还是 json 类型的 '"gs"'::json都会抛出异常，json 类型不支持 等号（=）操作符
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::json->'nickname' = '"gs"';

-- json 类型不支持 "=" 操作符
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::json->'nickname' = '"gs"'::json;

-- jsonb 格式是可以查询成功的，这里使用 -> 查出的数据为json 对象，所以匹配项也应该是json 对象
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::jsonb->'nickname' = '"gs"';





-- #> 和 #>> 操作符
-- 使用 #> 查出的数据为json 对象
-- 使用 #>> 查出的数据为text
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::json#>'{tags,0}' as tag;
"python"

select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::json#>>'{tags,0}' as tag;
python

select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::jsonb#>'{tags,0}' = '"python"';
t

select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::jsonb#>>'{tags,0}' = 'python';
t

-- 会抛出错误，这里无论匹配项是text类型的 'python'  还是 json 类型的 '"python"'::json都会抛出异常，json 类型不支持 等号（=）操作符
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::json#>'{tags,0}' = '"python"';





jsonb 数据查询（不适用于json）
额外的jsonb操作符

-- nickname 为 gs 的用户
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::jsonb @> '{"nickname": "gs"}'::jsonb;

-- 等同于以下查询
-- 这里使用 -> 查出的数据为json 对象，所以匹配项也应该是json 对象
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::jsonb->'nickname' = '"gs"';
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::jsonb->>'nickname' = 'gs';

-- 查询有 python 和 golang 标签的数据
select '{"nickname": "gs", "avatar": "avatar_url", "tags": ["python", "golang", "db"]}'::jsonb @> '{"tags": ["python", "golang"]}';
 ?column?
----------
 t
 
 
 
 -- 更新 account content 字段（覆盖式更新）
update account set content = jsonb_set(content, '{}', '{"nickname": "gs", "tags": ["python", "golang", "db"]}', false);



insert into account select uuid_generate_v1(), ('{"nickname": "nn-' || round(random()*20000000) || '", "avatar": "avatar_url", "tags": ["python", "golang", "c"]}')::jsonb from (select * from generate_series(1,100000)) as tmp;




