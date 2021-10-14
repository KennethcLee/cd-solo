import requests, uuid, json
from google.oauth2 import service_account
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.login import Logins
# from google.cloud import translate
# from googletrans import Translator
# import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from textblob import TextBlob

class SentenceSorting:
    def __init__(self, data):
        self.id=data['id']
        self.num_element=data['num_element']
        self.game_data=data['game_data']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

    @classmethod
    def get_game_data(cls, data, src_lang, dest_lang):
        query = "SELECT sentence_sorting_data.id, num_element, game_data, sentence_sorting_data.created_at, sentence_sorting_data.updated_at FROM sentence_sorting_data JOIN game_level_sentence_sorting_data ON game_level_sentence_sorting_data.id = sentence_sorting_data.id JOIN game_level ON game_level_sentence_sorting_data.game_level_id = game_level.id WHERE game_level.level = %(level)s AND game_type=%(game_type)s ORDER BY RAND() LIMIT 1"
        result = []
        questions = connectToMySQL('games').query_db(query, data)
        print('***  9000A  ***', query)
        print('***  9000B  ***', questions)
        for j in questions:
            print('***  9000J  ***', j['game_data'])
            #Google Language translate:  Takes too long j['game_data'] = SentenceSorting.translate_text(j['game_data'])
            if src_lang != dest_lang:
                j['game_data'] = SentenceSorting.translate_text(j['game_data'], src_lang, dest_lang)
            print('***  9000C  ***', j['game_data'])
            result.append(cls(j))
        return result

    @staticmethod
    def translate_text(text, src_lang, dest_lang):
        # Add your subscription key and endpoint
        with open ("./flask_app/static/files/microsoft.key", "r") as myfile:
            #Read Subscription from file and remove the newline \n from end of line
            subscription_key=(myfile.read()).strip()
        # print('***  20000A  ***', subscription_key, type(subscription_key))

        endpoint = "https://api.cognitive.microsofttranslator.com"

        # Add your location, also known as region. The default is global.
        # This is required if using a Cognitive Services resource.
        location = "westus2"

        path = '/translate'
        constructed_url = endpoint + path

        params = {
            'api-version': '3.0',
            'from': src_lang,
            'to': [dest_lang]
        }
        constructed_url = endpoint + path

        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json',
            'X-ClientTraceId': str(uuid.uuid4())
        }

        # You can pass more than one object in body.
        body = [{
            'text': text
        }]

        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        print('***  20000B  ***', response[0]['translations'][0]['text'])
        print('***  20000C  ***')
        # print(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
        return response[0]['translations'][0]['text']

    # @staticmethod
    # def translate_text(text, src_lang, dest_lang):
    #     translator = Translator()
    #     result = translator.translate(text,src=src_lang, dest=dest_lang)
    #     result = result.text
    #     return result

    #Google Translator (Too Slow)
    # @staticmethod
    # def translate_text(text, project_id="celtic-shape-328321"):

    #     credentials = service_account.Credentials.from_service_account_file("./flask_app/static/files/credentials.json")
    #     print('***  20000C  ***', credentials, text)
    #     client = translate.TranslationServiceClient(credentials=credentials)

    #     location = "global"

    #     parent = f"projects/{project_id}/locations/{location}"

    #     # Detail on supported types can be found here:
    #     # https://cloud.google.com/translate/docs/supported-formats
    #     response = client.translate_text(
    #         request={
    #             "parent": parent,
    #             "contents": [text],
    #             "mime_type": "text/plain",  # mime types: text/plain, text/html
    #             "source_language_code": "en-US",
    #             "target_language_code": "zh",
    #         }
    #     )

    #     # Display the translation for each input text provided
    #     result = ''
    #     for translation in response.translations:
    #         result+= "{}".format(translation.translated_text)
    #         print("*** 20000S ***", result)
    #         print("*** 20000W ***", "{}".format(translation.translated_text))
    #     return result