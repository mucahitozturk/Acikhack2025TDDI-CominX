import json

def create_unified_safepath_prompt(user_input: str, location: str | None, data: dict) -> str:
    """
    LLM'e tüm bilgileri bir "araç kutusu" gibi sunan ve belirli bir JSON formatında
    yanıt vermesini isteyen birleştirilmiş prompt oluşturur.
    """
    data_context = f"""
### BÖLGE BİLGİ KARTI: {location or 'Tespit Edilemedi'} ###
- Güvenlik Skoru: {data.get('safety_score', 'N/A')}/10
- Tespit Edilen Erişilebilir Tuvaletler: {json.dumps(data.get('accessible_toilets', []), ensure_ascii=False)}
- Tespit Edilen Erişilebilir Kafe/Restoranlar: {json.dumps(data.get('accessible_food', []), ensure_ascii=False)}
- Tespit Edilen Erişilebilir Ulaşım Seçenekleri: {json.dumps(data.get('transport', []), ensure_ascii=False)}
"""

    system_prompt = """<|im_start|>system
Sen SafePath adlı, engelli bireylere şehirde yardımcı olan bir yapay zeka asistanısın. Görevin, sana verilen BİLGİ KARTI'nı ve kullanıcının sorusunu analiz ederek, net, yardımcı ve empatik bir yanıt vermektir.

CEVAP FORMATI:
Yanıtını MUTLAKA aşağıdaki JSON formatında ver. Başka hiçbir metin ekleme.
{
  "thought": "Kullanıcının ana ihtiyacını ve hangi bilgileri kullanacağını özetleyen kısa bir düşünce süreci.",
  "responseText": "Kullanıcıya gösterilecek, akıcı ve doğal dildeki metin.",
  "suggestedActions": ["Sonraki adım için öneri 1", "Sonraki adım için öneri 2"]
}
<|im_end|>"""

    user_prompt = f"""<|im_start|>user
{data_context}

Kullanıcı Sorusu: "{user_input}"

Yukarıdaki bilgi kartını ve kullanıcının sorusunu kullanarak istenen JSON formatında bir yanıt oluştur.
<|im_end|>"""

    return f"{system_prompt}\n{user_prompt}\n<|im_start|>assistant\n"