# core/engine.py
from core.substances import Chemical

class SimulationEngine:
    def __init__(self):
        self.beaker_contents = []
        self.total_volume = 0.0
        self.mixed_ph = 7.0
        self.has_indicator = False  # Fenolftalein var mı kontrolü

    def add_substance(self, substance: Chemical):
        """Behere yeni bir kimyasal madde ekler ve anlık reaksiyonları hesaplar."""
        self.beaker_contents.append(substance)
        self.total_volume += substance.volume
        
        # pH ve indikatör kontrolü
        if substance.formula == "Phenolphthalein":
            self.has_indicator = True
            
        # Dinamik pH hesabı (Basitleştirilmiş logaritmik yaklaşım)
        self.recalculate_ph()

        # 1. ETKİLEŞİM: Sodyum + Su Reaksiyonu
        formulas = [c.formula for c in self.beaker_contents]
        if "Na" in formulas and "H2O" in formulas:
            # Reaksiyon gerçekleştikten sonra elementleri tüket ve ürünü ekle
            self.remove_substance("Na")
            self.remove_substance("H2O")
            
            # Ürün olarak Sodyum Hidroksit çözeltisi (Baz) ekle
            naoh = Chemical("NaOH", "Sodyum Hidroksit Çözeltisi", "liquid", "#EAEAEA", 0.5, 13.0, 350.15)
            self.beaker_contents.append(naoh)
            self.recalculate_ph()
            
            return {"triggered": True, "reaction": "2Na + 2H2O -> 2NaOH + H2", "temp_rise": 52.0}
            
        # 2. ETKİLEŞİM: Asit + Baz Nötrleşme Reaksiyonu (HCl + NaOH -> NaCl + H2O)
        if "HCl" in formulas and "NaOH" in formulas:
            self.remove_substance("HCl")
            self.remove_substance("NaOH")
            
            # Tuzlu su oluşumu (Nötr ortam)
            nacl = Chemical("NaCl", "Tuzlu Su", "liquid", "#3483FA", 0.6, 7.0, 315.15)
            self.beaker_contents.append(nacl)
            self.recalculate_ph()
            
            return {"triggered": True, "reaction": "HCl + NaOH -> NaCl + H2O (Nötrleşme)", "temp_rise": 15.0}

        return {"triggered": False, "reaction": None, "temp_rise": 0.0}

    def remove_substance(self, formula: str):
        self.beaker_contents = [c for c in self.beaker_contents if c.formula != formula]

    def recalculate_ph(self):
        """Beherdeki maddelere göre genel pH değerini dengeler."""
        if not self.beaker_contents:
            self.mixed_ph = 7.0
            return
            
        total_ph_weight = sum([c.ph * c.volume for c in self.beaker_contents])
        self.mixed_ph = total_ph_weight / self.total_volume

    def get_canvas_color(self) -> str:
        """İndikatör durumuna göre kanvasın alacağı sıvı rengini belirler."""
        # Eğer ortamda fenolftalein indikatörü varsa ve ortam BAZİK (pH > 8.3) ise renk PEMBE olur
        if self.has_indicator and self.mixed_ph > 8.3:
            return "#FF1493"  # Canlı Pembe / Fuşya
        
        # İndikatör yoksa veya asidik/nötr ise en baskın sıvının orijinal rengini döndür
        if self.beaker_contents:
            return self.beaker_contents[-1].color_hex
        return "#3483FA"
