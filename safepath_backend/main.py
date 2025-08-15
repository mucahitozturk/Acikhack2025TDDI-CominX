# --- Gerekli Kütüphaneler ---
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import time
import os
import json
import soundfile as sf
import requests
import warnings

# Transformers uyarılarını bastır
warnings.filterwarnings("ignore", message=".*return_token_timestamps.*", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*WhisperFeatureExtractor.*", category=FutureWarning)

# --- Modüler Yapıdan Gelen Fonksiyonlar ---
from logic.ai_pipelines import load_all_models, load_llm_models, load_tts_model
from logic.database import get_mock_data_for_location
from logic.prompt_manager import create_unified_safepath_prompt

# ==============================================================================
# GEREKLİ PYDANTIC MODELLERİ
# ==============================================================================
# Sadece kullanılan modelleri bırakıyoruz

class StatusResponse(BaseModel):
    status: str
    uptime: str
    timestamp: str

class ToiletData(BaseModel):
    x: float
    y: float
    mahal_adi: str
    ilce: str

# ==============================================================================
# Global Değişkenler
# ==============================================================================
pipelines = {}
TEMP_DIR = os.path.join(os.getcwd(), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# ==============================================================================
# FastAPI Uygulaması
# ==============================================================================
app = FastAPI(
    title="SafePath Birleşik AI API",
    description="Flutter uygulaması için Yapay Zeka ve Veri Servislerini içeren birleşik API",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """Sunucu başladığında modelleri yükle."""
    global pipelines
    pipelines = load_all_models()

# ==============================================================================
# ANA API ENDPOINT'LERİ
# ==============================================================================

@app.post("/process-audio-query/", summary="Sesli Sorguyu İşle (Yapay Zeka Çekirdeği)", tags=["Yapay Zeka"])
async def process_audio_query(file: UploadFile = File(..., description="Kullanıcının ses kaydı")):
    """
    Sesli bir sorguyu alır, metne çevirir, analiz eder, LLM ile yanıt üretir
    ve hem metin hem de sesli yanıt olarak geri döner.
    """
    # ... Bu fonksiyonun içeriği öncekiyle aynı ...
    if not pipelines:
        raise HTTPException(status_code=503, detail="Modeller henüz yüklenmedi...")
    file_path = os.path.join(TEMP_DIR, f"input_{int(time.time())}.wav")
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    # Whisper çağrısı - deprecated parametreleri kullanmayan versiyon
    transcribed_text = pipelines["stt"](
        file_path,
        return_timestamps=False,
        generate_kwargs={
            "language": "turkish", 
            "task": "transcribe",
            "do_sample": False
        }
    )["text"]
    if not transcribed_text.strip():
        raise HTTPException(status_code=400, detail="Konuşma algılanamadı.")
    entities = pipelines["ner"](transcribed_text)
    locations = [ent['word'] for ent in entities if 'LOC' in ent['entity']]
    location_text = locations[0] if locations else None
    mock_data = get_mock_data_for_location(location_text)
    prompt = create_unified_safepath_prompt(transcribed_text, location_text, mock_data)
    
    # LLM modellerini lazy loading ile yükle
    model, tokenizer = load_llm_models(pipelines)
    
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=256, pad_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    try:
        json_str_start = generated_text.rfind('{')
        json_str_end = generated_text.rfind('}') + 1
        json_str = generated_text[json_str_start:json_str_end]
        response_obj = json.loads(json_str)
    except Exception:
        raise HTTPException(status_code=500, detail="LLM'den geçerli bir yanıt alınamadı.")
    final_text_response = response_obj.get("responseText", "Yanıt metni bulunamadı.")
    
    # TTS modelini lazy loading ile yükle
    tts_pipe = load_tts_model(pipelines)
    speech_output = tts_pipe(final_text_response)
    output_filename = f"response_{int(time.time())}.wav"
    output_filepath = os.path.join(TEMP_DIR, output_filename)
    sf.write(output_filepath, speech_output["audio"][0], samplerate=speech_output["sampling_rate"])
    return {
        "userInput": transcribed_text,
        "assistantResponse": response_obj,
        "assistantResponseAudioUrl": f"/audio/{output_filename}"
    }

@app.get("/audio/{file_name}", summary="Ses Dosyasını Getir", tags=["Yapay Zeka"])
async def get_audio_file(file_name: str):
    """Oluşturulan ses dosyalarını sunar."""
    file_path = os.path.join(TEMP_DIR, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/wav")
    raise HTTPException(status_code=404, detail="Ses dosyası bulunamadı.")

# DEĞİŞİKLİK: API endpoint yolu güncellendi
@app.get("/api/veriler", response_model=List[ToiletData], tags=["Veri Servisleri"])
async def get_city_points_data():
    """İBB Açık Veri Portalı'ndan halka açık tuvalet verilerini anlık olarak çeker."""
    try:
        url = "https://data.ibb.gov.tr/dataset/8789b75c-bae9-4acb-8287-bfc0ba88c8ea/resource/9585ab4a-d160-4541-8a41-b86eeec4c1cc/download/sehir_tuvaletleri_verisi.geojson"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        toilet_data = [
            ToiletData(
                x=feature.get("properties", {}).get("X", 0.0),
                y=feature.get("properties", {}).get("Y", 0.0),
                mahal_adi=feature.get("properties", {}).get("MAHAL_ADI", ""),
                ilce=feature.get("properties", {}).get("ILCE", "")
            ) for feature in data.get("features", [])
        ]
        return toilet_data
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Harici veri kaynağına ulaşılamadı: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Veri işlenirken bir hata oluştu: {e}")