# features/voice_control.py
import speech_recognition as sr

class ChemVoiceController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.recognizer = sr.Recognizer()

    def listen_and_execute(self):
        """Mikrofonu dinler ve gelen komuta göre ana penceredeki fonksiyonları tetikler."""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                # Sesi kaydet ve Google Speech Recognition ile metne çevir
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                command = self.recognizer.recognize_google(audio, language="tr-TR").lower()
                
                print(f"[Sesli Komut Algılandı]: {command}")
                self.process_command(command)
                return f"Algılanan Komut: '{command}'"
            except sr.WaitTimeoutError:
                return "Ses duyulamadı, zaman aşımı."
            except sr.UnknownValueError:
                return "Komut anlaşılamadı."
            except Exception as e:
                return f"Ses sistemi hatası: {str(e)}"

    def process_command(self, command):
        """Metne dökülen komutu analiz edip arayüz fonksiyonlarını tetikler."""
        if "su ekle" in command or "saf su" in command:
            self.main_window.add_water()
        elif "sodyum" in command or "metal ekle" in command:
            self.main_window.add_sodium()
        elif "analiz" in command or "asistan" in command:
            self.main_window.trigger_ai_analysis()
        elif "rapor" in command or "rapor üret" in command:
            self.main_window.trigger_report_generation()
