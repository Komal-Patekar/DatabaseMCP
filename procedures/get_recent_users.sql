DELIMITER |
DROP PROCEDURE IF EXISTS get_recent_users;
CREATE PROCEDURE get_recent_users()
BEGIN
	select user from mysql.user where user not like '%mysql%' and user not like '%sys%';
END |
DELIMITER ;
