from flask import Flask, request, render_template, jsonify
from classifier import classify_intent
from text_model import generate_text
from image_model import generate_image
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    """Единый эндпоинт для обработки любого запроса"""
    data = request.get_json()
    prompt = data.get('prompt', '').strip()
    
    if not prompt:
        return jsonify({'error': 'Промпт не может быть пустым'}), 400
    
    # 1. Определяем тип запроса
    intent = classify_intent(prompt)
    print(f"🔍 Распознан тип: {intent.upper()} | Промпт: {prompt[:50]}...")
    
    start_time = time.time()
    
    try:
        if intent == 'image':
            # Генерация изображения
            result = generate_image(prompt)
            response = {
                'type': 'image',
                'data': result,  # base64 строка
                'time': round(time.time() - start_time, 1)
            }
        else:
            # Генерация текста
            result = generate_text(prompt)
            response = {
                'type': 'text',
                'data': result,
                'time': round(time.time() - start_time, 1)
            }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Запуск мультимодального приложения...")
    print("📝 Текстовая модель: Qwen2.5-1.5B (CPU)")
    print("🎨 Графическая модель: amused-256 (CPU)")
    print("📍 http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)