# core/substances.py
from dataclasses import dataclass

@dataclass
class Chemical:
    formula: str
    name: str
    state: str  # 'solid', 'liquid', 'gas'
    color: str  # HEX Kodu
    density: float  # g/cm³
    ph: float
    temperature: float  # Kelvin

