# ui/canvas.py
import numpy as np
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen
from PyQt6.QtCore import QTimer, Qt

class ChemCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.liquid_level = 0.0
        self.liquid_color = QColor(0, 0, 0, 0)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start(16)

    def set_liquid(self, volume_ratio, color_hex):
        self.liquid_level = min(volume_ratio, 1.0)
        self.liquid_color = QColor(color_hex)
        self.liquid_color.setAlpha(180)

    def add_explosion_particles(self):
        for _ in range(50):
            self.particles.append({
                "x": self.width() / 2,
                "y": self.height() - 50,
                "vx": np.random.uniform(-4, 4),
                "vy": np.random.uniform(-8, -2),
                "radius": np.random.uniform(2, 5),
                "life": 1.0,
                "color": QColor(255, 76, 41)
            })

    def update_simulation(self):
        for p in self.particles[:]:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.1
            p["life"] -= 0.02
            if p["life"] <= 0:
                self.particles.remove(p)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        beaker_pen = QPen(QColor("#393E46"), 4)
        painter.setPen(beaker_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        margin = 40
        w = self.width() - (margin * 2)
        h = self.height() - 80
        
        painter.drawLine(margin, 20, margin, 20 + h)
        painter.drawLine(margin, 20 + h, margin + w, 20 + h)
        painter.drawLine(margin + w, 20, margin + w, 20 + h)

        if self.liquid_level > 0:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(self.liquid_color))
            liquid_h = h * self.liquid_level
            painter.drawRect(margin + 2, int(20 + h - liquid_h), w - 4, int(liquid_h - 2))

        for p in self.particles:
            color = p["color"]
            color.setAlpha(int(p["life"] * 255))
            painter.setBrush(QBrush(color))
            painter.drawEllipse(int(p["x"]), int(p["y"]), int(p["radius"]), int(p["radius"]))
            
        painter.end()
