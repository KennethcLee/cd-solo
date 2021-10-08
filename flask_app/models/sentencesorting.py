from google.cloud import translate
import os
from google.oauth2 import service_account
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.login import Logins

class SentenceSorting:
    def __init__(self, data):
        self.id=data['id']
        self.num_element=data['num_element']
        self.game_data=data['game_data']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def get_game_data(cls, data):
        print('***  9000  ***', data)
        query = "SELECT sentence_sorting_data.id, num_element, game_data, sentence_sorting_data.created_at, sentence_sorting_data.updated_at FROM sentence_sorting_data JOIN game_level_sentence_sorting_data ON game_level_sentence_sorting_data.id = sentence_sorting_data.id JOIN game_level ON game_level_sentence_sorting_data.game_level_id = game_level.id WHERE game_level.level = %(level)s AND game_type=%(game_type)s ORDER BY RAND() LIMIT 10"
        result = []
        questions = connectToMySQL('games').query_db(query, data)
        print('***  9000A  ***', query)
        print('***  9000B  ***', questions)
        for j in questions:
            print('***  9000J  ***', j['game_data'])
            j['game_data'] = SentenceSorting.translate_text(j['game_data'])
            result.append(cls(j))
        print('***  9000D  ***', result)
        return result

    @staticmethod
    def translate_text(text, project_id="celtic-shape-328321"):
        print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])
        # credentials = service_account.Credentials.from_service_account_file("/credentials.json")
        # credentials = service_account.Credentials.from_service_account_file()

        client = translate.TranslationServiceClient()

        location = "global"

        parent = f"projects/{project_id}/locations/{location}"

        # Detail on supported types can be found here:
        # https://cloud.google.com/translate/docs/supported-formats
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "mime_type": "text/plain",  # mime types: text/plain, text/html
                "source_language_code": "en-US",
                "target_language_code": "fr",
            }
        )

        # Display the translation for each input text provided
        for translation in response.translations:
            print("*** 20000 *** Translated text: {}".format(translation.translated_text))