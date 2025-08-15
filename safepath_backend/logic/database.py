def get_mock_data_for_location(location: str | None) -> dict:
    """Konum bazlı simüle edilmiş veritabanından bilgi alır."""
    location_db = {
        "beşiktaş": {
            "safety_score": 9,
            "accessible_toilets": [{"name": "Beşiktaş Belediyesi", "features": ["rampa", "geniş kapı"]}],
            "accessible_food": [{"name": "Starbucks Beşiktaş", "features": ["rampa girişi", "geniş koridor"]}, {"name": "Mado Beşiktaş", "features": ["zemin kat"]}],
            "transport": [{"type": "Metro", "accessibility": "Asansör ve rampa mevcut"}]
        },
        "kadıköy": {
            "safety_score": 8,
            "accessible_toilets": [{"name": "Kadıköy Belediyesi", "features": ["rampa"]}],
            "accessible_food": [{"name": "Starbucks Bahariye", "features": ["zemin kat", "rampa"]}]
        }
    }
    # Eğer konum bulunamazsa veya belirtilmezse, varsayılan bir yanıt döndür
    return location_db.get(location.lower() if location else "default", {
        "safety_score": 7, "accessible_toilets": [], "accessible_food": [], "transport": []
    })