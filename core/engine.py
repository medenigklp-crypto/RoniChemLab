# core/engine.py
from core.substances import Chemical

class SimulationEngine:
    def __init__(self):
        self.beaker_contents = []

    def add_substance(self, substance: Chemical):
        self.beaker_contents.append(substance)
        return self.check_reactions()

    def check_reactions(self):
        """Beher içindeki maddeleri kontrol eder ve reaksiyon matrisini tetikler."""
        formulas = [c.formula for c in self.beaker_contents]
        
        # Dinamik reaksiyon kontrolü
        if "Na" in formulas and "H2O" in formulas:
            self.beaker_contents.clear()
            # Yeni oluşan ürün: Sodyum Hidroksit çözeltisi
            self.beaker_contents.append(Chemical("NaOH", "Sodyum Hidroksit", "liquid", "#EAEAEA", 2.13, 14.0, 373.15))
            return {
                "triggered": True,
                "reaction": "2Na + 2H2O -> 2NaOH + H2 (Eksotermik)",
                "effect": "explosion_particles",
                "temp_rise": 80.0
            }
        return {"triggered": False}

