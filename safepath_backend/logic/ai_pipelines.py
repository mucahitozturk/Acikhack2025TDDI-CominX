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

def load_all_models():
    """
    Tüm yapay zeka modellerini ve pipeline'ları yükler.
    Bu fonksiyon sunucu başladığında sadece bir kez çalıştırılmalıdır.
    """
    print("Yapay zeka modelleri yükleniyor... Bu işlem sunucu donanımına göre birkaç dakika sürebilir.")
    
    # Model konfigürasyonları
    MODEL_WHISPER = "openai/whisper-large-v3"
    MODEL_NER = "savasy/bert-base-turkish-ner-cased"
    MODEL_LLM = "Qwen/Qwen2.5-7B-Instruct"
    MODEL_TTS = "facebook/mms-tts-tur"
    
    # Otomatik cihaz ve veri tipi seçimi
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    print(f"Modeller için kullanılacak cihaz: {device.upper()}")

    # Cache dizinini ayarla
    models_cache_dir = os.path.join(os.getcwd(), "models_cache")

    # Sadece gerekli modelleri hızlıca yükle (STT ve NER)
    print("Hızlı başlangıç: Sadece temel modeller yükleniyor...")
    
    # Pipeline'ları oluştur - sadece temel modeller
    stt_pipe = pipeline(
        "automatic-speech-recognition", 
        model=MODEL_WHISPER, 
        device=device, 
        torch_dtype=dtype, 
        model_kwargs={"cache_dir": models_cache_dir}
    )
    ner_pipe = pipeline("ner", model=MODEL_NER, model_kwargs={"cache_dir": models_cache_dir})
    
    print("Temel modeller yüklendi! LLM ve TTS modelleri lazy loading ile yüklenecek.")
    
    # LLM ve TTS modellerini lazy loading için None olarak başlat
    return {
        "stt": stt_pipe,
        "ner": ner_pipe,
        "tts": None,  # Lazy loading
        "llm_model": None,  # Lazy loading
        "llm_tokenizer": None,  # Lazy loading
        "model_configs": {
            "MODEL_LLM": MODEL_LLM,
            "MODEL_TTS": MODEL_TTS,
            "models_cache_dir": models_cache_dir,
            "device": device,
            "dtype": dtype
        }
    }

def load_llm_models(pipelines):
    """LLM modellerini lazy loading ile yükle"""
    if pipelines["llm_model"] is None:
        print("LLM modeli yükleniyor...")
        config = pipelines["model_configs"]
        llm_tokenizer = AutoTokenizer.from_pretrained(config["MODEL_LLM"], cache_dir=config["models_cache_dir"])
        llm_model = AutoModelForCausalLM.from_pretrained(
            config["MODEL_LLM"], 
            cache_dir=config["models_cache_dir"],
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True
        )
        pipelines["llm_model"] = llm_model
        pipelines["llm_tokenizer"] = llm_tokenizer
        print("LLM modeli yüklendi!")
    return pipelines["llm_model"], pipelines["llm_tokenizer"]

def load_tts_model(pipelines):
    """TTS modelini lazy loading ile yükle"""
    if pipelines["tts"] is None:
        print("TTS modeli yükleniyor...")
        config = pipelines["model_configs"]
        tts_pipe = pipeline("text-to-speech", model=config["MODEL_TTS"], model_kwargs={"cache_dir": config["models_cache_dir"]})
        pipelines["tts"] = tts_pipe
        print("TTS modeli yüklendi!")
    return pipelines["tts"]