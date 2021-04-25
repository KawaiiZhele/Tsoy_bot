from flask import Flask, request
import logging
from flask_ngrok import run_with_ngrok
import json
import random

app = Flask(__name__)
run_with_ngrok(app)
logging.basicConfig(level=logging.INFO)

sessionStorage = {}
photo_list = ['1030494/4fc61bbeb37a519efd34',
              '1652229/9526472bbb1f40a48b63',
              '1540737/2859fb7d5a0be64a94cb',
              '1540737/8c82f1161677f7530d8f',
              '965417/432fa96647ec67d62787',
              '1540737/19195841dffc064508a8',
              '997614/390ec4c113080220a21a']

missunderstand = ['Повторите, пожалуйста',
                  'Я вас немного не поняла',
                  'Можете, пожалуйста, перефразировать?',
                  'Боюсь, мы друг друга не поняли']

interesting_list = ['Первая гитара у Цоя появилась, когда он учился в 5-м классе.',
                    'Свою первую музыкальную группу Цой собрал в 8-м классе.',
                    'Первая песня была написана им в 18-летнем возрасте.',
                    'Любимый цвет Виктора Цоя — чёрный, любимые цветы — жёлтые розы.',
                    'Цой очень не любил зиму и вид крови.',
                    'Виктор хорошо владел английским языком.']


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response'][
            'text'] = 'Привет! Здесь ты можешь узнать много интересного о легендарном рокере Викторе Цое! Спроси у меня "Что ты умеешь?", и я покажу тебе все вопросы, которые ты можешь задать мне.'
        return

    if req['request']['original_utterance'].lower() in [
        'пока',
        'прекрати',
        'до скорой встречи',
        'до свидания'
    ]:
        res['response'][
            'text'] = 'Всего вам доброго, приятно было рассказать вам об этом великом музыканте!'
        return
    elif req['request']['original_utterance'].lower() in [
        'биография',
        'жизнь'
    ]:
        res['response'][
            'text'] = 'Вот вам биография Виктора Робертовича Цоя: https://ru.wikipedia.org/wiki/Цой,_Виктор_Робертович'
        return
    elif req['request']['original_utterance'].lower() in [
        'когда родился?',
        'день рождения'
    ]:
        res['response']['text'] = '21 июня 1962'
        return
    elif req['request']['original_utterance'].lower() in [
        'дата смерти',
        'когда умер?'
    ]:
        res['response']['text'] = '15 августа 1990'
        return
    elif req['request']['original_utterance'].lower() in [
        'фото',
        'фотография'
    ]:
        photo = random.choice(photo_list)
        res['response'] = {
            "text": f"Фотография Виктора Робертовича Цоя!",
            "card": {
                'type': "BigImage",
                "image_id": photo,
                'title': f"Фотография Виктора Робертовича Цоя!"
            }
        }
        return
    elif req['request']['original_utterance'].lower() in ['что ты умеешь?']:
        res['response']['text'] = 'Вы можете спросить у меня следующие вопросы:\n' \
                                  '-Биография / жизнь\n' \
                                  '-Песни\n' \
                                  '-Выступления\n' \
                                  "-Когда родился?\n" \
                                  "-Дата смерти\n" \
                                  "-Фото\n" \
                                  "-Интересные факты\n"
        return
    elif req['request']['original_utterance'].lower() in [
        'песни',
    ]:
        res['response']['text'] = 'Все песни Цоя только тут!: https://music.yandex.ru/artist/953565'
        return
    elif req['request']['original_utterance'].lower() in [
        'выступления',
    ]:
        res['response'][
            'text'] = 'Все выступления Цоя!: https://www.youtube.com/results?search_query=%D0%BA%D0%BE%D0%BD%D1%86%D0%B5%D1%80%D1%82%D1%8B+%D0%B2%D0%B8%D0%BA%D1%82%D0%BE%D1%80%D0%B0+%D1%86%D0%BE%D1%8F'
        return
    elif req['request']['original_utterance'].lower() in [
        'интересные факты',
    ]:
        res['response']['text'] = random.choice(interesting_list)
        return
    else:
        res['response']['text'] = random.choice(missunderstand)

    # res['response']['buttons'] = get_suggests(user_id)


if __name__ == '__main__':
    app.run()
