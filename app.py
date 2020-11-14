from __future__ import unicode_literals
import json
import logging
from flask import Flask, request

app = Flask(__name__)
app.debug = True

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
        card = {
                'type': 'BigImage',
                'image_id': 457239017,
                'title': '',
                'description': ''
                }

        buttons = [
                    {'title': 'Примеры'},
                    {'title': 'Не надо примеров'}
                  ]

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
