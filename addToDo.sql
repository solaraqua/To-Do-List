DELIMITER //
DROP PROCEDURE IF EXISTS "addToDo" //

CREATE PROCEDURE addToDo(IN toDo VARCHAR(1000), IN users VARCHAR(500))
begin
  INSERT INTO toDoList (username, toDoString, isDone) VALUES
	(users, toDo, false);
end//
DELIMITER ;
