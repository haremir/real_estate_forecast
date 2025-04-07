"""
Veri analizi için rapor şablonu
"""
import pandas as pd
from .base_template import BaseReport
from ..components.cover_page import CoverPage
from ..components.table_of_contents import TableOfContents
from ..components.data_summary import DataSummary
from ..components.visualizations import CorrelationMatrix, DistributionPlots, ImageGallery
from ..components.text_sections import TitlePage

class DataAnalysisReport(BaseReport):
    """
    Veri analizi için rapor şablonu
    """
    def __init__(self, df, title="Veri Analizi Raporu", author=None, 
                 visuals_directory=None):
        """
        Args:
            df (pd.DataFrame): Analiz edilecek veri çerçevesi
            title (str): Rapor başlığı
            author (str): Rapor yazarı
            visuals_directory (str): Görselleştirmelerin bulunduğu dizin
        """
        super().__init__(title, author)
        self.df = df
        self.visuals_directory = visuals_directory
        self.build()
        
    def build(self):
        """
        Veri analizi raporunu oluşturur
        """
        # Kapak sayfası
        self.add_component(CoverPage(
            title=self.title,
            subtitle=f"Gözlem Sayısı: {len(self.df):,} | Özellik Sayısı: {len(self.df.columns)}",
            author=self.author
        ))
        
        # İçindekiler
        toc_items = [
            "1. Veri Özeti",
            "2. Korelasyon Analizi",
            "3. Dağılım Analizi"
        ]
        
        if self.visuals_directory:
            toc_items.append("4. Görsel Analizler")
            
        self.add_component(TableOfContents(toc_items))
        
        # Veri özeti
        self.add_component(DataSummary(self.df, "1. VERİ ÖZETİ"))
        
        # Korelasyon analizi
        self.add_component(CorrelationMatrix(self.df, "2. KORELASYON ANALİZİ"))
        
        # Dağılım analizi
        self.add_component(DistributionPlots(self.df, "3. DAĞILIM ANALİZİ"))
        
        # Eğer görsel dizini belirtilmişse, görselleri ekle
        if self.visuals_directory:
            self.add_component(TitlePage("4. GÖRSEL ANALİZLER"))
            self.add_component(ImageGallery(self.visuals_directory))