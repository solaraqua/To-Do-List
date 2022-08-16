DELIMITER //
DROP PROCEDURE IF EXISTS "deleteToDo" //

CREATE PROCEDURE deleteToDo(IN users VARCHAR(500), IN iD int)
begin
  DELETE FROM toDoList
  WHERE iD = id AND users = username;
end//
DELIMITER ;
