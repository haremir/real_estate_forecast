"""
Özel rapor şablonu
"""
from .base_template import BaseReport
from ..components.cover_page import CoverPage
from ..components.table_of_contents import TableOfContents

class CustomReport(BaseReport):
    """
    Özel rapor şablonu.
    Bileşenler, bu şablonun kullanıcıları tarafından eklenir.
    """
    def __init__(self, title="Özel Rapor", author=None):
        """
        Args:
            title (str): Rapor başlığı
            author (str): Rapor yazarı
        """
        super().__init__(title, author)
        
    def build(self):
        """
        Özel raporun temel yapısını oluşturur.
        Bu metodu override edebilir veya add_component metodunu kullanabilirsiniz.
        """
        # Kapak sayfası
        self.add_component(CoverPage(
            title=self.title,
            author=self.author
        ))
        
        # İçindekiler sayfası - öğeler eklendikçe güncellenir
        self.add_component(TableOfContents([]))