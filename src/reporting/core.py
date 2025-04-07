"""
Rapor oluşturma sisteminin temel sınıflarını içerir.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from abc import ABC, abstractmethod

class PdfReport:
    """
    PDF raporu oluşturmak için temel sınıf.
    """
    def __init__(self, output_path=None, style='ggplot', config=None):
        """
        Args:
            output_path (str): PDF çıktı dosyasının yolu
            style (str): Matplotlib stil adı
            config (dict): Matplotlib konfigürasyon ayarları
        """
        self.output_path = output_path
        self.style = style
        self.default_config = {
            'figure.figsize': (11, 8),
            'font.size': 10,
            'axes.titlesize': 14,
            'axes.labelsize': 12
        }
        self.config = config if config else self.default_config
        self.initialize_style()
        
    def initialize_style(self):
        """Görsel stilini başlatır"""
        plt.style.use(self.style)
        sns.set_palette("husl")
        plt.rcParams.update(self.config)
    
    def create_report(self, components):
        """
        Raporun bileşenlerini kullanarak PDF oluşturur
        
        Args:
            components (list): ReportComponent sınıfından türeyen nesnelerin listesi
        """
        if not self.output_path:
            raise ValueError("Output path is not specified")
            
        # Output klasörünün varlığını kontrol et
        output_dir = os.path.dirname(self.output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"ℹ Bilgi: Çıktı klasörü oluşturuldu: {output_dir}")
            
        with PdfPages(self.output_path) as pdf:
            for component in components:
                component.render(pdf)
                
        print(f"✓ Rapor başarıyla oluşturuldu:\n{os.path.abspath(self.output_path)}")
        return True

class ReportComponent(ABC):
    """
    Raporun her bir bölümü için soyut temel sınıf.
    Bu sınıftan türetilmiş sınıflar bir rapora eklenebilir.
    """
    def __init__(self, title=None, figsize=(11, 8.5)):
        self.title = title
        self.figsize = figsize
    
    @abstractmethod
    def render(self, pdf):
        """
        Bileşeni PDF'e ekle.
        
        Args:
            pdf (PdfPages): Matplotlib PdfPages nesnesi
        """
        pass