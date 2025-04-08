"""
Veri analizi için rapor şablonu
"""
import pandas as pd
from .base_template import BaseReport
from ..components.cover_page import CoverPage
from ..components.table_of_contents import TableOfContents
from ..components.data_summary import DataSummary
from ..components.visualizations import CorrelationMatrix, DistributionPlots, ImageGallery
from ..components.text_sections import FindingsSummary, TitlePage

# data_analysis_template.py güncelleme
class DataAnalysisReport(BaseReport):
    """
    Veri analizi için rapor şablonu
    """
    def __init__(self, df, title="Veri Analizi Raporu", author=None, 
                 visuals_directory=None, logo_path=None, add_comments=True,
                 findings=None):
        """
        Args:
            df (pd.DataFrame): Analiz edilecek veri çerçevesi
            title (str): Rapor başlığı
            author (str): Rapor yazarı
            visuals_directory (str): Görselleştirmelerin bulunduğu dizin
            logo_path (str): Logo dosyasının yolu
            add_comments (bool): Grafiklere otomatik yorum eklensin mi?
            findings (list): Rapor sonunda gösterilecek bulgular listesi
        """
        super().__init__(title, author)
        self.df = df
        self.visuals_directory = visuals_directory
        self.logo_path = logo_path
        self.add_comments = add_comments
        self.findings = findings
        self.build()
        
    def build(self):
        """
        Veri analizi raporunu oluşturur
        """
        # Kapak sayfası
        self.add_component(CoverPage(
            title=self.title,
            subtitle=f"Gözlem Sayısı: {len(self.df):,} | Özellik Sayısı: {len(self.df.columns)}",
            author=self.author,
            logo_path=self.logo_path
        ))
        
        # İçindekiler
        toc_items = [
            "1. Veri Özeti",
            "2. Korelasyon Analizi",
            "3. Dağılım Analizi"
        ]
        
        if self.visuals_directory:
            toc_items.append("4. Görsel Analizler")
            
        if self.findings:
            toc_items.append("5. Bulgular Özeti")
            
        self.add_component(TableOfContents(toc_items))
        
        # Veri özeti
        self.add_component(DataSummary(self.df, "1. VERİ ÖZETİ"))
        
        # Korelasyon analizi
        self.add_component(CorrelationMatrix(self.df, "2. KORELASYON ANALİZİ", 
                                           add_comments=self.add_comments))
        
        # Dağılım analizi
        self.add_component(DistributionPlots(self.df, "3. DAĞILIM ANALİZİ"))
        
        # Eğer görsel dizini belirtilmişse, görselleri ekle
        if self.visuals_directory:
            self.add_component(TitlePage("4. GÖRSEL ANALİZLER"))
            self.add_component(ImageGallery(self.visuals_directory))
            
        # Eğer bulgular belirtilmişse, bulgular özetini ekle
        if self.findings:
            self.add_component(FindingsSummary(self.findings, "5. BULGULAR ÖZETİ"))