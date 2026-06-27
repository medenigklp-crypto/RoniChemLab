# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLabel
from config.settings import APP_NAME, VERSION, THEME
from core.engine import SimulationEngine
from core.substances import Chemical
from features.ai_assistant import ChemAIAssistant

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = SimulationEngine()
        self.ai = ChemAIAssistant()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(1100, 700)
        
        # Ana Widget ve Layout
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        # SOL TARAF: Simülasyon Kontrol ve Beher Alanı
        sim_layout = QVBoxLayout()
        self.canvas_label = QLabel("Beher Simülasyon Alanı (2D/3D Particle Canvas)")
        self.canvas_label.setStyleSheet(f"background-color: {THEME['surface']}; border: 2px dashed {THEME['secondary']}; color: {THEME['text_muted']}; font-size: 16px;")
        self.canvas_label.setProperty("alignment", "Center")
        
        btn_add_water = QPushButton("Saf Su Ekle (H2O)")
        btn_add_sodium = QPushButton("Sodyum Ekle (Na)")
        
        btn_add_water.clicked.connect(self.add_water)
        btn_add_sodium.clicked.connect(self.add_sodium)
        
        sim_layout.addWidget(self.canvas_label, stretch=4)
        sim_layout.addWidget(btn_add_water)
        sim_layout.addWidget(btn_add_sodium)
        
        # SAĞ TARAF: Gelişmiş AI Sohbet ve Otomatik Raporlama Paneli
        ai_layout = QVBoxLayout()
        ai_title = QLabel("AI Kimya Asistanı & Analiz")
        ai_title.setStyleSheet(f"color: {THEME['primary']}; font-weight: bold; font-size: 14px;")
        
        self.ai_output = QTextEdit()
        self.ai_output.setReadOnly(True)
        self.ai_output.setStyleSheet(f"background-color: {THEME['surface']}; color: {THEME['text_main']}; border: 1px solid {THEME['secondary']};")
        
        btn_analyze = QPushButton("Beheri AI ile Analiz Et")
        btn_analyze.clicked.connect(self.trigger_ai_analysis)
        
        ai_layout.addWidget(ai_title)
        ai_layout.addWidget(self.ai_output)
        ai_layout.addWidget(btn_analyze)
        
        # Layoutları Birleştirme
        main_layout.addLayout(sim_layout, stretch=2)
        main_layout.addLayout(ai_layout, stretch=1)
        
        self.setCentralWidget(main_widget)
        self.apply_global_styles()

    def apply_global_styles(self):
        # Uygulamanın modern koyu görünümü
        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {THEME['background']}; }}
            QPushButton {{
                background-color: {THEME['secondary']};
                color: {THEME['text_main']};
                border: 1px solid #444;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {THEME['primary']};
                color: #121212;
            }}
        """)

    def add_water(self):
        water = Chemical("H2O", "Saf Su", "liquid", "#3483FA", 1.0, 7.0, 298.15)
        res = self.engine.add_substance(water)
        self.update_log(f"Behere H2O eklendi. {res['reaction'] if res['triggered'] else ''}")

    def add_sodium(self):
        sodium = Chemical("Na", "Sodyum Metal", "solid", "#C0C0C0", 0.97, 7.0, 298.15)
        res = self.engine.add_substance(sodium)
        if res['triggered']:
            self.update_log(f"⚠️ REAKSİYON: {res['reaction']}! Sıcaklık Artışı: +{res['temp_rise']}K")
        else:
            self.update_log("Behere Na eklendi.")

    def trigger_ai_analysis(self):
        self.ai_output.setText("AI analiz ediyor, lütfen bekleyin...")
        report = self.ai.analyze_beaker(self.engine.beaker_contents)
        self.ai_output.setText(report)

    def update_log(self, text):
        self.ai_output.append(f"\n[Sistem]: {text}")
