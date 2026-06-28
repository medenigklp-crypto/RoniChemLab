# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLabel
from config.settings import APP_NAME, VERSION, THEME
from core.engine import SimulationEngine
from core.substances import Chemical
from features.ai_assistant import ChemAIAssistant
from features.reporter import ChemReporter
from features.voice_control import ChemVoiceController  # Sesli kontrolü içe aktardık
from ui.canvas import ChemCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = SimulationEngine()
        self.ai = ChemAIAssistant()
        self.reporter = ChemReporter()
        self.voice_controller = ChemVoiceController(self)  # Sesli kontrol motorunu tanımladık
        self.reaction_history = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(1100, 700)
        
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        # SOL TARAF: Simülasyon Kontrol ve Dinamik Beher Alanı
        sim_layout = QVBoxLayout()
        self.canvas = ChemCanvas()
        
        btn_add_water = QPushButton("Saf Su Ekle (H2O)")
        btn_add_sodium = QPushButton("Sodyum Ekle (Na)")
        
        btn_add_water.clicked.connect(self.add_water)
        btn_add_sodium.clicked.connect(self.add_sodium)
        
        sim_layout.addWidget(self.canvas, stretch=4)
        sim_layout.addWidget(btn_add_water)
        sim_layout.addWidget(btn_add_sodium)
        
        # SAĞ TARAF: AI Sohbet Paneli, Raporlama ve Sesli Kontrol
        ai_layout = QVBoxLayout()
        ai_title = QLabel("AI Kimya Asistanı & Akıllı Laboratuvar")
        ai_title.setStyleSheet(f"color: {THEME['primary']}; font-weight: bold; font-size: 14px;")
        
        self.ai_output = QTextEdit()
        self.ai_output.setReadOnly(True)
        self.ai_output.setStyleSheet(f"background-color: {THEME['surface']}; color: {THEME['text_main']}; border: 1px solid {THEME['secondary']};")
        
        btn_analyze = QPushButton("Beheri AI ile Analiz Et")
        btn_report = QPushButton("📄 Profesyonel Deney Raporu Üret")
        btn_voice = QPushButton("🎤 Sesli Komut Modunu Aç")  # Yeni Ses Butonu
        
        btn_analyze.clicked.connect(self.trigger_ai_analysis)
        btn_report.clicked.connect(self.trigger_report_generation)
        btn_voice.clicked.connect(self.trigger_voice_control)  # Ses fonksiyonuna bağladık
        
        ai_layout.addWidget(ai_title)
        ai_layout.addWidget(self.ai_output)
        ai_layout.addWidget(btn_analyze)
        ai_layout.addWidget(btn_report)
        ai_layout.addWidget(btn_voice)  # Butonu arayüze yerleştirdik
        
        main_layout.addLayout(sim_layout, stretch=2)
        main_layout.addLayout(ai_layout, stretch=1)
        
        self.setCentralWidget(main_widget)
        self.apply_global_styles()

    def apply_global_styles(self):
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
        self.canvas.set_liquid(0.4, THEME["accent_bio"])
        self.update_log("Behere Saf Su (H2O) eklendi.")

    def add_sodium(self):
        sodium = Chemical("Na", "Sodyum Metal", "solid", "#C0C0C0", 0.97, 7.0, 298.15)
        res = self.engine.add_substance(sodium)
        
        if res['triggered']:
            self.canvas.add_explosion_particles()
            self.canvas.set_liquid(0.5, "#EAEAEA")
            log_msg = f"REAKSİYON: {res['reaction']} - Sıcaklık Artışı: +{res['temp_rise']}K"
            self.reaction_history.append(log_msg)
            self.update_log(f"⚠️ {log_msg}")
        else:
            self.update_log("Behere Sodyum (Na) metal parçası bırakıldı.")

    def trigger_ai_analysis(self):
        self.ai_output.setText("AI analiz ediyor, lütfen bekleyin...")
        report = self.ai.analyze_beaker(self.engine.beaker_contents)
        self.ai_output.setText(report)

    def trigger_report_generation(self):
        report_content = self.reporter.generate_markdown_report(
            self.engine.beaker_contents, 
            self.reaction_history
        )
        self.ai_output.setText(report_content)

    def trigger_voice_control(self):
        """Sesli kontrolü başlatır ve dinleme durumunu ekrana basar."""
        self.update_log("🎤 Sesli komut dinleniyor... (Konuşun: 'saf su ekle', 'sodyum ekle' vb.)")
        result = self.voice_controller.listen_and_execute()
        self.update_log(f"[Ses Sistemi]: {result}")

    def update_log(self, text):
        self.ai_output.append(f"\n[Sistem]: {text}")

