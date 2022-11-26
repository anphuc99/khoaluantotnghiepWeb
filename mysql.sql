DROP PROCEDURE IF EXISTS GetHistory;
DELIMITER $$
CREATE PROCEDURE GetHistory (
	IN  playerID INT
)
BEGIN
	SELECT Game_gameinfo.gameID, Game_gameinfo.playerID, 
	Game_gameinfo.team, Game_game.redScore, Game_game.blueScore, 
    Game_game.date, 
    IF((Game_gameinfo.team = 0 AND Game_game.redScore > Game_game.blueScore) OR 
       (Game_gameinfo.team = 1 AND Game_game.redScore < Game_game.blueScore),0,
      IF (Game_game.redScore = Game_game.blueScore,1,2)) as "result"
    FROM `Game_gameinfo` 
    INNER JOIN `Game_game` ON (`Game_gameinfo`.`gameID` = `Game_game`.`id`)
    WHERE `Game_gameinfo`.`playerID` = playerID
    ORDER BY `Game_game`.`id` DESC
    LIMIT 100;
END$$
