DROP PROCEDURE IF EXISTS GetHistory;
DELIMITER $$
CREATE PROCEDURE GetHistory (
	IN  playerID INT
)
BEGIN
	SELECT game_gameinfo.gameID, game_gameinfo.playerID, 
	game_gameinfo.team, game_game.redScore, game_game.blueScore, 
    game_game.date, 
    IF((game_gameinfo.team = 0 AND game_game.redScore > game_game.blueScore) OR 
       (game_gameinfo.team = 1 AND game_game.redScore < game_game.blueScore),0,
      IF (game_game.redScore = game_game.blueScore,1,2)) as "result"
    FROM `game_gameinfo` 
    INNER JOIN `game_game` ON (`game_gameinfo`.`gameID` = `game_game`.`id`)
    WHERE `game_gameinfo`.`playerID` = playerID
    ORDER BY `game_game`.`id` DESC
    LIMIT 100;
END$$
