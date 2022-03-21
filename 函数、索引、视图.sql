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



		