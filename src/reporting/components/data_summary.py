"""
Veri özeti rapor bileşeni
"""
import matplotlib.pyplot as plt
import pandas as pd
from ..core import ReportComponent
from ..utils import format_dataframe_summary

class DataSummary(ReportComponent):
    """
    Veri özeti rapor bileşeni
    """
    def __init__(self, df, title="VERİ ÖZETİ"):
        """
        Args:
            df (pd.DataFrame): Özeti oluşturulacak veri çerçevesi
            title (str): Başlık
        """
        super().__init__(title, figsize=(11, 8.5))
        self.df = df
        
    def render(self, pdf):
        """
        Veri özeti sayfasını oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        plt.figure(figsize=self.figsize)
        
        # Başlık
        plt.text(0.5, 0.95, self.title, 
                ha='center', va='center', fontsize=16, fontweight='bold')
        
        # İstatistiksel özet için bir tablo hazırla
        stats_text = format_dataframe_summary(self.df)
        
        plt.text(0.1, 0.8, stats_text, 
                ha='left', va='top', fontsize=9, family='monospace')
        
        plt.axis('off')
        pdf.savefig(bbox_inches='tight')
        plt.close()