#Python
pipenv install flask PyMySql cryptography flask-bcrypt

pipenv --venv

pipenv graph

pipenv shell

python3 server.py

#SQL
USE games;
SET SQL_SAFE_UPDATES = 0;

SELECT * FROM users;

SELECT * FROM scores;
SELECT * FROM users JOIN scores on users.id = scores.user_id JOIN game_level on scores.game_level_id = game_level.id;
SELECT * FROM users JOIN scores on users.id = scores.user_id JOIN game_level on scores.game_level_id = game_level.id WHERE game_type = 'addition' ORDER BY score DESC LIMIT 10;

SELECT * FROM game_level;
SELECT * FROM game_level WHERE game_type = 'addition' AND level = 2;
SELECT max_int, max_line FROM game_level WHERE game_type = 'addition' AND level = 2;

DELETE FROM scores;

INSERT INTO scores(user_id, game_level_id, score, question_total, question_correct, datetime, created_at, updated_at) VALUES
	(1, 1, 10, 10, 1, '2021-08-01 12:00:00', now(), now()),
    (1, 1, 60, 10, 6, '2021-08-12 14:00:00', now(), now()),
	(1, 2, 40, 10, 4, '2021-09-02 02:00:00', now(), now()),
    (1, 2, 20, 10, 2, '2021-09-14 19:00:00', now(), now());

INSERT INTO game_level(game_type, level, min_digit, max_digit, min_line, max_line, max_question, score_question, created_at, updated_at) VALUES
	(1, 1, 1, 1, 2, 2, 10, 10, now(), now()),
	(1, 2, 1, 2, 3, 3, 10, 15, now(), now()),
    (1, 3, 2, 2, 4, 4, 10, 20, now(), now()),
    (1, 4, 2, 3, 2, 2, 10, 25, now(), now()),
    (1, 5, 3, 3, 3, 3, 10, 30, now(), now()),
    (1, 6, 2, 4, 4, 4, 10, 35, now(), now()),
    (1, 7, 3, 4, 2, 2, 10, 40, now(), now()),
    (1, 8, 4, 4, 3, 3, 10, 45, now(), now()),
    (1, 9, 2, 5, 4, 4, 10, 50, now(), now()),
    (1, 10, 3, 5, 2, 2, 10, 55, now(), now());