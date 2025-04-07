#!/usr/bin/env python3
"""
Boston Housing - Rapor Üretici
Kullanım:
  python report.py [--input <path>] [--output <path>]
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime

# --------------------------
# KONFİGÜRASYON
# --------------------------
# Proje kök dizinini belirle (src klasörünün bir seviye üstü)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DEFAULT_INPUT = os.path.join(PROJECT_ROOT, "data", "processed", "cleaned_boston.csv")
DEFAULT_OUTPUT = os.path.join(PROJECT_ROOT, "report", f"analysis_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf")
VISUALIZATIONS_DIR = os.path.join(PROJECT_ROOT, "src", "visualizations")

# Mevcut görselleştirmeler
VISUALIZATION_FILES = [
    "final_correlation.png",
    "medv_boxplot.png",
    "medv_boxplot_dist.png",
    "medv_distribution.png",
    "missing_data.png",
    "pairplot.png",
    "rm_vs_medv.png",
    "scorrelation_matrix.png"
]

# Görsel açıklamaları
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

STYLE_CONFIG = {
    'figure.figsize': (11, 8),
    'font.size': 10,
    'axes.titlesize': 14,
    'axes.labelsize': 12
}

# --------------------------
# RAPOR FONKSİYONLARI
# --------------------------
def initialize_report():
    """Rapor başlangıç ayarları"""
    plt.style.use('ggplot')
    sns.set_palette("husl")
    plt.rcParams.update(STYLE_CONFIG)

def create_cover_page(pdf, df):
    """Kapak sayfası oluşturur"""
    plt.figure(figsize=(11, 8.5))
    plt.text(0.5, 0.7, "BOSTON KONUT ANALİZ RAPORU", 
            ha='center', va='center', fontsize=20, fontweight='bold')
    plt.text(0.5, 0.5, f"Veri Seti: {os.path.basename(args.input)}", 
            ha='center', va='center', fontsize=14)
    plt.text(0.5, 0.4, f"Gözlem Sayısı: {len(df):,} | Özellik Sayısı: {len(df.columns)}", 
            ha='center', va='center', fontsize=12)
    plt.text(0.5, 0.3, f"Oluşturulma Tarihi: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 
            ha='center', va='center', fontsize=12)
    plt.axis('off')
    pdf.savefig(bbox_inches='tight')
    plt.close()

def create_toc_page(pdf):
    """İçindekiler sayfası oluşturur"""
    plt.figure(figsize=(11, 8.5))
    plt.text(0.5, 0.9, "İÇİNDEKİLER", 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    sections = [
        "1. Veri Özeti",
        "2. Korelasyon Analizi",
        "3. Dağılım Analizi",
        "4. Görsel Analizler"
    ]
    
    for i, section in enumerate(sections):
        plt.text(0.2, 0.8 - i*0.1, section, 
                ha='left', va='center', fontsize=12)
    
    plt.axis('off')
    pdf.savefig(bbox_inches='tight')
    plt.close()

def add_analysis_section(pdf, df, title, analysis_func, figsize=(11, 6)):
    """Analiz bölümü ekler"""
    plt.figure(figsize=figsize)
    analysis_func(df)
    plt.title(title, pad=20)
    pdf.savefig(bbox_inches='tight')
    plt.close()

def add_data_summary(pdf, df):
    """Veri özeti bölümü ekler"""
    plt.figure(figsize=(11, 8.5))
    plt.text(0.5, 0.95, "1. VERİ ÖZETİ", 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # İstatistiksel özet için bir tablo hazırla
    stats = df.describe().round(2)
    stats_text = ""
    for col in stats.columns:
        stats_text += f"Özellik: {col}\n"
        for stat, value in stats[col].items():
            stats_text += f"   {stat}: {value}\n"
        stats_text += "\n"
    
    plt.text(0.1, 0.8, stats_text, 
            ha='left', va='top', fontsize=9, family='monospace')
    
    plt.axis('off')
    pdf.savefig(bbox_inches='tight')
    plt.close()

def add_existing_visualizations(pdf):
    """Mevcut görselleştirmeleri rapora ekler"""
    for img_file in VISUALIZATION_FILES:
        img_path = os.path.join(VISUALIZATIONS_DIR, img_file)
        if os.path.exists(img_path):
            # Görsel için yeni bir sayfa oluştur
            plt.figure(figsize=(11, 8.5))
            img = mpimg.imread(img_path)
            plt.imshow(img)
            plt.axis('off')
            
            # Görselin açıklamasını ekle
            if img_file in VISUALIZATION_DESCRIPTIONS:
                plt.figtext(0.5, 0.01, VISUALIZATION_DESCRIPTIONS[img_file], 
                        ha='center', va='bottom', fontsize=10, 
                        bbox=dict(facecolor='white', alpha=0.8))
            
            # Başlık ekle
            plt.title(f"Görsel: {img_file.replace('_', ' ').replace('.png', '')}", pad=20)
            
            pdf.savefig(bbox_inches='tight')
            plt.close()
        else:
            print(f"⚠️ Uyarı: {img_file} dosyası bulunamadı.")

# --------------------------
# ANALİZ FONKSİYONLARI
# --------------------------
def plot_correlation(df):
    """Korelasyon matrisi"""
    corr = df.corr(numeric_only=True)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
               cbar_kws={"shrink": 0.8}, annot_kws={"size": 8})
    
def plot_distributions(df):
    """Temel dağılımlar"""
    num_cols = df.select_dtypes(include=np.number).columns
    for i, col in enumerate(num_cols[:4]):  # İlk 4 sayısal sütun
        plt.subplot(2, 2, i+1)
        sns.histplot(df[col], kde=True)
        plt.title(col)
    plt.tight_layout()

# --------------------------
# ANA İŞLEM
# --------------------------
def generate_report(input_path, output_path):
    """PDF raporu oluşturur"""
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
        if not os.path.exists(VISUALIZATIONS_DIR):
            print(f"⚠️ Uyarı: Görselleştirmeler klasörü bulunamadı: {VISUALIZATIONS_DIR}")
        
        df = pd.read_csv(input_path)
        initialize_report()
        
        with PdfPages(output_path) as pdf:
            # Kapak ve içindekiler
            create_cover_page(pdf, df)
            create_toc_page(pdf)
            
            # Veri özeti
            add_data_summary(pdf, df)
            
            # Analiz bölümleri
            add_analysis_section(pdf, df, "2. Özellik Korelasyonları", plot_correlation)
            add_analysis_section(pdf, df, "3. Temel Dağılımlar", plot_distributions, figsize=(11, 8))
            
            # Mevcut görselleştirmeleri ekle
            plt.figure(figsize=(11, 8.5))
            plt.text(0.5, 0.5, "4. GÖRSEL ANALİZLER", 
                    ha='center', va='center', fontsize=16, fontweight='bold')
            plt.axis('off')
            pdf.savefig(bbox_inches='tight')
            plt.close()
            
            add_existing_visualizations(pdf)
            
        print(f"✓ Rapor başarıyla oluşturuldu:\n{os.path.abspath(output_path)}")
        return True
    except Exception as e:
        print(f"✗ Hata: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=DEFAULT_INPUT, 
                       help="Girdi CSV dosya yolu (varsayılan: data/processed/cleaned_boston.csv)")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                       help="Çıktı PDF dosya yolu (varsayılan: report/analysis_report_YYYYMMDD.pdf)")
    parser.add_argument("--visuals-dir", default=VISUALIZATIONS_DIR,
                       help="Görselleştirmeler klasörü (varsayılan: src/visualizations)")
    args = parser.parse_args()
    
    # Görselleştirmeler klasörünü güncelle (eğer argüman verilmişse)
    if args.visuals_dir != VISUALIZATIONS_DIR:
        VISUALIZATIONS_DIR = args.visuals_dir
    
    # Yolları normalize et
    input_path = os.path.abspath(os.path.normpath(args.input))
    output_path = os.path.abspath(os.path.normpath(args.output))
    
    # Bilgileri görüntüle
    print(f"Girdi dosyası: {input_path}")
    print(f"Çıktı dosyası: {output_path}")
    print(f"Görselleştirmeler klasörü: {VISUALIZATIONS_DIR}")
    
    sys.exit(0 if generate_report(input_path, output_path) else 1)