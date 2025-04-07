"""
Rapor kapak sayfası bileşeni
"""
import matplotlib.pyplot as plt
from datetime import datetime
from ..core import ReportComponent

class CoverPage(ReportComponent):
    """
    Rapor kapak sayfası bileşeni
    """
    def __init__(self, title="Rapor", subtitle=None, author=None, date_format="%d/%m/%Y %H:%M"):
        """
        Args:
            title (str): Rapor başlığı
            subtitle (str): Alt başlık
            author (str): Yazar adı
            date_format (str): Tarih formatı
        """
        super().__init__(title, figsize=(11, 8.5))
        self.subtitle = subtitle
        self.author = author
        self.date_format = date_format
        
    def render(self, pdf):
        """
        Kapak sayfasını oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        plt.figure(figsize=self.figsize)
        
        # Başlık
        plt.text(0.5, 0.7, self.title.upper(), 
                ha='center', va='center', fontsize=20, fontweight='bold')
        
        # Alt başlık
        if self.subtitle:
            plt.text(0.5, 0.5, self.subtitle, 
                    ha='center', va='center', fontsize=14)
        
        # Yazar
        if self.author:
            plt.text(0.5, 0.4, f"Hazırlayan: {self.author}", 
                    ha='center', va='center', fontsize=12)
        
        # Tarih
        current_time = datetime.now().strftime(self.date_format)
        plt.text(0.5, 0.3, f"Oluşturulma Tarihi: {current_time}", 
                ha='center', va='center', fontsize=12)
        
        plt.axis('off')
        pdf.savefig(bbox_inches='tight')
        plt.close()