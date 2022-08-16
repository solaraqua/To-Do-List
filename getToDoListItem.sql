DELIMITER //
DROP PROCEDURE IF EXISTS getToDoListItem //

CREATE PROCEDURE getToDoListItem(IN users VARCHAR(500), IN iD int)
BEGIN
  SELECT *
    FROM toDoList WHERE users = username AND iD = id;
END //
DELIMITER ;
