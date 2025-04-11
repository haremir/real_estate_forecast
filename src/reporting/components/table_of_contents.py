"""
Rapor içindekiler sayfası bileşeni
"""
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from ..core import ReportComponent

class TableOfContents(ReportComponent):
    """
    Rapor içindekiler sayfası bileşeni
    """
    def __init__(self, sections, theme_config=None):
        """
        Args:
            sections (list): Bölüm başlıklarının listesi
        """
        super().__init__("İÇİNDEKİLER", figsize=(11, 8.5))
        self.sections = sections
        self.theme = theme_config or {
            "primary": "#2E86AB",
            "secondary": "#F18F01",
            "background": "#F8F9FA",
            "text_color": "#212121",
            "accent": "#00E5E0"
        }
        
    def render(self, pdf):
        """
        İçindekiler sayfasını oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        fig.patch.set_facecolor(self.theme["background"])
        
        # İnce turkuaz bir başlık çizgisi ekle
        ax.add_patch(Rectangle((0.1, 0.87), 0.8, 0.01, 
                             color=self.theme["accent"], 
                             alpha=0.7))
        
        # Başlık
        plt.text(0.5, 0.9, self.title, 
                ha='center', va='center', fontsize=18, fontweight='bold',
                color=self.theme["primary"])
        
        # Bölümler
        for i, section in enumerate(self.sections):
            plt.text(0.2, 0.8 - i*0.1, section, 
                    ha='left', va='center', fontsize=12, 
                    color=self.theme["text_color"])
        
        plt.axis('off')
        pdf.savefig(bbox_inches='tight')
        plt.close()