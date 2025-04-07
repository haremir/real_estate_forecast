"""
Rapor oluşturucu sınıfını içerir.
"""
import os
from .core import PdfReport
from datetime import datetime

class ReportGenerator:
    """
    Rapor oluşturmak için ana sınıf.
    """
    def __init__(self, template, output_path=None, style='ggplot', config=None):
        """
        Args:
            template: Kullanılacak rapor şablonu
            output_path (str): PDF çıktı dosyasının yolu
            style (str): Matplotlib stil adı
            config (dict): Matplotlib konfigürasyon ayarları
        """
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            output_path = f"report_{timestamp}.pdf"
            
        self.template = template
        self.pdf_report = PdfReport(output_path, style, config)
    
    def generate(self):
        """
        Şablonu kullanarak raporu oluşturur.
        """
        components = self.template.get_components()
        return self.pdf_report.create_report(components)