CREATE ROLE manager;

GRANT SELECT, INSERT, UPDATE ON TABLE book TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE book_awards TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE awards TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE book_genre TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE genre TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE book_series TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE series TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE book_publisher TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE publisher TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE book_author TO manager;
GRANT SELECT, INSERT, UPDATE ON TABLE author TO manager;

DO $$ 
DECLARE 
    user_record RECORD;
BEGIN
    FOR user_record IN (SELECT username FROM users WHERE user_type = 'manager') 
    LOOP
        EXECUTE format('GRANT manager TO %I;', user_record.username);
    END LOOP;
END $$;
