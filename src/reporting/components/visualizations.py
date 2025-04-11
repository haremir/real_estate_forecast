"""
Veri görselleştirme rapor bileşenleri
"""
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
from ..core import ReportComponent
from ..utils import get_image_files, load_image

# visualizations.py içindeki CommentedGraph sınıfını kullanıma hazır hale getirelim

class CorrelationMatrix(ReportComponent):
    """
    Korelasyon matrisi rapor bileşeni
    """
    def __init__(self, df, title="KORELASYON ANALİZİ", add_comments=True):
        """
        Args:
            df (pd.DataFrame): Korelasyon hesaplanacak veri çerçevesi
            title (str): Başlık
            add_comments (bool): Otomatik yorum eklensin mi?
        """
        super().__init__(title, figsize=(11, 8))
        self.df = df
        self.add_comments = add_comments
        
    def render(self, pdf):
        """
        Korelasyon matrisi sayfasını oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        fig = plt.figure(figsize=self.figsize)
        
        # Grafiği çizmek için alt figür alanı oluştur
        if self.add_comments:
            plot_area = plt.subplot2grid((5, 1), (0, 0), rowspan=4)
        else:
            plot_area = plt.subplot(111)
        
        # Başlık
        plt.suptitle(self.title, fontsize=16, y=0.98)
        
        # Korelasyon matrisi
        corr = self.df.corr(numeric_only=True)
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
                   cbar_kws={"shrink": 0.8}, annot_kws={"size": 8}, ax=plot_area)
        
        # Otomatik yorum ekle
        if self.add_comments:
            comment_area = plt.subplot2grid((5, 1), (4, 0))
            comment_area.axis('off')
            
            # En yüksek korelasyonları bul
            corr_no_diag = corr.copy()
            np.fill_diagonal(corr_no_diag.values, 0)
            max_corr = corr_no_diag.abs().unstack().sort_values(ascending=False)[:3]
            
            comment = f"En yüksek korelasyonlar: "
            for (col1, col2), val in max_corr.items():
                comment += f"{col1}-{col2} ({val:.2f}), "
            comment = comment[:-2]  # Son virgülü kaldır
            
            comment_area.text(0.02, 0.5, f"📊 Yorum: {comment}", 
                         wrap=True, va='center', ha='left',
                         fontsize=10, bbox=dict(facecolor='#f8f9fa', 
                                              alpha=0.8, boxstyle='round,pad=0.5'))
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        pdf.savefig(bbox_inches='tight')
        plt.close()

class DistributionPlots(ReportComponent):
    """
    Dağılım grafikleri rapor bileşeni
    """
    def __init__(self, df, title="DAĞILIM ANALİZİ", max_cols=4):
        """
        Args:
            df (pd.DataFrame): Dağılımları çizilecek veri çerçevesi
            title (str): Başlık
            max_cols (int): Bir sayfada gösterilecek maksimum sütun sayısı
        """
        super().__init__(title, figsize=(11, 8))
        self.df = df
        self.max_cols = max_cols
        
    def render(self, pdf):
        """
        Dağılım grafikleri sayfasını oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        # Sayısal sütunları seç
        num_cols = self.df.select_dtypes(include=np.number).columns
        
        # Her sayfada en fazla max_cols sütun göster
        for i in range(0, len(num_cols), self.max_cols):
            plt.figure(figsize=self.figsize)
            
            # Başlık
            if i == 0:
                plt.suptitle(self.title, fontsize=16, y=0.98)
            else:
                plt.suptitle(f"{self.title} (Devam)", fontsize=16, y=0.98)
            
            # Grafiklerin sayısını ve yerleşimini belirle
            cols_subset = num_cols[i:i+self.max_cols]
            n_plots = len(cols_subset)
            n_rows = (n_plots + 1) // 2  # 2 sütunlu bir düzen için
            
            # Grafikleri çiz
            for j, col in enumerate(cols_subset):
                plt.subplot(n_rows, 2, j+1)
                sns.histplot(self.df[col], kde=True)
                plt.title(col)
            
            plt.tight_layout(rect=[0, 0, 1, 0.95]) # Başlık için üstte boşluk bırak
            pdf.savefig(bbox_inches='tight')
            plt.close()

class ImageGallery(ReportComponent):
    """
    Resim galerisi rapor bileşeni
    """
    def __init__(self, image_directory, title=None, descriptions=None):
        """
        Args:
            image_directory (str): Resimlerin bulunduğu dizin
            title (str): Başlık
            descriptions (dict): Resim dosya adı -> açıklama eşlemesi
        """
        super().__init__(title, figsize=(11, 8.5))
        self.image_directory = image_directory
        self.descriptions = descriptions if descriptions else {}
        
    def render(self, pdf):
        """
        Resim galerisi sayfalarını oluşturur ve PDF'e ekler
        
        Args:
            pdf (PdfPages): PDF sayfaları
        """
        image_files = get_image_files(self.image_directory)
        
        if not image_files:
            print(f"⚠️ Uyarı: Resim dizininde resim bulunamadı: {self.image_directory}")
            return
            
        for img_path in image_files:
            plt.figure(figsize=self.figsize)
            
            try:
                img = load_image(img_path)
                plt.imshow(img)
                plt.axis('off')
                
                img_filename = os.path.basename(img_path)
                
                # Görselin başlığı
                clean_title = img_filename.replace('_', ' ').replace('.png', '').replace('.jpg', '')
                plt.title(f"Görsel: {clean_title}", pad=20)
                
                # Eğer bu resim için bir açıklama varsa, ekle
                if img_filename in self.descriptions:
                    plt.figtext(0.5, 0.01, self.descriptions[img_filename], 
                            ha='center', va='bottom', fontsize=10, 
                            bbox=dict(facecolor='white', alpha=0.8))
                
                pdf.savefig(bbox_inches='tight')
                
            except Exception as e:
                print(f"⚠️ Uyarı: {img_path} dosyası yüklenemedi: {str(e)}")
                
            plt.close()

