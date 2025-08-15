# SafePath Backend API

## 📖 Proje Hakkında

SafePath Backend, engelli bireylerin şehirde daha güvenli ve rahat hareket etmelerini sağlamak amacıyla geliştirilmiş bir yapay zeka destekli backend API'sidir. Bu proje, sesli sorguları alıp işleyerek kullanıcılara erişilebilir mekanlar, güvenlik bilgileri ve ulaşım seçenekleri hakkında bilgi verir.

## 🎯 Özellikler

- **🎤 Sesli Sorgu İşleme**: Whisper AI ile ses kayıtlarını metne çevirme
- **🧠 Akıllı Yanıt Üretimi**: Qwen2.5-7B modeli ile doğal dil işleme
- **🔍 Konum Tanıma**: BERT-Turkish-NER ile metinden konum bilgisi çıkarma
- **🗣️ Sesli Yanıt**: MMS-TTS ile metni sese dönüştürme
- **📍 Erişilebilir Mekan Bilgileri**: İBB Açık Veri Portalı entegrasyonu
- **⚡ Lazy Loading**: Hızlı başlangıç için optimize edilmiş model yükleme
- **🔥 GPU/CPU Desteği**: Otomatik donanım algılama ve optimizasyon

## 🏗️ Sistem Mimarisi

```
SafePath Backend/
├── main.py                    # FastAPI ana uygulama
├── requirements.txt           # Python bağımlılıkları
├── logic/                     # İş mantığı modülleri
│   ├── ai_pipelines.py       # AI model yönetimi (Lazy Loading)
│   ├── ai_pipelines_fast.py  # Hızlı/küçük modeller (alternatif)
│   ├── database.py           # Veritabanı simülasyonu
│   └── prompt_manager.py     # LLM prompt yönetimi
├── models_cache/             # AI modelleri cache klasörü
└── temp/                     # Geçici ses dosyaları
```

## 🚀 Kurulum

### Ön Gereksinimler

- Python 3.9+
- 16GB+ RAM (önerilen)
- CUDA destekli GPU (opsiyonel, performans için)
- ~20GB disk alanı (AI modelleri için)

### Adım 1: Depoyu Klonlayın

```bash
git clone <repository-url>
cd safepath_backend
```

### Adım 2: Sanal Ortam Oluşturun

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\\Scripts\\activate   # Windows
```

### Adım 3: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 4: Sunucuyu Başlatın

```bash
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
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

## ⚡ Performance Optimizasyonları

### Lazy Loading Sistemi
- **Başlangıç**: Sadece STT ve NER modelleri yüklenir
- **İlk İstek**: LLM ve TTS modelleri ihtiyaç halinde yüklenir
- **Sonraki İstekler**: Tüm modeller hazır, hızlı yanıt

### Bellek Yönetimi
- GPU varsa otomatik GPU kullanımı
- CPU fallback desteği
- Model cache sistemi
- Geçici dosya temizleme

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

### Yeni Özellik Ekleme

1. `logic/` klasörüne yeni modül ekleyin
2. `main.py`'da endpoint tanımlayın
3. Gerekirse `requirements.txt`'e bağımlılık ekleyin
4. Test edin

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

### Bellek Sorunları
- Daha küçük modeller kullanın (`ai_pipelines_fast.py`)
- Batch size'ı azaltın
- GPU belleği temizleyin

### Deprecated Uyarıları
- Zaten warnings filtresi eklendi
- Transformers versiyonunu güncelleyin

## 🤝 Katkı Sağlama

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Commit yapın (`git commit -m 'Add some AmazingFeature'`)
4. Push yapın (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## 👥 İletişim

- **Proje Sahibi**: [Sizin İsminiz]
- **E-posta**: [email@example.com]
- **GitHub**: [github.com/username]

## 🙏 Teşekkürler

- **Hugging Face**: AI modelleri için
- **OpenAI**: Whisper modeli için
- **Facebook**: MMS-TTS modeli için
- **İBB**: Açık veri portalı için
- **FastAPI**: Web framework için

---

*SafePath - Erişilebilir bir şehir için yapay zeka çözümleri* 🌟
