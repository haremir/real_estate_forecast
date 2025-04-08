# cover_page.py güncelleniyor
from datetime import datetime
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from ..core import ReportComponent

class CoverPage(ReportComponent):
    def __init__(self, title="BOSTON KONUT ANALİZ RAPORU", 
                 subtitle=None, 
                 author="HAREZMİ INTELLIGENCE", 
                 logo_path=None, 
                 date_format="%d/%m/%Y %H:%M",
                 theme_config=None):
        super().__init__(title, figsize=(11, 8.5))
        self.subtitle = subtitle or "Veri Bilimi Ekibi"
        self.author = author
        self.logo_path = logo_path
        self.date_format = date_format
        self.theme = theme_config or {
            "primary": "#2E86AB",
            "secondary": "#F18F01",
            "background": "#212121",  # Logo ile uyumlu koyu arka plan
            "text_color": "#FFFFFF",  # Beyaz metin
            "accent": "#00E5E0"  # Logo'daki turkuaz renk
        }

    def render(self, pdf):
        # Koyu arka planlı tam sayfa figür oluştur
        fig, ax = plt.subplots(figsize=self.figsize)
        fig.patch.set_facecolor(self.theme["background"])
        ax.set_facecolor(self.theme["background"])
        
        # Turkuaz vurgu çizgisi ekle
        ax.add_patch(Rectangle((0, 0.4), 1, 0.02, 
                             color=self.theme["accent"], 
                             transform=ax.transAxes,
                             alpha=0.7))
        
        # Logo Ekleme
        if self.logo_path:
            try:
                img = plt.imread(self.logo_path)
                imagebox = OffsetImage(img, zoom=0.5, resample=True)
                ab = AnnotationBbox(imagebox, (0.5, 0.65), frameon=False, box_alignment=(0.5, 0.5))
                ax.add_artist(ab)
            except Exception as e:
                print(f"⚠️ Logo yüklenemedi: {e}")

        # Metinler (Koyu arka plan üzerine beyaz)
        plt.text(0.5, 0.35, self.title, 
                ha='center', va='center', 
                fontsize=24, fontweight='bold', color=self.theme["text_color"],
                transform=ax.transAxes)
        
        plt.text(0.5, 0.28, self.subtitle, 
                ha='center', va='center', 
                fontsize=16, color=self.theme["accent"],
                transform=ax.transAxes)
        
        plt.text(0.5, 0.18, f"Hazırlayan: {self.author}", 
                ha='center', va='center', 
                fontsize=14, color=self.theme["text_color"],
                transform=ax.transAxes)
        
        plt.text(0.5, 0.12, f"Oluşturulma Tarihi: {datetime.now().strftime(self.date_format)}", 
                ha='center', va='center', 
                fontsize=12, color=self.theme["text_color"],
                alpha=0.7, transform=ax.transAxes)
        
        plt.axis('off')
        pdf.savefig(bbox_inches='tight', dpi=300, facecolor=self.theme["background"])
        plt.close()