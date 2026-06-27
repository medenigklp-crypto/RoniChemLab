# features/ai_assistant.py
import ollama

class ChemAIAssistant:
    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def analyze_beaker(self, current_chemicals: list):
        """Beherin o anki durumunu analiz eder ve otomatik rapor hazırlar."""
        if not current_chemicals:
            return "Beher şu an boş. Kimyasal ekleyerek başlayabilirsiniz."
            
        substance_list = ", ".join([f"{c.name} ({c.formula})" for c in current_chemicals])
        prompt = f"Bir kimya simülasyonunda beherde şu maddeler var: {substance_list}. Bunların olası etkileşimlerini, tehlikelerini ve reaksiyon mekanizmalarını bir kimya profesörü gibi özetle."
        
        try:
            response = ollama.generate(model=self.model_name, prompt=prompt)
            return response['response']
        except Exception:
            return f"Lokal AI modeline bağlanılamadı. Mevcut kimyasallar: {substance_list}. (Lütfen Ollama'nın arka planda açık olduğundan emin olun.)"
