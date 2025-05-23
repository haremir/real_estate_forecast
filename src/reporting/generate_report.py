#!/usr/bin/env python3
"""
Boston Housing - Modüler Rapor Üretici
Kullanım:
  python generate_report.py [--input <path>] [--output <path>] [--visuals-dir <path>] [--logo <path>]
"""

import os
import sys
import argparse
import pandas as pd
from datetime import datetime

# Proje kök dizinini belirle (src klasörünün bir seviye üstü)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Modüler rapor sisteminin bulunduğu klasörü Python yoluna ekle
sys.path.append(os.path.join(PROJECT_ROOT, "reporting"))  # reporting klasörünü ekle
# veya
sys.path.append(PROJECT_ROOT)  # Eğer reporting klasörü proje kök dizininde ise

# Şimdi import edebilirsiniz
from src.reporting import ReportGenerator, DataAnalysisReport

# Varsayılan dosya yolları
DEFAULT_INPUT = os.path.join(PROJECT_ROOT, "data", "processed", "cleaned_boston.csv")
VISUALIZATIONS_DIR = os.path.join(PROJECT_ROOT, "src", "visualizations")
DEFAULT_OUTPUT = os.path.join(
    PROJECT_ROOT, "reports", f"boston_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
)
DEFAULT_LOGO = os.path.join(PROJECT_ROOT, "src", "assets", r"C:\Users\PC\Desktop\real_estate_forecast\src\reporting\assets\harezmi_intelligence.PNG")

# Görsel açıklamaları - İsteğe bağlı görsel açıklamaları ekleyebilirsiniz
VISUALIZATION_DESCRIPTIONS = {
    "final_correlation.png": "Özellikler arasındaki korelasyon ilişkisini gösteren ısı haritası. Konut fiyatlarıyla (MEDV) en güçlü ilişkiye sahip değişkenler gösterilmektedir.",
    "medv_boxplot.png": "Konut değerlerinin kutu grafiği. Bu görsel, veri setindeki aykırı değerleri ve fiyat dağılımının merkeziliğini göstermektedir.",
    "medv_boxplot_dist.png": "Konut değerlerinin hem kutu grafiği hem de dağılımı. Bu kombine grafik, fiyat dağılımının yapısını anlamayı kolaylaştırır.",
    "medv_distribution.png": "Konut değerlerinin dağılım grafiği. Histogramdan görüldüğü üzere, fiyat dağılımı sağa çarpıktır.",
    "missing_data.png": "Veri setindeki eksik değerlerin analizi. Bu görsel, veri temizleme sürecinde kullanılmıştır.",
    "pairplot.png": "Tüm sayısal değişkenlerin ikili ilişkilerini gösteren matris. Değişkenler arasındaki örüntüler ve ilişkiler görselleştirilmiştir.",
    "rm_vs_medv.png": "Oda sayısı (RM) ile konut değeri (MEDV) arasındaki ilişki. Pozitif korelasyon açıkça görülmektedir.",
    "scorrelation_matrix.png": "Tüm değişkenler arasındaki korelasyon katsayılarını gösteren matris."
}

# Rapor bulgularını tanımla
REPORT_FINDINGS = [
    "Boston konut fiyatları (MEDV) ile oda sayısı (RM) arasında güçlü pozitif korelasyon bulunmaktadır.",
    "Düşük gelirli bölgelerde (LSTAT yüksek) konut fiyatları (MEDV) önemli ölçüde düşmektedir.",
    "Bölgedeki suç oranı (CRIM) arttıkça konut fiyatları düşmektedir.",
    "Charles Nehri'ne yakınlık (CHAS=1), konut fiyatlarında ortalama 5 birimlik bir artışa karşılık gelmektedir.",
    "Veri seti özelliklerinin çoğu normal dağılım göstermemekte, sağa çarpık dağılımlar görülmektedir."
]

def generate_report(input_path, output_path, visuals_dir, logo_path=None):
    """
    Modüler rapor sistemini kullanarak Boston Housing verisi için rapor üretir

    Args:
        input_path (str): Girdi CSV dosyasının yolu
        output_path (str): Çıktı PDF dosyasının yolu
        visuals_dir (str): Görselleştirmeler klasörünün yolu
        logo_path (str): Logo dosyasının yolu

    Returns:
        bool: Başarılı ise True, değilse False
    """
    try:
        # Input dosyasının varlığını kontrol et
        if not os.path.exists(input_path):
            print(f"✗ Hata: Girdi dosyası bulunamadı: {input_path}", file=sys.stderr)
            return False
            
        # Output klasörünün varlığını kontrol et
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"ℹ Bilgi: Çıktı klasörü oluşturuldu: {output_dir}")
        
        # Görselleştirmeler klasörünü kontrol et
        if visuals_dir and not os.path.exists(visuals_dir):
            print(f"⚠️ Uyarı: Görselleştirmeler klasörü bulunamadı: {visuals_dir}")
            visuals_dir = None
            
        # Logo dosyasını kontrol et
        if logo_path and not os.path.exists(logo_path):
            print(f"⚠️ Uyarı: Logo dosyası bulunamadı: {logo_path}")
            logo_path = None
        
        # Veriyi yükle
        df = pd.read_csv(input_path)
        print(f"ℹ Bilgi: Veri başarıyla yüklendi: {len(df)} satır, {len(df.columns)} sütun")
        
        # DataAnalysisReport şablonunu kullanarak rapor oluştur
        template = DataAnalysisReport(
            df=df,
            title="BOSTON KONUT ANALİZ RAPORU",
            author="HAREZMİ INTELLIGENCE",
            visuals_directory=visuals_dir,
            logo_path=logo_path,
            add_comments=True,
            findings=REPORT_FINDINGS
        )
        
        # ImageGallery bileşenine açıklamaları ekle (eğer visuals_dir varsa)
        if visuals_dir:
            for component in template.get_components():
                from src.reporting.components.visualizations import ImageGallery
                if isinstance(component, ImageGallery):
                    component.descriptions = VISUALIZATION_DESCRIPTIONS
        
        # ReportGenerator ile PDF oluştur
        generator = ReportGenerator(
            template=template,
            output_path=output_path,
            style='ggplot',
            config={
                'figure.figsize': (11, 8),
                'font.size': 10,
                'axes.titlesize': 14,
                'axes.labelsize': 12,
                'font.family': 'sans-serif'
            }
        )
        
        result = generator.generate()
        
        if result:
            print(f"✓ Rapor başarıyla oluşturuldu:\n{os.path.abspath(output_path)}")
        
        return result
        
    except Exception as e:
        print(f"✗ Hata: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Boston Housing Rapor Üretici")
    parser.add_argument("--input", default=DEFAULT_INPUT, 
                       help=f"Girdi CSV dosya yolu (varsayılan: {DEFAULT_INPUT})")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                       help=f"Çıktı PDF dosya yolu (varsayılan: {DEFAULT_OUTPUT})")
    parser.add_argument("--visuals-dir", default=VISUALIZATIONS_DIR,
                       help=f"Görselleştirmeler klasörü (varsayılan: {VISUALIZATIONS_DIR})")
    parser.add_argument("--logo", default=DEFAULT_LOGO,
                       help=f"Logo dosyası (varsayılan: {DEFAULT_LOGO})")
    args = parser.parse_args()
    
    # Yolları normalize et
    input_path = os.path.abspath(os.path.normpath(args.input))
    output_path = os.path.abspath(os.path.normpath(args.output))
    visuals_dir = os.path.abspath(os.path.normpath(args.visuals_dir)) if args.visuals_dir else None
    logo_path = os.path.abspath(os.path.normpath(args.logo)) if args.logo else None
    
    # Bilgileri görüntüle
    print(f"Girdi dosyası: {input_path}")
    print(f"Çıktı dosyası: {output_path}")
    print(f"Görselleştirmeler klasörü: {visuals_dir}")
    print(f"Logo dosyası: {logo_path}")
    
    sys.exit(0 if generate_report(input_path, output_path, visuals_dir, logo_path) else 1)