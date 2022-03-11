
DROP FUNCTION fc_TimeChecker

CREATE FUNCTION fc_TimeChecker() RETURNS TRIGGER AS $tr_TimeChecker$
	BEGIN
		IF NEW.
	RETURN NEW;
	END;
$tr_TimeChecker$ LANGUAGE plpgsql;


CREATE TRIGGER tr_TimeChecker
	BEFORE INSERT OR UPDATE ON tb_arrivals
	FOR EACH ROW EXECUTE FUNCTION fc_TimeChecker();
