import torch
from diffusers import AmusedPipeline
import base64
import io
from PIL import Image

_pipeline = None

def load_image_model():
    """Загружает модель генерации изображений amused-256"""
    global _pipeline
    
    if _pipeline is None:
        print("🎨 Загрузка модели генерации изображений amused-256...")
        
        _pipeline = AmusedPipeline.from_pretrained(
            "amused/amused-256",
            variant="fp16",
            torch_dtype=torch.float32  # Для CPU
        )
        
        # Включаем экономию памяти
        _pipeline.enable_attention_slicing()
        _pipeline = _pipeline.to("cpu")
        
        print("✅ Модель генерации изображений загружена")
    
    return _pipeline

def generate_image(prompt: str, seed: int = 42, num_steps: int = 12) -> str:
    """
    Генерирует изображение по промпту и возвращает base64 строку
    """
    pipeline = load_image_model()
    
    generator = torch.Generator(device="cpu").manual_seed(seed)
    
    result = pipeline(
        prompt,
        generator=generator,
        num_inference_steps=num_steps
    )
    
    image = result.images[0]
    
    # Конвертируем в base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return img_str