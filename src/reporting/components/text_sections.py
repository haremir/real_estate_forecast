"""
Metin ve başlık bileşenleri
"""
import matplotlib.pyplot as plt
from ..core import ReportComponent

class TitlePage(ReportComponent):
    """
    Başlık sayfası bileşeni
    """
    def __init__(self, title):
        """
        Args:
            title (str): Sayfa başlığı
        """
        super().__init__(title, figsize=(11, 8.5))
        
    def render(self, pdf):
        """
        Başlık sayfasını oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        plt.figure(figsize=self.figsize)
        plt.text(0.5, 0.5, self.title, 
                ha='center', va='center', fontsize=16, fontweight='bold')
        plt.axis('off')
        pdf.savefig(bbox_inches='tight')
        plt.close()

class TextSection(ReportComponent):
    """
    Metin bölümü bileşeni
    """
    def __init__(self, title, text, fontsize=12):
        """
        Args:
            title (str): Bölüm başlığı
            text (str): Bölüm metni
            fontsize (int): Metin font boyutu
        """
        super().__init__(title, figsize=(11, 8.5))
        self.text = text
        self.fontsize = fontsize
        
    def render(self, pdf):
        """
        Metin bölümünü oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        plt.figure(figsize=self.figsize)
        
        # Başlık
        plt.text(0.5, 0.95, self.title, 
                ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Metin
        plt.text(0.1, 0.8, self.text, 
                ha='left', va='top', fontsize=self.fontsize, 
                wrap=True)
        
        plt.axis('off')
        pdf.savefig(bbox_inches='tight')
        plt.close()


# text_sections.py'a eklenecek yeni FindingsSummary sınıfı

class FindingsSummary(ReportComponent):
    """
    Bulgular özeti rapor bileşeni
    """
    def __init__(self, findings, title="BULGULAR ÖZETİ"):
        """
        Args:
            findings (list): Bulguların listesi veya metni
            title (str): Bölüm başlığı
        """
        super().__init__(title, figsize=(11, 8.5))
        self.findings = findings if isinstance(findings, list) else [findings]
        
    def render(self, pdf):
        """
        Bulgular özeti sayfasını oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        plt.figure(figsize=self.figsize)
        
        # Başlık
        plt.text(0.5, 0.95, self.title, 
                ha='center', va='center', fontsize=16, fontweight='bold')
        
        # Bulgular listesi
        for i, finding in enumerate(self.findings):
            plt.text(0.1, 0.85 - i*0.1, f"{i+1}. {finding}", 
                    ha='left', va='top', fontsize=12, 
                    wrap=True, bbox=dict(facecolor='#f8f9fa', alpha=0.5))
        
        plt.axis('off')
        pdf.savefig(bbox_inches='tight')
        plt.close()