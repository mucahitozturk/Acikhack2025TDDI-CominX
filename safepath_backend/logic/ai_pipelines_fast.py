import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import os
import warnings
import logging

# Transformers deprecated uyarılarını bastır
warnings.filterwarnings("ignore", message=".*return_token_timestamps.*", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*WhisperFeatureExtractor.*", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*return_attention_mask.*", category=FutureWarning)

# Transformers logger seviyesini ayarla
logging.getLogger("transformers").setLevel(logging.ERROR)

def load_fast_models():
    """
    Daha küçük ve hızlı modelleri yükler - development için
    """
    print("Hızlı modeller yükleniyor...")
    
    # Daha küçük model konfigürasyonları
    MODEL_WHISPER = "openai/whisper-base"  # Daha küçük Whisper
    MODEL_NER = "savasy/bert-base-turkish-ner-cased"  # Aynı
    MODEL_LLM = "microsoft/DialoGPT-medium"  # Çok daha küçük LLM
    MODEL_TTS = "facebook/mms-tts-tur"  # Aynı
    
    # Otomatik cihaz ve veri tipi seçimi
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    print(f"Modeller için kullanılacak cihaz: {device.upper()}")

    # Cache dizinini ayarla
    models_cache_dir = os.path.join(os.getcwd(), "models_cache")

    # Pipeline'ları oluştur
    stt_pipe = pipeline(
        "automatic-speech-recognition", 
        model=MODEL_WHISPER, 
        device=device, 
        torch_dtype=dtype, 
        model_kwargs={"cache_dir": models_cache_dir}
    )
    ner_pipe = pipeline("ner", model=MODEL_NER, model_kwargs={"cache_dir": models_cache_dir})
    tts_pipe = pipeline("text-to-speech", model=MODEL_TTS, model_kwargs={"cache_dir": models_cache_dir})
    
    # Küçük LLM modeli
    llm_tokenizer = AutoTokenizer.from_pretrained(MODEL_LLM, cache_dir=models_cache_dir)
    llm_model = AutoModelForCausalLM.from_pretrained(
        MODEL_LLM, 
        cache_dir=models_cache_dir,
        torch_dtype=dtype
    )
    
    print("Hızlı modeller yüklendi!")
    
    return {
        "stt": stt_pipe,
        "ner": ner_pipe,
        "tts": tts_pipe,
        "llm_model": llm_model,
        "llm_tokenizer": llm_tokenizer,
    }
