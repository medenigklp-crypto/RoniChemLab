# core/substances.py

class Chemical:
    def __init__(self, formula: str, name: str, state: str, color_hex: str, volume: float, ph: float, temperature: float, molar_mass: float = 1.0):
        self.formula = formula          # Örn: "HCl"
        self.name = name                # Örn: "Hidroklorik Asit"
        self.state = state              # "solid", "liquid", "gas"
        self.color_hex = color_hex      # Kanvasta çizilecek renk kodu
        self.volume = volume            # Litre veya bağıntılı hacim
        self.ph = ph                    # Maddenin kendi pH değeri
        self.temperature = temperature  # Maddenin anlık sıcaklığı (Kelvin)
        self.molar_mass = molar_mass    # Gelişmiş reaksiyon hesapları için mol kütlesi
