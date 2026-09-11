from flask import Flask, render_template, request, session, redirect, url_for
from ai import analyze
from json import loads
from anime_image_v2 import get_character_image

app = Flask(__name__)
app.config['secret_key'] = ''
app.secret_key = "148852228"

QUESTIONS = [
    "1. Представь, что ты оказался в компании людей, которых совсем не знаешь. Как ты обычно ведёшь себя в такой ситуации?",
    "2. Что ты обычно делаешь, когда тебе становится эмоционально тяжело? Расскажи, как ты ведёшь себя в такие моменты.",
    "3. Вспомни ситуацию, когда кто-то сильно тебя разозлил. Что ты сделал и почему именно так?",
    "4. Представь, что твой близкий человек совершил поступок, который ты считаешь неправильным. Как ты поступишь?",
    "5. Что для тебя важнее в споре: доказать свою правоту или сохранить хорошие отношения? Почему?",
    "6. Расскажи о ситуации, когда тебе пришлось принять действительно важное решение. Как ты его принимал?",
    "7. Что ты обычно делаешь, когда сталкиваешься с проблемой, которую не знаешь, как решить?",
    "8. Что тебе ближе: сначала долго всё продумать или начать действовать и разбираться уже по ходу? Почему?",
    "9. Представь, что у тебя есть возможность получить всё, чего ты хочешь, но для этого придётся пожертвовать чем-то очень важным для тебя. Чем ты никогда не пожертвуешь?",
    "10. Что для тебя означает «успешный человек»?",
    "11. Как ты понимаешь, что поступил правильно?",
    "12. Расскажи о случае, когда у тебя что-то не получилось. Что ты сделал после этого?",
    "13. Представь, что тебе дали цель, которая кажется почти невозможной. Что ты будешь делать?",
    "14. Что сильнее всего заставляет тебя двигаться вперёд, даже когда тебе тяжело?",
    "15. Какие свои качества ты ценишь больше всего? А какие хотел бы изменить?",
    "16. Если бы твой лучший друг должен был описать тебя тремя словами, какие слова он бы назвал? Почему именно они?",
]

@app.route('/')
def hello_world():
    return render_template("index.html", title="main")

@app.route('/quiz')
def quiz():
    return render_template("quiz.html", title="quiz")

@app.route('/quiz/freeform', methods=['GET', 'POST'])
def freeform():
    if request.method == 'POST':
        return redirect(url_for('quiz_freeform_result'), code=307)
    return render_template("freeform.html", title="form")

@app.route('/quiz/freeform/result', methods=['GET', 'POST'])
def quiz_freeform_result():
    username = request.form.get('username', '')
    about = request.form.get('about', '')
    all_text = f"Имя: {username}\nО себе: {about}"

    result_json = analyze(all_text)
    result = loads(result_json)
    session.clear()
    character_image_url_1 = get_character_image(result['first']['character'], result['first']['anime'])
    character_image_url_2 = get_character_image(result['second']['character'], result['second']['anime'])
    character_image_url_3 = get_character_image(result['third']['character'], result['third']['anime'])
    return render_template("result_form.html", title="result", result=result,
                           character_image_url_1=character_image_url_1, character_image_url_2=character_image_url_2, character_image_url_3=character_image_url_3)

@app.route('/quiz/form/<int:num>', methods=['GET', 'POST'])
def form(num):
    if request.method == 'POST':
        session[f'form_{num}'] = request.form['form']
        if num >= len(QUESTIONS):
            return redirect(url_for('quiz_result'))
        return redirect(url_for('form', num=num + 1))
    return render_template("form.html", title="form", num=num, question=QUESTIONS[num - 1])

@app.route('/quiz/form/result', methods=['GET', 'POST'])
def quiz_form_result():
    answers = []

    for i in range(1, len(QUESTIONS) + 1):
        answer = session.get(f'form_{i}')
        if answer:
            answers.append(f"{QUESTIONS[i - 1]}: {answer}")
    all_text = "\n".join(answers)
    result_json = analyze(all_text)
    result = loads(result_json)
    session.clear()
    character_image_url_1 = get_character_image("Levi Ackerman")
    return render_template("result_form.html", title="result", result=result, character_image_url_1=character_image_url_1)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
