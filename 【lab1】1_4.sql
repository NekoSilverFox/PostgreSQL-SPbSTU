-------------------------------- 触发器 --------------------------------
-- 添加新记录时，船舶的到达码头的时间不得早于该船舶在系统中记录的最晚离开时间（也就是说，必须离开一个码头才能到达新的码头）

-- Время отправления корабля не может быть меньше времени прибытия
-- При добавлении новой записи время прибытия корабля в порт не должно быть раньше, чем последнее время отправления, зарегистрированное для корабля в системе (т.е. оно должно покинуть порт, чтобы прибыть на новый порт).
CREATE OR REPLACE FUNCTION fc_TimeChecker() RETURNS TRIGGER
	AS $tr_TimeChecker$
	BEGIN
		CASE
		WHEN TG_OP = 'INSERT' THEN
			-- 系统中无记录，即为首条记录
			IF ((SELECT COUNT(*) FROM tb_arrivals WHERE SeacraftID=NEW.SeacraftID) = 0)
			THEN
			
				IF ((NEW.LeaveTime IS NOT NULL) AND (NEW.ArrivalTime::TIMESTAMP > NEW.LeaveTime::TIMESTAMP)) THEN
					raise notice '[ERROR-1] The previous record is incomplete';
					RETURN NULL;
				END IF;
				
			END IF;
		
			-- 不是首条记录
			-- 与上条记录做对比
			IF (((SELECT LeaveTime::TIMESTAMP 
							FROM tb_arrivals 
							WHERE SeacraftID=NEW.SeacraftID
							ORDER BY LeaveTime DESC
							LIMIT 1) IS NULL)
					OR
					((SELECT LeaveTime::TIMESTAMP 
							FROM tb_arrivals 
							WHERE SeacraftID=NEW.SeacraftID
							ORDER BY LeaveTime DESC
							LIMIT 1) > NEW.ArrivalTime::TIMESTAMP)) THEN
					raise notice '[ERROR-2] Time conflict, unable to add this record';
					RETURN NULL;
			END IF;
			
			-- 再与自身作对比
			IF ((NEW.LeaveTime IS NOT NULL) AND (NEW.ArrivalTime::TIMESTAMP > NEW.LeaveTime::TIMESTAMP)) THEN
				raise notice '[ERROR-3] The leave time cannot be less than the arrival time';
				RETURN NULL;
			END IF;
	

		WHEN TG_OP = 'UPDATE' THEN
			IF ((NEW.LeaveTime IS NOT NULL) AND (NEW.ArrivalTime::TIMESTAMP > NEW.LeaveTime::TIMESTAMP)) THEN
				raise notice '[ERROR-4] The leave time cannot be less than the arrival time';
				RETURN NULL;
			END IF;
		END CASE;
	
 	RETURN NEW;
	END
	$tr_TimeChecker$ LANGUAGE plpgsql;

--
CREATE OR REPLACE TRIGGER tr_TimeChecker
	BEFORE INSERT OR UPDATE ON tb_arrivals
	FOR EACH ROW EXECUTE FUNCTION fc_TimeChecker();


------------
SELECT * FROM tb_arrivals WHERE IDArrival=2000;
INSERT INTO tb_Arrivals (idarrival, PortID, SeacraftID, Purpose, ArrivalTime, LeaveTime) VALUES (2000, 10, 17, NULL, '2022-02-04 10:23:01', '2022-05-26 00:10:27');
UPDATE tb_arrivals SET LeaveTime='2022-05-26 00:10:26' WHERE IDArrival=2000;
DELETE FROM tb_arrivals WHERE idarrival=2000;



