# Safe# SafePath Backend API

FastAPI tabanlı AI destekli erişilebilirlik API'si. Ana SafePath projesinin backend bileşenidir.

## 🎯 Özellikler

- **🎤 Sesli Sorgu**: Whisper AI ile konuşma tanıma
- **🧠 AI Yanıt**: Qwen2.5-7B ile doğal dil işleme  
- **🔍 Konum NER**: BERT-Turkish ile yer adı çıkarma
- **🗣️ TTS**: MMS-TTS ile sesli yanıt
- **⚡ Lazy Loading**: Optimize edilmiş model yükleme
- **📊 İBB Entegrasyonu**: Açık veri portalı bağlantısı

## 🚀 Kurulum

```bash
# Python 3.9+ gerekli
python -m venv venv
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Sunucuyu başlat  
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## 📡 API Endpoints

- **POST** `/api/process-audio` - Ses dosyası işleme
- **GET** `/api/veriler` - Erişilebilirlik verileri
- **GET** `/health` - Sağlık kontrolü
- **GET** `/docs` - Swagger dokümantasyonu

## 🔧 Yapılandırma

### Çevre Değişkenleri
```bash
TRANSFORMERS_CACHE=./models_cache
CUDA_VISIBLE_DEVICES=0
API_PORT=8080
LOG_LEVEL=INFO
```

### Sistem Gereksinimleri
- **RAM**: 8GB minimum, 16GB+ önerilen
- **Disk**: ~20GB (AI modelleri için)
- **GPU**: Opsiyonel, CUDA destekli
- **Python**: 3.9+

## 🧪 Test

```bash
# API test
curl http://localhost:8080/health

# Swagger UI
open http://localhost:8080/docs

# Ses dosyası test
curl -X POST "http://localhost:8080/api/process-audio" 
  -H "Content-Type: multipart/form-data" 
  -F "file=@test.wav"
```

## 📄 Lisans

MIT License - Ana proje lisansına tabidir.

⚠️ **Not**: MMS-TTS modeli akademik kullanım için (CC-BY-NC 4.0).ccessibility Platform

## 📖 Proje Hakkında

SafePath, engelli bireylerin şehirde daha güvenli hareket etmelerini sağlayan **yapay zeka destekli erişilebilirlik platformudur**. Sesli sorguları alıp işleyerek kullanıcılara erişilebilir mekanlar ve güvenlik bilgileri sunar.

## �️ Proje Yapısı

```
SafePath/
├── 🔧 safepath_backend/      # FastAPI Backend (Python)
│   ├── main.py              # API endpoints
│   ├── logic/               # AI pipelines & business logic
│   └── requirements.txt     # Python dependencies
├── � safepath_mobile/       # Flutter Mobile App
│   ├── lib/                 # Dart/Flutter kod
│   ├── android/             # Android platform
│   ├── ios/                 # iOS platform
│   └── pubspec.yaml         # Flutter dependencies
```

## 🎯 Özellikler

### 🎤 AI Backend
- **Sesli Sorgu**: Whisper AI ile ses-metin dönüşümü
- **Akıllı Yanıt**: Qwen2.5-7B ile doğal dil işleme
- **Konum Tanıma**: BERT-Turkish-NER ile yer bilgisi çıkarma
- **Sesli Yanıt**: MMS-TTS ile metin-ses dönüşümü

### 📱 Mobil & Web App
- **Cross-Platform**: Flutter ile iOS, Android ve Web desteği
- **Offline Mod**: Kritik özellikler için çevrimdışı kullanım
- **Erişilebilir UI**: WCAG standartlarına uygun tasarım
- **Sesli Navigasyon**: Tamamen sesli kontrol desteği

## 🚀 Hızlı Başlangıç

## 📊 Veri Setleri ve Kaynaklar

### 🔗 Kullanılan Açık Veri Kaynakları

#### 1. **İBB Açık Veri Portalı - Erişilebilir Tuvaletler**
- **Kaynak**: İstanbul Büyükşehir Belediyesi
- **URL**: https://data.ibb.gov.tr/dataset/8789b75c-bae9-4acb-8287-bfc0ba88c8ea/resource/9585ab4a-d160-4541-8a41-b86eeec4c1cc/download/sehir_tuvaletleri_verisi.geojson
- **Format**: GeoJSON
- **Açıklama**: İstanbul'daki halka açık tuvaletlerin koordinat ve detay bilgileri
- **Güncellenme**: Anlık API çağrısı ile
- **Lisans**: Açık Veri Lisansı

#### 2. **AI Modelleri ve Veri Setleri**

| Model | Kaynak | Veri Seti | Lisans |
|-------|--------|-----------|--------|
| **Whisper-Large-v3** | OpenAI/Hugging Face | [Whisper Dataset](https://huggingface.co/openai/whisper-large-v3) | MIT |
| **BERT-Turkish-NER** | Savasy/Hugging Face | [Turkish NER Dataset](https://huggingface.co/savasy/bert-base-turkish-ner-cased) | MIT |
| **Qwen2.5-7B-Instruct** | Alibaba/Hugging Face | [Qwen2.5 Dataset](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | Apache 2.0 |
| **MMS-TTS-Turkish** | Facebook/Hugging Face | [MMS Dataset](https://huggingface.co/facebook/mms-tts-tur) | CC-BY-NC 4.0 |

#### 3. **Test Veri Setleri**

**Sesli Test Dosyaları** (Geliştirme için):
```bash
# Test ses dosyalarını indirin
wget https://github.com/YOURUSERNAME/safepath-backend/releases/download/v1.0.0/test-audio-samples.zip
unzip test-audio-samples.zip -d test-data/
```

**Mock Veri Seti** (Geliştirme için):
- **Dosya**: `logic/database.py`
- **İçerik**: Beşiktaş, Kadıköy bölgeleri için örnek erişilebilirlik verileri
- **Format**: Python dictionary

### 🌐 Dış API'ler

#### İBB Açık Veri API
```python
# Otomatik veri çekme
GET https://data.ibb.gov.tr/dataset/.../download/sehir_tuvaletleri_verisi.geojson

# Yanıt formatı:
{
  "type": "FeatureCollection",
  "features": [
    {
      "properties": {
        "X": 28.9784,
        "Y": 41.0082,
        "MAHAL_ADI": "Beşiktaş Merkez",
        "ILCE": "Beşiktaş"
      }
    }
  ]
}
```

### 📥 Veri İndirme ve Kurulum

**Otomatik Model İndirme:**
- İlk çalıştırmada modeller otomatik olarak Hugging Face'den indirilir
- `models_cache/` klasörüne kaydedilir
- İnternet bağlantısı gerektirir (tek seferlik)

**Manuel Model İndirme (Opsiyonel):**
```python
from transformers import pipeline

# Modelleri önceden indirme
pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
pipeline("ner", model="savasy/bert-base-turkish-ner-cased")
pipeline("text-to-speech", model="facebook/mms-tts-tur")
```

## 🔧 Yapılandırma ve Çevresel Değişkenler

### Çevre Değişkenleri (.env dosyası)

```bash
# .env dosyası oluşturun
cat > .env << EOF
# Model Cache Dizini
TRANSFORMERS_CACHE=./models_cache
HF_HOME=./models_cache

# GPU Ayarları
CUDA_VISIBLE_DEVICES=0
PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512

# API Ayarları
API_HOST=0.0.0.0
API_PORT=8080
API_WORKERS=1

# Log Seviyesi
LOG_LEVEL=INFO

# Geçici Dosya Temizlik (saniye)
TEMP_FILE_CLEANUP_INTERVAL=3600
EOF
```

## 🤖 Kullanılan AI Modelleri

| Model | Görevi | Boyut | Açıklama |
|-------|--------|-------|----------|
| **Whisper-Large-v3** | Speech-to-Text | ~3GB | Ses kayıtlarını metne çevirme |
| **BERT-Turkish-NER** | Named Entity Recognition | ~1GB | Türkçe metinden konum çıkarma |
| **Qwen2.5-7B-Instruct** | Language Model | ~14GB | Doğal dil anlama ve yanıt üretme |
| **MMS-TTS-Turkish** | Text-to-Speech | ~2GB | Metni Türkçe sese dönüştürme |

## 📡 API Endpoints

### 1. Sesli Sorgu İşleme
```http
POST /process-audio-query/
Content-Type: multipart/form-data

Body: audio file (WAV format)
```

**Yanıt:**
```json
{
  "userInput": "Beşiktaş'ta erişilebilir tuvalet var mı?",
  "assistantResponse": {
    "thought": "Kullanıcı Beşiktaş bölgesinde erişilebilir tuvalet arıyor.",
    "responseText": "Beşiktaş'ta erişilebilir tuvaletler mevcut...",
    "suggestedActions": ["Beşiktaş Belediyesi'ni ziyaret edin", "Harita uygulamasını kullanın"]
  },
  "assistantResponseAudioUrl": "/audio/response_1234567890.wav"
}
```

### 2. Ses Dosyası Alma
```http
GET /audio/{file_name}
```

### 3. Erişilebilir Mekan Verileri
```http
GET /api/veriler
```

**Yanıt:**
```json
[
  {
    "x": 28.9784,
    "y": 41.0082,
    "mahal_adi": "Beşiktaş Merkez",
    "ilce": "Beşiktaş"
  }
]
```

## 🛠️ Geliştirme

### Proje Yapısı Detayları

**`main.py`**: FastAPI uygulamasının ana dosyası
- CORS middleware
- Endpoint tanımları
- Error handling

**`logic/ai_pipelines.py`**: AI model yönetimi
- Lazy loading implementasyonu
- Model konfigürasyonları
- GPU/CPU otomatik algılama

**`logic/database.py`**: Veri simülasyonu
- Konum bazlı mock data
- Güvenlik skorları
- Erişilebilir mekan bilgileri

**`logic/prompt_manager.py`**: LLM prompt yönetimi
- Sistem promptları
- JSON format kontrolü
- Context oluşturma

## 🔧 Yapılandırma

### Çevre Değişkenleri
```bash
export CUDA_VISIBLE_DEVICES=0  # GPU seçimi
export TRANSFORMERS_CACHE=/path/to/cache  # Model cache dizini
```

### Model Değiştirme
`logic/ai_pipelines.py` dosyasında model isimlerini değiştirin:
```python
MODEL_WHISPER = "openai/whisper-base"  # Daha küçük model
MODEL_LLM = "microsoft/DialoGPT-medium"  # Daha hızlı model
```

## 📊 Sistem Gereksinimleri

### Minimum Sistem
- **RAM**: 8GB
- **Disk**: 10GB
- **CPU**: 4 çekirdek
- **Süre**: İlk yükleme ~10 dakika

### Önerilen Sistem
- **RAM**: 16GB+
- **Disk**: 20GB+ SSD
- **GPU**: NVIDIA RTX 3060+
- **CPU**: 8+ çekirdek
- **Süre**: İlk yükleme ~3 dakika

## 🚨 Sorun Giderme

### Model Yükleme Sorunları
```bash
# Cache temizleme
rm -rf models_cache/
# Yeniden başlatma
uvicorn main:app --reload
```

## 📄 Lisans ve Yasal Bilgiler

### 📋 Proje Lisansı
Bu proje **MIT Lisansı** altında yayınlanmaktadır. Detaylar için [LICENSE](LICENSE) dosyasına bakınız.


### 📊 Veri Kullanım Politikası

- **İBB Açık Veri**: İstanbul Büyükşehir Belediyesi Açık Veri Lisansı
- **Hugging Face Modelleri**: İlgili model sayfalarındaki lisanslara tabidir
- **Test Verileri**: Proje kapsamında oluşturulmuş, MIT lisansı altında

### 🎯 Katkı Alanları

- 🐛 Hata düzeltmeleri
- 🚀 Yeni özellikler
- 📚 Dokümantasyon iyileştirmeleri
- 🔧 Performans optimizasyonları
- 🌍 Çeviri ve yerelleştirme
- ♿ Erişilebilirlik geliştirmeleri

## 🏗️ Geliştirme Durumu ve Roadmap

### ✅ Tamamlanan Özellikler

- [x] Türkçe konuşma tanıma (Whisper)
- [x] Varlık entitesi çıkarma (BERT-NER)
- [x] AI yanıt üretimi (Qwen2.5)
- [x] Türkçe sesli yanıt (MMS-TTS)
- [x] FastAPI backend
- [x] Lazy loading optimizasyonu
- [x] CORS desteği
- [x] Kapsamlı dokümantasyon

### 🎯 Gelecek Planları

- [ ] Multi-language desteği (İngilizce, Almanca)
- [ ] Real-time WebSocket API
- [ ] Mobil uygulama SDK'sı
- [ ] Offline mod desteği
- [ ] Custom model fine-tuning araçları

---

## 📚 Daha Fazla Bilgi

### 🔗 Yararlı Bağlantılar

- [FastAPI Dokümantasyonu](https://fastapi.tiangolo.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [PyTorch Dokümantasyonu](https://pytorch.org/docs/)
- [İBB Açık Veri Portalı](https://data.ibb.gov.tr/)
- [Erişilebilirlik Standartları (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/)

### 📖 Teknik Makaleler

- [Whisper: Robust Speech Recognition](https://arxiv.org/abs/2212.04356)
- [BERT: Pre-training Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805)
- [Qwen2.5: Technical Report](https://qwenlm.github.io/)
- [MMS: Scaling Speech Technology to 1000+ Languages](https://arxiv.org/abs/2305.13516)

---

**🌟 Bu proje, teknolojinin herkes için erişilebilir olması gerektiği inancıyla geliştirilmiştir.**

*SafePath Backend v1.0.0 - AI-Powered Accessibility for Everyone*
