"""
Rapor içindekiler sayfası bileşeni
"""
import matplotlib.pyplot as plt
from ..core import ReportComponent

class TableOfContents(ReportComponent):
    """
    Rapor içindekiler sayfası bileşeni
    """
    def __init__(self, sections):
        """
        Args:
            sections (list): Bölüm başlıklarının listesi
        """
        super().__init__("İÇİNDEKİLER", figsize=(11, 8.5))
        self.sections = sections
        
    def render(self, pdf):
        """
        İçindekiler sayfasını oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        plt.figure(figsize=self.figsize)
        
        # Başlık
        plt.text(0.5, 0.9, self.title, 
                ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Bölümler
        for i, section in enumerate(self.sections):
            plt.text(0.2, 0.8 - i*0.1, section, 
                    ha='left', va='center', fontsize=12)
        
        plt.axis('off')
        pdf.savefig(bbox_inches='tight')
        plt.close()