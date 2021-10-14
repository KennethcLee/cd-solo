#Python
pipenv install flask PyMySql cryptography flask-bcrypt jsonify 
(Deprecated: nltk textblob)

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
SELECT * FROM users JOIN scores on users.id = scores.user_id JOIN game_level on scores.game_level_id = game_level.id WHERE game_type = 'sentencesorting' ORDER BY score DESC LIMIT 10;
SELECT id FROM game_level WHERE game_type ='sentencesorting' AND level = 1;

SELECT * FROM game_level;
SELECT * FROM game_level WHERE game_type = 'addition' AND level = 2;
SELECT max_int, max_line FROM game_level WHERE game_type = 'addition' AND level = 2;
SELECT * FROM game_level WHERE game_type = 'addition' ORDER BY level;

ALTER TABLE game_level MODIFY COLUMN game_type
ENUM('addition','sentencesorting');

SELECT * FROM sentence_sorting_data;

SELECT * FROM game_level_sentence_sorting_data;
SELECT sentence_sorting_data.id, num_element, game_data, sentence_sorting_data.created_at, sentence_sorting_data.updated_at FROM sentence_sorting_data 
JOIN game_level_sentence_sorting_data 
ON game_level_sentence_sorting_data.id = sentence_sorting_data.id
JOIN game_level
ON game_level_sentence_sorting_data.game_level_id = game_level.id
WHERE game_level.level = 1
AND game_type='sentencesorting'
ORDER BY RAND()
LIMIT 10;

DELETE FROM scores;
DELETE FROM sentence_sorting_data;
DELETE FROM game_level_sentence_sorting_data;

INSERT INTO scores(user_id, game_level_id, score, question_total, question_correct, created_at, updated_at) VALUES
	(1, (SELECT id FROM game_level WHERE game_type ='sentencesorting' AND level = 1), 10, 10, 1, now(), now());

INSERT INTO scores(user_id, game_level_id, score, question_total, question_correct, created_at, updated_at) VALUES
	(1, 1, 10, 10, 1, now(), now()),
    (1, 1, 60, 10, 6, now(), now()),
	(1, 2, 40, 10, 4, now(), now()),
    (1, 2, 20, 10, 2, now(), now());
    
INSERT INTO game_level(game_type, game_name, level, min_element, max_element, min_line, max_line, max_question, score_question, created_at, updated_at) VALUES
	(1, 'Addition', 1, 1, 1, 2, 2, 10, 10, now(), now()),
	(1, 'Addition', 2, 1, 2, 3, 3, 10, 15, now(), now()),
    (1, 'Addition', 3, 2, 2, 4, 4, 10, 20, now(), now()),
    (1, 'Addition', 4, 2, 3, 2, 2, 10, 25, now(), now()),
    (1, 'Addition', 5, 3, 3, 3, 3, 10, 30, now(), now()),
    (1, 'Addition', 6, 2, 4, 4, 4, 10, 35, now(), now()),
    (1, 'Addition', 7, 3, 4, 2, 2, 10, 40, now(), now()),
    (1, 'Addition', 8, 4, 4, 3, 3, 10, 45, now(), now()),
    (1, 'Addition', 9, 2, 5, 4, 4, 10, 50, now(), now()),
    (1, 'Addition', 10, 3, 5, 2, 2, 10, 55, now(), now());

INSERT INTO game_level(game_type, game_name, level, min_element, max_element, min_line, max_line, max_question, score_question, created_at, updated_at) VALUES
	(2, 'Sentence Sorting', 1, 3, 3, 1, 1, 10, 10, now(), now()),
	(2, 'Sentence Sorting', 2, 3, 4, 1, 1, 10, 15, now(), now()),
    (2, 'Sentence Sorting', 3, 4, 5, 1, 1, 10, 20, now(), now()),
    (2, 'Sentence Sorting', 4, 5, 6, 1, 1, 10, 25, now(), now()),
    (2, 'Sentence Sorting', 5, 6, 7, 1, 1, 10, 30, now(), now()),
    (2, 'Sentence Sorting', 6, 7, 8, 1, 1, 10, 35, now(), now()),
    (2, 'Sentence Sorting', 7, 8, 9, 1, 1, 10, 40, now(), now()),
    (2, 'Sentence Sorting', 8, 9, 10, 2, 2, 10, 45, now(), now()),
    (2, 'Sentence Sorting', 9, 3, 3, 2, 2, 10, 50, now(), now()),
    (2, 'Sentence Sorting', 10, 3, 4, 2, 2, 10, 55, now(), now());
    
    
INSERT INTO sentence_sorting_data(num_element, game_data, created_at, updated_at) VALUES
	(3, 'I can read.', now(), now()),
	(3, 'You can read.', now(), now()),
	(3, 'I can count.', now(), now()),
	(3, 'She can eat.', now(), now()),
	(3, 'Do you play?', now(), now()),
	(3, 'He can listen.', now(), now()),
    (3, 'Dog ate homework.', now(), now()),
	(3, 'Cat sleeps late.', now(), now()),
	(3, 'Parrot flies fast.', now(), now()),
   	(3, 'You can color.', now(), now()),
	(3, 'He threw balls.', now(), now());
    
INSERT INTO game_level_sentence_sorting_data(game_level_id, sentence_sorting_data_id, created_at, updated_at) VALUES
	(11, 1, now(), now()),
	(11, 2, now(), now()),
    (11, 3, now(), now()),
    (11, 4, now(), now()),
    (11, 5, now(), now()),
    (11, 6, now(), now()),
    (11, 7, now(), now()),
    (11, 8, now(), now()),
    (11, 9, now(), now()),
    (11, 10, now(), now()),
    (11, 11, now(), now());


#google Cloud
https://codelabs.developers.google.com/codelabs/cloud-translation-python3#1
https://cloud.google.com/translate/docs/reference/libraries/v3/python


https://console.cloud.google.com/home/dashboard

gcloud services enable translate.googleapis.com

pip install --upgrade google-cloud-translate
pip install googletrans==3.1.0a0

Create Service Account
https://console.cloud.google.com/iam-admin/serviceaccounts/create

Role: Cloud Translation

https://console.cloud.google.com/iam-admin/serviceaccounts/details/

Create Key:
https://console.cloud.google.com/iam-admin/serviceaccounts/detail

Google translge Language:
https://cloud.google.com/translate/docs/languages

#Microsoft Azure Translate
Setup Azure account
Login to portal:
https://portal.azure.com/#home

Create the tranlate service
Use API service code:
https://docs.microsoft.com/en-us/azure/cognitive-services/translator/quickstart-translator?WT.mc_id=Portal-Microsoft_Azure_ProjectOxford&tabs=python

Copy Key from site
