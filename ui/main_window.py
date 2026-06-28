# ui/main_window.py
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt6.QtCore import Qt
from config.settings import APP_NAME, VERSION, THEME
from core.engine import SimulationEngine
from core.substances import Chemical
from features.ai_assistant import ChemAIAssistant
from features.reporter import ChemReporter
from features.voice_control import ChemVoiceController
from ui.canvas import ChemCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.engine = SimulationEngine()
        self.ai = ChemAIAssistant()
        self.reporter = ChemReporter()
        self.voice_controller = ChemVoiceController(self)
        self.reaction_history = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(1100, 700)
        
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        
        # SOL TARAF: Simülasyon Kontrol, Göstergeler ve Kanvas
        sim_layout = QVBoxLayout()
        
        # --- YENİ: DİJİTAL GÖSTERGE PANELİ (DASHBOARD) ---
        self.dashboard_layout = QHBoxLayout()
        
        self.lbl_ph = QLabel("pH: 7.00")
        self.lbl_ph.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_ph.setStyleSheet(f"""
            background-color: {THEME['surface']}; 
            color: #00FF66; 
            font-family: 'Courier New', monospace; 
            font-size: 18px; 
            font-weight: bold; 
            border: 2px solid {THEME['secondary']}; 
            border-radius: 5px; 
            padding: 8px;
        """)
        
        self.lbl_temp = QLabel("Sıcaklık: 298.15 K")
        self.lbl_temp.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_temp.setStyleSheet(f"""
            background-color: {THEME['surface']}; 
            color: #FF3333; 
            font-family: 'Courier New', monospace; 
            font-size: 18px; 
            font-weight: bold; 
            border: 2px solid {THEME['secondary']}; 
            border-radius: 5px; 
            padding: 8px;
        """)
        
        self.dashboard_layout.addWidget(self.lbl_ph)
        self.dashboard_layout.addWidget(self.lbl_temp)
        # -------------------------------------------------
        
        self.canvas = ChemCanvas()
        
        # Kimyasal Ekleme Butonları
        btn_add_water = QPushButton("Saf Su Ekle (H2O)")
        btn_add_sodium = QPushButton("Sodyum Ekle (Na)")
        btn_add_hcl = QPushButton("Hidroklorik Asit Ekle (HCl)")
        btn_add_naoh = QPushButton("Sodyum Hidroksit Ekle (NaOH)")
        btn_add_indicator = QPushButton("Fenolftalein Damlat (İndikatör)")
        
        # Buton Bağlantıları
        btn_add_water.clicked.connect(self.add_water)
        btn_add_sodium.clicked.connect(self.add_sodium)
        btn_add_hcl.clicked.connect(self.add_hcl)
        btn_add_naoh.clicked.connect(self.add_naoh)
        btn_add_indicator.clicked.connect(self.add_indicator)
        
        # Sol taraf dizilimi: Önce göstergeler, sonra beherin kanvası, sonra butonlar
        sim_layout.addLayout(self.dashboard_layout)
        sim_layout.addWidget(self.canvas, stretch=4)
        sim_layout.addWidget(btn_add_water)
        sim_layout.addWidget(btn_add_sodium)
        sim_layout.addWidget(btn_add_hcl)
        sim_layout.addWidget(btn_add_naoh)
        sim_layout.addWidget(btn_add_indicator)
        
        # SAĞ TARAF: AI Sohbet Paneli, Raporlama ve Sesli Kontrol
        ai_layout = QVBoxLayout()
        ai_title = QLabel("AI Kimya Asistanı & Akıllı Laboratuvar")
        ai_title.setStyleSheet(f"color: {THEME['primary']}; font-weight: bold; font-size: 14px;")
        
        self.ai_output = QTextEdit()
        self.ai_output.setReadOnly(True)
        self.ai_output.setStyleSheet(f"background-color: {THEME['surface']}; color: {THEME['text_main']}; border: 1px solid {THEME['secondary']};")
        
        btn_analyze = QPushButton("Beheri AI ile Analiz Et")
        btn_report = QPushButton("📄 Profesyonel Deney Raporu Üret")
        btn_voice = QPushButton("🎤 Sesli Komut Modunu Aç")
        
        btn_analyze.clicked.connect(self.trigger_ai_analysis)
        btn_report.clicked.connect(self.trigger_report_generation)
        btn_voice.clicked.connect(self.trigger_voice_control)
        
        ai_layout.addWidget(ai_title)
        ai_layout.addWidget(self.ai_output)
        ai_layout.addWidget(btn_analyze)
        ai_layout.addWidget(btn_report)
        ai_layout.addWidget(btn_voice)
        
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

    def refresh_canvas_visuals(self):
        """Motorun güncel durumuna göre kanvas rengini, seviyesini ve dijital göstergeleri günceller."""
        current_color = self.engine.get_canvas_color()
        fill_ratio = min(0.2 + (len(self.engine.beaker_contents) * 0.15), 0.8)
        self.canvas.set_liquid(fill_ratio, current_color)
        
        # --- YENİ: PANEL GÖSTERGELERİNİ GÜNCELLE ---
        self.lbl_ph.setText(f"pH: {self.engine.mixed_ph:.2f}")
        
        # Beherdeki en yüksek sıcaklığı bul ve ekrana bas
        if self.engine.beaker_contents:
            max_temp = max([c.temperature for c in self.engine.beaker_contents])
            self.lbl_temp.setText(f"Sıcaklık: {max_temp:.2f} K")
        else:
            self.lbl_temp.setText("Sıcaklık: 298.15 K")
        # -------------------------------------------

    def add_water(self):
        water = Chemical("H2O", "Saf Su", "liquid", "#3483FA", 1.0, 7.0, 298.15)
        self.engine.add_substance(water)
        self.refresh_canvas_visuals()
        self.update_log("Behere Saf Su (H2O) eklendi.")

    def add_sodium(self):
        sodium = Chemical("Na", "Sodyum Metal", "solid", "#C0C0C0", 0.5, 7.0, 298.15)
        res = self.engine.add_substance(sodium)
        
        if res['triggered']:
            self.canvas.add_explosion_particles()
            log_msg = f"REAKSİYON: {res['reaction']} - Sıcaklık Artışı: +{res['temp_rise']}K"
            self.reaction_history.append(log_msg)
            self.update_log(f"⚠️ {log_msg}")
        else:
            self.update_log("Behere Sodyum (Na) metal parçası bırakıldı.")
        self.refresh_canvas_visuals()

    def add_hcl(self):
        hcl = Chemical("HCl", "Hidroklorik Asit", "liquid", "#E2E2E2", 0.5, 1.2, 298.15)
        res = self.engine.add_substance(hcl)
        
        if res['triggered']:
            log_msg = f"NÖTRLEŞME: {res['reaction']} - Ekzotermik Isı: +{res['temp_rise']}K"
            self.reaction_history.append(log_msg)
            self.update_log(f"⚡ {log_msg}")
        else:
            self.update_log("Behere Hidroklorik Asit (HCl) çözeltisi eklendi.")
        self.refresh_canvas_visuals()

    def add_naoh(self):
        naoh = Chemical("NaOH", "Sodyum Hidroksit", "liquid", "#F5F5F5", 0.5, 13.5, 298.15)
        res = self.engine.add_substance(naoh)
        
        if res['triggered']:
            log_msg = f"NÖTRLEŞME: {res['reaction']} - Ekzotermik Isı: +{res['temp_rise']}K"
            self.reaction_history.append(log_msg)
            self.update_log(f"⚡ {log_msg}")
        else:
            self.update_log("Behere Sodyum Hidroksit (NaOH) kuvvetli baz çözeltisi eklendi.")
        self.refresh_canvas_visuals()

    def add_indicator(self):
        indicator = Chemical("Phenolphthalein", "Fenolftalein İndikatörü", "liquid", "#FFFFFF", 0.05, 7.0, 298.15)
        self.engine.add_substance(indicator)
        self.update_log("Behere birkaç damla Fenolftalein indikatörü damlatıldı.")
        self.refresh_canvas_visuals()

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
        self.update_log("🎤 Sesli komut dinleniyor...")
        result = self.voice_controller.listen_and_execute()
        self.update_log(f"[Ses Sistemi]: {result}")

    def update_log(self, text):
        self.ai_output.append(f"\n[Sistem]: {text}")
