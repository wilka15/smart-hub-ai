# app.py
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Ключ берем из переменной окружения, которую мы настроим в Render
# Это самый безопасный способ хранить секреты
client = OpenAI(
    api_key=os.environ.get('ROUTERAI_API_KEY'),
    base_url="https://routerai.ru/api/v1"
)

@app.route('/')
def index():
    # При заходе на главную страницу отдаем HTML-файл
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # Получаем вопрос от браузера
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "Вопрос не может быть пустым"}), 400

    try:
        # Отправляем запрос в RouterAI (ключ уже внутри client)
        response = client.chat.completions.create(
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"Ошибка при обработке запроса: {str(e)}"}), 500

if __name__ == '__main__':
    # Запускаем сервер локально для тестов
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
