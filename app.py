from __future__ import unicode_literals
import json
import logging
from flask import Flask, request
import requests

import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="marusya-made-12e4432bff10.json"

app = Flask(__name__)
app.debug = True

def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        print('Detected intent: {} (confidence: {})\n'.format(
            response.query_result.intent.display_name,
            response.query_result.intent_detection_confidence))
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))
        return {'Query text': response.query_result.query_text,
                'Detected intent': response.query_result.intent.display_name,
                'Fulfillment text': response.query_result.fulfillment_text}

def get_intent(text):
    answer = detect_intent_texts('marusya-made', 7777777, [text], 'ru')
    return answer['Detected intent']

@app.route('/')
def index():
    return '<h1>На главной ничего нет</h1> <h5>вебхук для запросов: https://what-about-the-virus.herokuapp.com/mrs</h5>'

@app.route('/mrs', methods=['POST'])
def main():

    card = {}
    buttons = []
    end_session = False
    text = ''

    if request.json['session']['new']:
        text = 'Привет! Меня зовут Алиса. Я могу дать текущую сводку по \
                коронавирусу в разрезе стран или городов. \
                Вы можете ознакомиться с примерами команд или начать спрашивать)'
        # Потом раскоментить картинку!!!!!!!!
        # card = {
        #         'type': 'BigImage',
        #         'image_id': 457239017,
        #         'title': '',
        #         'description': ''
        #         }

        buttons = [
                    {'title': 'Примеры'},
                    {'title': 'Не надо примеров'}
                  ]

    elif request.json['request']['command'] == 'примеры':
        text = '1. Какая ситуация в мире? Что в мире?\n \
                2. Сводка по России. Ситуация в нашей стране\n \
                3. Статистика в Москве. Ситуация в Монголии.\n \
                4. Сравни показатели России и Бразилии.\n \
                5. Какие симптомы? Симптомы\n \
                6. Где найти советы по вирусу? Советы.'

    elif request.json['request']['command'] == 'не надо примеров':
        text = 'Хорошо, тогда слушаю вас)) \n (＾▽＾)'

    elif get_intent(request.json['request']['command']) == 'world request':
        try:
            res = requests.get('https://covid-api.com/api/reports/total')
            data = res.json()['data']

            text = 'СВОДКА ПО МИРУ \n\
                    Актуально на {d}\n\
                    Заражения: {z}\n\
                    Смерти: {de}\n\
                    Смертность: {s}%\n\
                    Выздоровления: {v}'.format(d=data['date'],
                                               z='{0:,}'.format(data['confirmed']).replace(',', ' '),
                                               de='{0:,}'.format(data['deaths']).replace(',', ' '),
                                               s=round(data['fatality_rate']*100,2),
                                               v='{0:,}'.format(data['recovered']).replace(',', ' '))
        except:
            text = 'Кажется, не только вам сейчас интересна статистика по миру. \
                    Не удается загрузить данные.\n\
                    Простите, может сработают другие команды.'

    elif request.json['request']['command'] == 'on_interrupt':
        text = 'Всего доброго! Берегите себя и близких!'

    response = {
    'version': request.json['version'],
    'session': request.json['session'],
    'response': {
        'end_session': end_session,
        'text': text,
        'card': card,
        'buttons': buttons
        }
    }

    logging.info('Response: %r', response)

    return json.dumps(response, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    app.run()


# @app.route('/mrs', methods=['POST'])
# def main():
#
#     card = {}
#     buttons = []
#     end_session = False
#     text = ''
#
#     if request.json['session']['new']:
#         text = 'Привет! Это еще тестовый навык.'
#     elif request.json['request']['command'].lower() == 'привет':
#         text = 'Привет!!!'
#     elif request.json['request']['command'].lower() == 'хватит':
#         text = 'Хорошо, до встречи!'
#         end_session = True
#     elif request.json['request']['command'] == 'on_interrupt':
#         text = 'Приходи еще.'
#     elif request.json['request']['command'].lower() == 'картинка':
#         text = 'Вот такая есть картинка:'
#         card = {
#             'type': 'BigImage',
#             'image_id': 457239018,
#             'title': 'Это Коржик — офисный пёс',
#             'description': 'текст'
#                 }
#     elif request.json['request']['command'].lower() == 'кнопки':
#         text = 'Вот такие есть кнопки:'
#         buttons = [
#                     {'title': 'кнопка 1'},
#                     {'title': 'кнопка 2'}
#                   ]
#     elif request.json['request']['command'].lower() == 'карусель':
#         text = 'Карусель:'
#         card = {
#             "type": "ItemsList",
#             # "title": "Две картинки",
#             # "description": "текст",
#             "items": [{"image_id": 457239018}, {"image_id": 457239017}, {"image_id": 457239019}]
#                 }
#     else:
#         text = request.json['request']['command'].lower()
#
#     response = {
#     'version': request.json['version'],
#     'session': request.json['session'],
#     'response': {
#         'end_session': end_session,
#         'text': text,
#         'card': card,
#         'buttons': buttons
#         }
#     }
#
#     logging.info('Response: %r', response)
#
#     return json.dumps(response, ensure_ascii=False, indent=2)
