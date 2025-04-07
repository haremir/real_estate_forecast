"""
Temel rapor şablonu
"""
from abc import ABC, abstractmethod

class BaseReport(ABC):
    """
    Tüm rapor şablonları için temel sınıf
    """
    def __init__(self, title=None, author=None):
        """
        Args:
            title (str): Rapor başlığı
            author (str): Rapor yazarı
        """
        self.title = title if title else "Rapor"
        self.author = author
        self.components = []
        
    def add_component(self, component):
        """
        Rapora bir bileşen ekler
        
        Args:
            component: ReportComponent sınıfından türeyen bir nesne
        """
        self.components.append(component)
        return self
        
    def get_components(self):
        """
        Rapor bileşenlerini döndürür
        
        Returns:
            list: Bileşenlerin listesi
        """
        return self.components
        
    @abstractmethod
    def build(self):
        """
        Rapor şablonunu bileşenleriyle oluşturur
        """
        pass