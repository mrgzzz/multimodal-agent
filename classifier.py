import re

# Ключевые слова для определения запроса на генерацию изображения
IMAGE_KEYWORDS = [
    # Русские
    'нарис', 'создай изображени', 'сгенерируй изображени', 'нарисуй',
    'картинк', 'рисунок', 'изображени', 'иллюстрац', 'пейзаж', 'портрет',
    'нарисуйте', 'создайте изображение', 'сгенерируйте картинку',
    'нарисуй мне', 'покажи картинку', 'сделай картинку',
    'изобрази', 'визуализируй', 'создай картинку', 'генерация изображения',
    'арт', 'иллюстрация', 'скетч', 'эскиз', 'натюрморт', 'абстракция',
    
    # Английские (для смешанных запросов)
    'draw', 'paint', 'generate image', 'create image', 'picture',
    'illustration', 'artwork', 'sketch', 'render', 'visualize',
    'make a picture', 'i want to see', 'show me a picture',
]

# Шаблоны для более точного распознавания
IMAGE_PATTERNS = [
    r'(?:нарисуй|нарисовать|нарисуйте)\s+(?:мне\s+)?(?:картинку|рисунок|изображение)',
    r'(?:создай|сгенерируй|сделай)\s+(?:мне\s+)?(?:изображение|картинку|рисунок)',
    r'(?:покажи|покажите)\s+(?:мне\s+)?(?:картинку|изображение|рисунок)',
    r'(?:хочу\s+)?(?:увидеть|посмотреть)\s+(?:картинку|изображение)',
    r'(?:напиши|нарисуй)\s+(?:промпт\s+)?(?:для\s+)?(?:нейросети|midjourney|stable diffusion)',
]

def classify_intent(prompt: str) -> str:
    """
    Определяет намерение пользователя: 'text' или 'image'
    
    Args:
        prompt: текстовый запрос пользователя
        
    Returns:
        'image' если запрос просит создать изображение, иначе 'text'
    """
    prompt_lower = prompt.lower().strip()
    
    # Проверка по шаблонам
    for pattern in IMAGE_PATTERNS:
        if re.search(pattern, prompt_lower, re.IGNORECASE):
            return 'image'
    
    # Проверка по ключевым словам
    words = prompt_lower.split()
    for keyword in IMAGE_KEYWORDS:
        if keyword in prompt_lower or keyword in ' '.join(words[:7]):
            return 'image'
    
    # Если запрос очень короткий (< 5 слов) и не содержит ключевых слов,
    # скорее всего это текстовый запрос
    if len(words) < 5 and not any(k in prompt_lower for k in IMAGE_KEYWORDS):
        return 'text'
    
    # По умолчанию — текст
    return 'text'

# Тестовые примеры (для проверки)
if __name__ == '__main__':
    test_queries = [
        ("Нарисуй кота", "image"),
        ("Создай изображение гор", "image"),
        ("Покажи мне картинку с закатом", "image"),
        ("Как дела?", "text"),
        ("Расскажи про космос", "text"),
        ("Что такое нейросети?", "text"),
        ("Напиши код на Python", "text"),
        ("Сгенерируй пейзаж с горами", "image"),
        ("Почему небо голубое?", "text"),
    ]
    
    print("🧪 Тестирование классификатора:")
    for query, expected in test_queries:
        result = classify_intent(query)
        status = "✅" if result == expected else "❌"
        print(f"{status} {query[:40]:40} → {result} (ожидалось: {expected})")