import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

_model = None
_tokenizer = None

def load_text_model():
    """Загружает легковесную текстовую модель (работает на CPU)"""
    global _model, _tokenizer
    
    if _model is None:
        print("📚 Загрузка текстовой модели Qwen2.5-1.5B...")
        model_id = "Qwen/Qwen2.5-1.5B-Instruct"
        
        _tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            trust_remote_code=True
        )
        
        _model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=torch.float32,  # Для CPU
            device_map="cpu",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        print("✅ Текстовая модель загружена")
    
    return _model, _tokenizer

def generate_text(prompt: str, max_length: int = 512) -> str:
    """Генерирует текст на основе промпта"""
    model, tokenizer = load_text_model()
    
    # Форматируем промпт для instruct-модели
    messages = [
        {"role": "user", "content": prompt}
    ]
    
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=max_length,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    return response.strip()

# Альтернативный вариант: более лёгкая модель для слабых компьютеров
# Модель: "microsoft/phi-2" (2.7B) или "IlyaGusev/saiga_mistral_7b" (если нужно русский лучше)