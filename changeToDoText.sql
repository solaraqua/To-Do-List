DELIMITER //
DROP PROCEDURE IF EXISTS "changeToDoText" //

CREATE PROCEDURE changeToDoText(IN users VARCHAR(500), IN iD int, IN newtoDo VARCHAR(1000))
begin
  UPDATE toDoList
  SET toDoString = newtoDo WHERE iD = id AND users = username;
end//
DELIMITER ;
